from hypurrquant.evm.utils.web3 import Web3Utils as BaseWeb3Utils
from hypurrquant.evm.utils.rpc import Web3Ctx
from hypurrquant.exception import NoSuchDexProtocolException

from backend.constants import DexProtocol
from web3 import AsyncWeb3
from web3.contract import AsyncContract

from typing import Tuple, List, Dict

# items 원소 타입: (pool_address, dex_protocol)
PoolItem = Tuple[str, DexProtocol]


def _decode_slot0(data: bytes):
    sqrtPriceX96 = int.from_bytes(data[0:32], "big")
    tick = int.from_bytes(data[32:64], "big", signed=True)
    return tick, sqrtPriceX96


def _decode_globalState(ret: bytes) -> tuple[int, int]:
    # returns (tick, sqrtPriceX96) — Algebra의 price는 Q64.96 sqrtPrice
    if len(ret) < 64:
        raise ValueError("bad globalState return")
    sqrtPriceX96 = int.from_bytes(ret[0:32], "big")  # uint160, but stored left-padded
    tick = int.from_bytes(ret[32:64], "big", signed=True)
    return tick, sqrtPriceX96


def _encode_state_call(proto: DexProtocol) -> bytes:
    if proto in (DexProtocol.UNISWAP, DexProtocol.PANCAKE):
        return Web3Utils.encode_selector("slot0()")
    elif proto == DexProtocol.ALGEBRA:
        return Web3Utils.encode_selector("globalState()")
    else:
        raise NoSuchDexProtocolException(f"Unsupported dex_protocol: {proto}")


def _decode_state(proto: DexProtocol, ret: bytes) -> Tuple[int, int]:
    """
    반환: (tick, extra)
      - Uni/Pancake: (tick, sqrtPriceX96)
      - Algebra:     (tick, price_raw)
    """
    if proto in (DexProtocol.UNISWAP, DexProtocol.PANCAKE):
        tick, sqrtP = _decode_slot0(ret)
        return int(tick), int(sqrtP)
    elif proto == DexProtocol.ALGEBRA:
        tick, price_raw = _decode_globalState(ret)
        return int(tick), int(price_raw)
    else:
        raise NoSuchDexProtocolException(f"Unsupported dex_protocol: {proto}")


class Web3Utils(BaseWeb3Utils):
    """
    Web3 유틸리티 클래스
    """

    @staticmethod
    async def get_slot0_many(
        web3ctx: Web3Ctx,
        items: List[PoolItem],  # [(pool_address, dex_protocol), ...]
        batch_size: int = 500,
    ) -> Dict[str, Tuple[int, int]]:
        """
        여러 풀의 상태를 멀티콜로 조회해 디코딩하여 반환.
        반환: { pool_address(checksum): (tick, extra) }
        - Uni/Pancake: extra = sqrtPriceX96
        - Algebra:     extra = price_raw
        실패한 풀은 맵에서 제외.
        """
        if not items:
            return {}

        multicall: AsyncContract = await Web3Utils.get_multicall(web3ctx)

        out: Dict[str, Tuple[int, int]] = {}

        for i in range(0, len(items), batch_size):
            chunk = items[i : i + batch_size]

            calls = []
            meta: List[Tuple[str, DexProtocol]] = []
            for addr, proto in chunk:
                a = AsyncWeb3.to_checksum_address(addr)
                calls.append({"target": a, "callData": _encode_state_call(proto)})
                meta.append((a, proto))

            # 실패해도 계속 진행 (requireSuccess=False)
            results = await multicall.functions.tryAggregate(False, calls).call()

            for (a, proto), (success, ret) in zip(meta, results):
                if not success or not ret:
                    continue
                try:
                    tick, extra = _decode_state(proto, ret)
                    out[a] = (tick, extra)
                except Exception:
                    # 디코딩 실패는 스킵
                    continue

        return out
