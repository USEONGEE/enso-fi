from hypurrquant.exception import NoSuchDexException
from hypurrquant.evm.constants._hyperliquid.token_address import *
from .dex import _hybra, _hyperswap, _prjx, _gliquid, _kitten, _upheaval
from ..types import PoolConfigType
from typing import List


###################################
# WHYPE/USDT0
###################################
WHYPE_USDT0_HYPERSWAP = PoolConfigType(
    dex_type=_hyperswap,
    pool_name=f"WHYPE/USDT0",
    token0=WHYPE_ADDRESS,
    token1=USDT0_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_USDT0_HYBRA = PoolConfigType(
    dex_type=_hybra,
    pool_name="WHYPE/USDT0",
    token0=WHYPE_ADDRESS,
    token1=USDT0_ADDRESS,
    fee=2500,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_USDT0_PRJX = PoolConfigType(
    dex_type=_prjx,
    pool_name="WHYPE/USDT0",
    token0=WHYPE_ADDRESS,
    token1=USDT0_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_USDT0_GLIQUID = PoolConfigType(
    dex_type=_gliquid,
    pool_name="WHYPE/USDT0",
    token0=WHYPE_ADDRESS,
    token1=USDT0_ADDRESS,
    fee=None,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_USDT0_KITTEN = PoolConfigType(
    dex_type=_kitten,
    pool_name="WHYPE/USDT0",
    token0=WHYPE_ADDRESS,
    token1=USDT0_ADDRESS,
    fee=None,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_USDT0_UPHEAVAL = PoolConfigType(
    dex_type=_upheaval,
    pool_name="WHYPE/USDT0",
    token0=WHYPE_ADDRESS,
    token1=USDT0_ADDRESS,
    fee=2500,
    pcts=[0.5, 1, 2, 3, 4, 5],
)
###################################
# WHYPE/USDHL
###################################

WHYPE_USDHL_HYPERSWAP = PoolConfigType(
    dex_type=_hyperswap,
    pool_name="WHYPE/USDHL",
    token0=WHYPE_ADDRESS,
    token1=USDHL_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_USDHL_HYBRA = PoolConfigType(
    dex_type=_hybra,
    pool_name="WHYPE/USDHL",
    token0=WHYPE_ADDRESS,
    token1=USDHL_ADDRESS,
    fee=2500,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_USDHL_PRJX = PoolConfigType(
    dex_type=_prjx,
    pool_name="WHYPE/USDHL",
    token0=WHYPE_ADDRESS,
    token1=USDHL_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_USDHL_GLIQUID = PoolConfigType(
    dex_type=_gliquid,
    pool_name="WHYPE/USDHL",
    token0=WHYPE_ADDRESS,
    token1=USDHL_ADDRESS,
    fee=None,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_USDHL_KITTEN = PoolConfigType(
    dex_type=_kitten,
    pool_name="WHYPE/USDHL",
    token0=WHYPE_ADDRESS,
    token1=USDHL_ADDRESS,
    fee=None,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

###################################
# WHYPE/LHYPE
###################################

WHYPE_LHYPE_HYPERSWAP = PoolConfigType(
    dex_type=_hyperswap,
    pool_name="WHYPE/LHYPE",
    token0=WHYPE_ADDRESS,
    token1=LHYPE_ADDRESS,
    fee=100,
    pcts=[0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5, 10],
)


WHYPE_LHYPE_HYBRA = PoolConfigType(
    dex_type=_hybra,
    pool_name="WHYPE/LHYPE",
    token0=WHYPE_ADDRESS,
    token1=LHYPE_ADDRESS,
    fee=200,
    pcts=[0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5, 10],
)

WHYPE_LHYPE_PRJX = PoolConfigType(
    dex_type=_prjx,
    pool_name="WHYPE/LHYPE",
    token0=WHYPE_ADDRESS,
    token1=LHYPE_ADDRESS,
    fee=100,
    pcts=[0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5, 10],
)

WHYPE_LHYPE_GLIQUID = PoolConfigType(
    dex_type=_gliquid,
    pool_name="WHYPE/LHYPE",
    token0=WHYPE_ADDRESS,
    token1=LHYPE_ADDRESS,
    fee=None,
    pcts=[0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5, 10],
)

WHYPE_LHYPE_KITTEN = PoolConfigType(
    dex_type=_kitten,
    pool_name="WHYPE/LHYPE",
    token0=WHYPE_ADDRESS,
    token1=LHYPE_ADDRESS,
    fee=None,
    pcts=[0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5, 10],
)
###################################
# WHYPE/KHYPE
###################################

WHYPE_KHYPE_HYPERSWAP = PoolConfigType(
    dex_type=_hyperswap,
    pool_name="WHYPE/KHYPE",
    token0=WHYPE_ADDRESS,
    token1=KHYPE_ADDRESS,
    fee=100,
    pcts=[0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5, 10],
)


WHYPE_KHYPE_HYBRA = PoolConfigType(
    dex_type=_hybra,
    pool_name="WHYPE/KHYPE",
    token0=WHYPE_ADDRESS,
    token1=KHYPE_ADDRESS,
    fee=200,
    pcts=[0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5, 10],
)


WHYPE_KHYPE_PRJX = PoolConfigType(
    dex_type=_prjx,
    pool_name="WHYPE/KHYPE",
    token0=WHYPE_ADDRESS,
    token1=KHYPE_ADDRESS,
    fee=100,
    pcts=[0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5, 10],
)

WHYPE_KHYPE_GLIQUID = PoolConfigType(
    dex_type=_gliquid,
    pool_name="WHYPE/KHYPE",
    token0=WHYPE_ADDRESS,
    token1=KHYPE_ADDRESS,
    fee=None,
    pcts=[0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5, 10],
)

WHYPE_KHYPE_KITTEN = PoolConfigType(
    dex_type=_kitten,
    pool_name="WHYPE/KHYPE",
    token0=WHYPE_ADDRESS,
    token1=KHYPE_ADDRESS,
    fee=None,
    pcts=[0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5, 10],
)

WHYPE_KHYPE_UPHEAVAL = PoolConfigType(
    dex_type=_upheaval,
    pool_name="WHYPE/KHYPE",
    token0=WHYPE_ADDRESS,
    token1=KHYPE_ADDRESS,
    fee=100,
    pcts=[0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5, 10],
)
###################################
# USDT0/KHYPE
###################################

KHYPE_USDT0_HYPERSWAP = PoolConfigType(
    dex_type=_hyperswap,
    pool_name="USDT0/KHYPE",
    token0=USDT0_ADDRESS,
    token1=KHYPE_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

KHYPE_USDT0_HYBRA = PoolConfigType(
    dex_type=_hybra,
    pool_name="USDT0/KHYPE",
    token0=USDT0_ADDRESS,
    token1=KHYPE_ADDRESS,
    fee=2500,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

KHYPE_USDT0_PRJX = PoolConfigType(
    dex_type=_prjx,
    pool_name="USDT0/KHYPE",
    token0=USDT0_ADDRESS,
    token1=KHYPE_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

KHYPE_USDT0_KITTEN = PoolConfigType(
    dex_type=_kitten,
    pool_name="USDT0/KHYPE",
    token0=USDT0_ADDRESS,
    token1=KHYPE_ADDRESS,
    fee=None,
    pcts=[0.5, 1, 2, 3, 4, 5],
)


###################################
# WHYPE/UBTC
###################################

WHYPE_UBTC_HYPERSWAP = PoolConfigType(
    dex_type=_hyperswap,
    pool_name="WHYPE/UBTC",
    token0=WHYPE_ADDRESS,
    token1=UBTC_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_UBTC_HYBRA = PoolConfigType(
    dex_type=_hybra,
    pool_name="WHYPE/UBTC",
    token0=WHYPE_ADDRESS,
    token1=UBTC_ADDRESS,
    fee=2500,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_UBTC_PRJX = PoolConfigType(
    dex_type=_prjx,
    pool_name="WHYPE/UBTC",
    token0=WHYPE_ADDRESS,
    token1=UBTC_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_UBTC_GLIQUID = PoolConfigType(
    dex_type=_gliquid,
    pool_name="WHYPE/UBTC",
    token0=WHYPE_ADDRESS,
    token1=UBTC_ADDRESS,
    fee=None,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_UBTC_KITTEN = PoolConfigType(
    dex_type=_kitten,
    pool_name="WHYPE/UBTC",
    token0=WHYPE_ADDRESS,
    token1=UBTC_ADDRESS,
    fee=None,
    pcts=[0.5, 1, 2, 3, 4, 5],
)
###################################
# WHYPE/UETH
###################################

WHYPE_UETH_HYPERSWAP = PoolConfigType(
    dex_type=_hyperswap,
    pool_name="WHYPE/UETH",
    token0=WHYPE_ADDRESS,
    token1=UETH_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_UETH_HYBRA = PoolConfigType(
    dex_type=_hybra,
    pool_name="WHYPE/UETH",
    token0=WHYPE_ADDRESS,
    token1=UETH_ADDRESS,
    fee=2500,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_UETH_PRJX = PoolConfigType(
    dex_type=_prjx,
    pool_name="WHYPE/UETH",
    token0=WHYPE_ADDRESS,
    token1=UETH_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_UETH_GLIQUID = PoolConfigType(
    dex_type=_gliquid,
    pool_name="WHYPE/UETH",
    token0=WHYPE_ADDRESS,
    token1=UETH_ADDRESS,
    fee=None,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_UETH_KITTEN = PoolConfigType(
    dex_type=_kitten,
    pool_name="WHYPE/UETH",
    token0=WHYPE_ADDRESS,
    token1=UETH_ADDRESS,
    fee=None,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

###################################
# UPUMP/WHYPE -> 해결됨
###################################

WHYPE_UPUMP_HYPERSWAP = PoolConfigType(
    dex_type=_hyperswap,
    pool_name="UPUMP/WHYPE",
    token0=UPUMP_ADDRESS,
    token1=WHYPE_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_UPUMP_HYBRA = PoolConfigType(
    dex_type=_hybra,
    pool_name="UPUMP/WHYPE",
    token0=UPUMP_ADDRESS,
    token1=WHYPE_ADDRESS,
    fee=2500,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

WHYPE_UPUMP_PRJX = PoolConfigType(
    dex_type=_prjx,
    pool_name="UPUMP/WHYPE",
    token0=UPUMP_ADDRESS,
    token1=WHYPE_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)


###################################
# USDT0/HSTR
###################################

USDT0_HSTR_PRJX = PoolConfigType(
    dex_type=_prjx,
    pool_name="USDT0/HSTR",
    token0=USDT0_ADDRESS,
    token1=HSTR_ADDRESS,
    fee=10000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

###################################
# UBTC/KHYPE -> 순서 해결
###################################

KHYPE_UBTC_HYPERSWAP = PoolConfigType(
    dex_type=_hyperswap,
    pool_name="UBTC/KHYPE",
    token0=UBTC_ADDRESS,
    token1=KHYPE_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

KHYPE_UBTC_HYBRA = PoolConfigType(
    dex_type=_hybra,
    pool_name="UBTC/KHYPE",
    token0=UBTC_ADDRESS,
    token1=KHYPE_ADDRESS,
    fee=2500,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

KHYPE_UBTC_PRJX = PoolConfigType(
    dex_type=_prjx,
    pool_name="UBTC/KHYPE",
    token0=UBTC_ADDRESS,
    token1=KHYPE_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)


###################################
# UBTC/UETH
###################################

UBTC_UETH_HYPERSWAP = PoolConfigType(
    dex_type=_hyperswap,
    pool_name="UBTC/UETH",
    token0=UBTC_ADDRESS,
    token1=UETH_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

UBTC_UETH_HYBRA = PoolConfigType(
    dex_type=_hybra,
    pool_name="UBTC/UETH",
    token0=UBTC_ADDRESS,
    token1=UETH_ADDRESS,
    fee=2500,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

UBTC_UETH_PRJX = PoolConfigType(
    dex_type=_prjx,
    pool_name="UBTC/UETH",
    token0=UBTC_ADDRESS,
    token1=UETH_ADDRESS,
    fee=3000,
    pcts=[0.5, 1, 2, 3, 4, 5],
)

###################################

_hyper_swap_configs = [
    WHYPE_USDT0_HYPERSWAP,
    WHYPE_USDHL_HYPERSWAP,
    WHYPE_LHYPE_HYPERSWAP,
    WHYPE_KHYPE_HYPERSWAP,
    WHYPE_UBTC_HYPERSWAP,
    WHYPE_UETH_HYPERSWAP,
    WHYPE_UPUMP_HYPERSWAP,
    KHYPE_USDT0_HYPERSWAP,
    KHYPE_UBTC_HYPERSWAP,
    UBTC_UETH_HYPERSWAP,
]

_prjx_configs = [
    WHYPE_USDT0_PRJX,
    WHYPE_USDHL_PRJX,
    WHYPE_LHYPE_PRJX,
    WHYPE_KHYPE_PRJX,
    WHYPE_UBTC_PRJX,
    WHYPE_UETH_PRJX,
    WHYPE_UPUMP_PRJX,
    KHYPE_USDT0_PRJX,
    KHYPE_UBTC_PRJX,
    UBTC_UETH_PRJX,
    USDT0_HSTR_PRJX,
]

_hybra_configs = [
    WHYPE_USDT0_HYBRA,
    WHYPE_USDHL_HYBRA,
    WHYPE_LHYPE_HYBRA,
    WHYPE_KHYPE_HYBRA,
    WHYPE_UBTC_HYBRA,
    WHYPE_UETH_HYBRA,
    WHYPE_UPUMP_HYBRA,
    KHYPE_USDT0_HYBRA,
    KHYPE_UBTC_HYBRA,
    UBTC_UETH_HYBRA,
]

_gliquid_configs = [
    WHYPE_USDT0_GLIQUID,
    WHYPE_USDHL_GLIQUID,
    WHYPE_LHYPE_GLIQUID,
    WHYPE_KHYPE_GLIQUID,
    WHYPE_UBTC_GLIQUID,
    WHYPE_UETH_GLIQUID,
]

_kitten_configs = [
    WHYPE_USDT0_KITTEN,
    WHYPE_USDHL_KITTEN,
    WHYPE_LHYPE_KITTEN,
    WHYPE_KHYPE_KITTEN,
    WHYPE_UBTC_KITTEN,
    WHYPE_UETH_KITTEN,
    KHYPE_USDT0_KITTEN,
]

_upheaval_configs = [
    WHYPE_USDT0_UPHEAVAL,
    #  WHYPE_KHYPE_UPHEAVAL
]

pool_configs = (
    _hyper_swap_configs
    + _prjx_configs
    + _hybra_configs
    + _gliquid_configs
    + _kitten_configs
    + _upheaval_configs
)


def get_pool_config_types(dex_type: str) -> List[PoolConfigType]:
    """
    DEX 타입에 따라 풀 설정을 반환합니다.
    :param dex_type: DEX 타입 (예: HYBRA, HYPERSWAP, PRJX)
    :return: 해당 DEX 타입의 PoolConfig 객체 리스트
    """

    if dex_type == _hybra:
        return _hybra_configs
    elif dex_type == _prjx:
        return _prjx_configs
    elif dex_type == _gliquid:
        return _gliquid_configs
    elif dex_type == _hyperswap:
        return _hyper_swap_configs
    elif dex_type == _kitten:
        return _kitten_configs
    elif dex_type == _upheaval:
        return _upheaval_configs
    else:
        raise NoSuchDexException(f"Unsupported DEX type: {dex_type}")
