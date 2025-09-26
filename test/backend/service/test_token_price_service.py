# tests/test_token_price_service.py
import types
import pytest

from hypurrquant.evm import use_chain, Chain
from backend.lpvault.service.token_price_service import (
    TokenPriceService,
    route_to_json,
    route_from_json,
    Edge,
    Route,
    PoolSpec,
)


class DummyCtx:
    def __init__(self, chain, chain_id):
        self.chain = chain
        self.chain_id = chain_id


@pytest.mark.asyncio
async def test_route_json_roundtrip():
    route = Route(
        edges=[
            Edge(
                pools=[
                    PoolSpec(
                        dex_type="UNI",
                        t0="0xAAA",
                        t1="0xUSDT",
                        fee=3000,
                        address="0xPOOL1",
                    ),
                    PoolSpec(
                        dex_type="UNI",
                        t0="0xAAA",
                        t1="0xUSDT",
                        fee=10000,
                        address="0xPOOL2",
                    ),
                ]
            )
        ]
    )
    s = route_to_json(route)
    rt = route_from_json(s)
    assert isinstance(rt, Route)
    assert len(rt.edges) == 1
    assert len(rt.edges[0].pools) == 2
    assert rt.edges[0].pools[0].address == "0xPOOL1"


@pytest.mark.asyncio
async def test_get_token_price_in_usd_with_real_web3(monkeypatch):
    """
    Web3 관련 호출(멀티콜/slot0/batch_lookup_pools)은 실제 구현 사용.
    단, 빈 문자열 체크섬(USDT_ADDRESS 생성)만 안전하게 처리.
    """
    from hypurrquant.evm.constants._hyperliquid.token_address import (
        UBTC_ADDRESS,
        WHYPE_ADDRESS,
    )
    from backend.constants import get_dex_configs

    dex_configs = get_dex_configs(Chain.HYPERLIQUID)
    dex_types = [dc.dex.name for dc in dex_configs]

    svc = TokenPriceService()

    async with use_chain(Chain.HYPERLIQUID) as web3ctx:
        result = await svc.get_token_price_in_usd(
            web3ctx, [UBTC_ADDRESS, WHYPE_ADDRESS], dex_types=dex_types
        )
        print(result)
