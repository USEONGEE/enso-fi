from hypurrquant.evm.constants.chain import *
from hypurrquant.evm.constants._hyperliquid import (
    token_address as hyperliquid_token_address,
)
from hypurrquant.evm.constants import *
from ._hyperliquid import dex as hyperliquid_dex
from ._hyperliquid import pool_config as hyperliquid_pool_config
from .types import *

from typing import List, Dict


# =====================
# Dex 전용 메서드
# =====================
def get_pool_config_types(chain: Chain, dex_type: str) -> List[PoolConfigType]:
    """
    주어진 체인에 해당하는 풀 설정을 반환합니다.
    """
    if chain == Chain.HYPERLIQUID:
        return hyperliquid_pool_config.get_pool_config_types(dex_type)

    raise ValueError(f"Unknown chain: {chain}")


def get_dex_config(chain: Chain, dex_type: str) -> DexConfig:
    if chain == Chain.HYPERLIQUID:
        return hyperliquid_dex.get_dex_config(dex_type)

    raise ValueError(f"Unknown chain: {chain}")


def get_all_dex_types(chain: Chain) -> List[str]:
    if chain == Chain.HYPERLIQUID:
        return [
            dex_config.dex.name
            for dex_config in hyperliquid_dex.HYPERLIQUID_DEX_CONFIGS.values()
        ]

    raise ValueError(f"Unknown chain: {chain}")


def get_dex_configs(chain: Chain) -> List[DexConfig]:
    if chain == Chain.HYPERLIQUID:
        return list(hyperliquid_dex.HYPERLIQUID_DEX_CONFIGS.values())

    raise ValueError(f"Unknown chain: {chain}")


def get_all_pool_config_types() -> Dict[Chain, List[PoolConfigType]]:
    return {
        Chain.HYPERLIQUID: hyperliquid_pool_config.pool_configs,
    }
