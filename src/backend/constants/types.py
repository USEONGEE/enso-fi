from hypurrquant.evm.constants.types import *
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field


class DexProtocol(str, Enum):
    UNISWAP = "UNISWAP"
    ALGEBRA = "ALGEBRA"
    PANCAKE = "PANCAKE"


class Ve33(BaseModel):
    gov_token_address: str = Field(..., description="Governance token address")
    farm_center: str = Field(..., description="Farm center contract address")


class Dex(BaseModel):
    name: str = Field(..., description="Name of the DEX. dex_type으로 사용됨")
    protocol: DexProtocol = Field(..., description="Protocol used by the DEX")


class CommonContractAddress(BaseModel):
    nft_position_manager: str = Field(..., description="NFT position manager address")
    cl_factory: str = Field(..., description="CL factory contract address")


class DexConfig(BaseModel):
    dex: Dex
    common_contract: CommonContractAddress
    ve33: Optional[
        Ve33
    ]  # NOTE: ve33이 존재하는 경우 farm 로직이 수행될 수 있음. 해당 플랫폼에서 이를 지원하는지를 등록 전에 파악해야함.


class PoolConfigType(BaseModel):
    dex_type: str = Field(..., description="DEX 이름")
    pool_name: str  # / 를 기준으로 token0, token1 구분
    token0: str
    token1: str
    fee: Optional[int]
    pcts: List[float]
