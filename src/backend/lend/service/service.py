from __future__ import annotations
from hypurrquant.api.async_http import send_request_for_external
from hypurrquant.utils.singleton import singleton


from dataclasses import dataclass
from decimal import Decimal, getcontext
from typing import Optional, Any, Dict, List

# 필요 시 정밀도 조정 (토큰 수량 계산에 충분하도록)
getcontext().prec = 50


@dataclass(frozen=True)
class TokenAsset:
    token: str  # 컨트랙트 주소 (또는 네이티브 토큰 마커)
    amount_wei: int  # 원문 amount를 정수로 (wei/최소단위)
    chain_id: int  # 체인 ID
    decimals: int  # 토큰 소수 자리수
    price: Decimal  # 1개당 가격 (법정화폐 or 기준 통화)
    name: str  # 토큰 이름
    symbol: str  # 토큰 심볼
    logo_uri: Optional[str] = None  # 로고 URL (없을 수 있음)

    @property
    def quantity(self) -> Decimal:
        """
        사람이 읽는 수량 = amount_wei / (10 ** decimals)
        """
        if self.decimals < 0:
            raise ValueError("decimals must be >= 0")
        scale = Decimal(10) ** self.decimals
        return Decimal(self.amount_wei) / scale

    @property
    def value(self) -> Decimal:
        """
        총 평가금액 = quantity * price
        """
        return (self.quantity * self.price).quantize(
            Decimal("1.0000000000")
        )  # 소수 10자리로 예시 반올림

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TokenAsset":
        """
        주어진 dict 한 건을 TokenAsset으로 변환
        - amount는 문자열일 수 있으므로 int로 변환
        - price는 float일 수 있으므로 Decimal로 변환
        - 키 이름을 파이썬 스타일로 맞춰 매핑
        """
        return TokenAsset(
            token=d["token"],
            amount_wei=int(d["amount"]),
            chain_id=int(d["chainId"]),
            decimals=int(d["decimals"]),
            price=Decimal(str(d.get("price", 0))),
            name=d["name"],
            symbol=d["symbol"],
            logo_uri=d.get("logoUri"),
        )


def _to_float(x: Any) -> Optional[float]:
    # None, "None", "" 등을 안전하게 처리
    if x is None or x == "" or x == "None":
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


@dataclass(frozen=True)
class UnderlyingToken:
    address: str
    chain_id: int
    type: str
    decimals: int
    name: str
    symbol: str
    logos_uri: List[str]


@dataclass(frozen=True)
class TokenInfo:
    chain_id: int
    address: str
    decimals: int
    name: str
    symbol: str
    logos_uri: List[str]
    type: str
    project: str
    protocol: str
    underlying_tokens: List[UnderlyingToken]
    primary_address: Optional[str]
    apy: Optional[float]  # supply apy
    apy_base: Optional[float]
    apy_reward: Optional[str]
    tvl: Optional[float]

    @staticmethod
    def from_dict(d: dict) -> "TokenInfo":
        def _logos_list(v) -> List[str]:
            if v is None:
                return []
            if isinstance(v, list):
                return [str(x) for x in v]
            return [str(v)]

        return TokenInfo(
            chain_id=int(d["chainId"]),
            address=d["address"],
            decimals=int(d["decimals"]),
            name=d["name"],
            symbol=d["symbol"],
            logos_uri=_logos_list(d.get("logosUri")),
            type=d["type"],
            project=d["project"],
            protocol=d["protocol"],
            underlying_tokens=[
                UnderlyingToken(
                    address=ut["address"],
                    chain_id=int(ut["chainId"]),
                    type=ut["type"],
                    decimals=int(ut["decimals"]),
                    name=ut["name"],
                    symbol=ut["symbol"],
                    logos_uri=_logos_list(ut.get("logosUri")),
                )
                for ut in (d.get("underlyingTokens") or [])
            ],
            primary_address=d.get("primaryAddress"),
            apy=_to_float(d.get("apy")),
            apy_base=_to_float(d.get("apyBase")),
            apy_reward=(
                None
                if d.get("apyReward") in (None, "None", "")
                else str(d.get("apyReward"))
            ),
            tvl=_to_float(d.get("tvl")),
        )


@dataclass(frozen=True)
class PortfolioItem:
    info: TokenInfo  # 프로토콜 메타 (TokenInfo)
    asset: TokenAsset  # 사용자 보유 (TokenAsset)
    rate: Optional[RateInfo]  # 대출 금리 정보 (RateInfo) - 매칭 없을 수 있어 Optional
    quantity: Decimal  # 사람이 읽는 수량 (asset.quantity 캐시)
    value: Decimal  # 평가액 (asset.value 캐시)


def _norm_addr(addr: str) -> str:
    # 주소 비교용 정규화 (0x + 소문자)
    return (addr or "").lower()


@dataclass(frozen=True)
class RateInfo:
    address: str
    supply_apr: float
    supply_apy: float
    borrow_apr: float
    borrow_apy: float
    underlying: Optional[str] = None
    collateral: Optional[str] = None

    @staticmethod
    def from_dict(address: str, d: Dict[str, Any]) -> "RateInfo":
        return RateInfo(
            address=address,
            supply_apr=float(d.get("supplyAPR", 0)),
            supply_apy=float(d.get("supplyAPY", 0)),
            borrow_apr=float(d.get("borrowAPR", 0)),
            borrow_apy=float(d.get("borrowAPY", 0)),
            underlying=d.get("underlying"),
            collateral=d.get("collateral"),
        )


@singleton
class LendService:
    async def get_supply_data(self, address: str) -> list[TokenAsset]:
        data = await send_request_for_external(
            "GET",
            f"https://api.enso.finance/api/v1/wallet/balances",
            params={
                "chainId": 999,
                "eoaAddress": address,
                "useEoa": "true",
            },
            headers={
                "Authorization": "Bearer 1e02632d-6feb-4a75-a157-documentation",
                "accept": "application/json",
            },
        )
        return [TokenAsset.from_dict(i) for i in data]

    async def get_tokens(
        self, project: str = "hyperlend"
    ) -> dict:  # hypurrfi, hyperlend

        data = await send_request_for_external(
            "GET",
            f"https://api.enso.finance/api/v1/tokens",
            params={
                "project": project,
                "chainId": 999,
                "type": "defi",
                "page": 1,
                "pageSize": 100,
                "cursor": "1233456",
                "includeMetadata": "true",
                "includeUnderlying": "true",
            },
            headers={
                "Authorization": "Bearer 1e02632d-6feb-4a75-a157-documentation",
                "accept": "application/json",
            },
        )
        data = data["data"]
        return [TokenInfo.from_dict(i) for i in data]

    async def get_tokens_borrow_info(self, project: str) -> dict:
        url = "https://api.hyperlend.finance/data/markets/rates?chain=hyperEvm"
        data = await send_request_for_external("GET", url)
        rates = {
            addr.lower(): RateInfo.from_dict(addr, data) for addr, data in data.items()
        }
        return rates

    async def get_user_portfolio_for_project(self, address: str) -> List[PortfolioItem]:
        """
        1) 프로젝트 토큰 목록(TokenInfo) 조회
        2) 사용자 보유 목록(TokenAsset) 조회
        3) address 기준으로 매칭해서 포함되는 것만 반환
        4) TokenInfo의 underlying_tokens 주소를 rates 키(소문자)와 비교해 매칭되면 RateInfo를 포함
        """
        tokens: List[TokenInfo] = await self.get_tokens()
        assets: List[TokenAsset] = await self.get_supply_data(address)
        rates: Dict[str, RateInfo] = await self.get_tokens_borrow_info(
            "hyperlend"
        )  # 키는 이미 lower

        # TokenInfo 주소 인덱스 (소문자)
        info_by_addr: Dict[str, TokenInfo] = {_norm_addr(t.address): t for t in tokens}

        portfolio: List[PortfolioItem] = []
        for a in assets:
            key = _norm_addr(a.token)
            if (
                key == "0x747d0d4ba0a2083651513cd008deb95075683e82"  # WHYPE BORROW
                or key == "0x1ef897622d62335e7fc88fb0605fbba28ec0b01d"  # USDT BORROW
            ):
                if key == "0x747d0d4ba0a2083651513cd008deb95075683e82":
                    info = info_by_addr.get(
                        "0x0d745eaa9e70bb8b6e2a0317f85f1d536616bd34"
                    )  # WHYPE SUPPLY
                else:
                    info = info_by_addr.get(
                        "0x10982ad645D5A112606534d8567418Cf64c14cB5"
                    )  # USDT SUPPLY
            else:
                info = info_by_addr.get(key)
                if info is None:
                    continue  # 프로젝트 토큰 목록에 없는 자산은 스킵

            # underlying 주소들 중 rates에 존재하는 첫 항목을 사용
            matched_rate: Optional[RateInfo] = None
            for ut in info.underlying_tokens:
                ut_addr_l = _norm_addr(ut.address)
                r = rates.get(ut_addr_l)
                if r is not None:
                    matched_rate = r
                    break

            portfolio.append(
                PortfolioItem(
                    info=info,
                    asset=a,
                    rate=matched_rate,
                    quantity=a.quantity,
                    value=a.value,
                )
            )
        return portfolio


# ---- 사용 예시 ----
if __name__ == "__main__":
    import asyncio

    async def main():
        service = LendService()
        project = "hyperlend"
        user_addr = "0xCb0f40FfA2285fb88Dd970cc4632cf27fcB88ee5"

        # 포함 여부만 확인 (포트폴리오 추림)
        portfolio = await service.get_supply_data(user_addr)

        # 보기 좋게 출력
        for p in portfolio:
            print(p)

    asyncio.run(main())
