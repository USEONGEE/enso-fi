from __future__ import annotations

from typing import Dict, Optional

from ..types import DexConfig, Dex, Ve33, DexProtocol, CommonContractAddress
from hypurrquant.evm.constants._hyperliquid.token_address import *


def _cfg(
    *,
    name: str,
    protocol: DexProtocol,
    npm: str,
    clf: str,
    ve33: Optional[Ve33] = None,
) -> DexConfig:
    return DexConfig(
        dex=Dex(name=name, protocol=protocol),
        common_contract=CommonContractAddress(
            nft_position_manager=npm,
            cl_factory=clf,
        ),
        ve33=ve33,
    )


_hybra = "HYBRA"
_hyperswap = "HYPERSWAP"
_prjx = "PRJX"
_gliquid = "GLIQUID"
_kitten = "KITTEN"
_upheaval = "UPHEAVAL"
_ultrasolid = "ULTRASOLID"

# DEX별 설정 집합
HYPERLIQUID_DEX_CONFIGS: Dict[str, DexConfig] = {
    # ====================
    # Non ve33
    # ====================
    _hybra: _cfg(
        name=_hybra,
        protocol=DexProtocol.UNISWAP,
        npm="0x934C4f47B2D3FfcA0156A45DEb3A436202aF1efa",
        clf="0x2dC0Ec0F0db8bAF250eCccF268D7dFbF59346E5E",
        ve33=None,
    ),
    _hyperswap: _cfg(
        name=_hyperswap,
        protocol=DexProtocol.UNISWAP,
        npm="0x6eDA206207c09e5428F281761DdC0D300851fBC8",
        clf="0xB1c0fa0B789320044A6F623cFe5eBda9562602E3",
        ve33=None,
    ),
    _prjx: _cfg(
        name=_prjx,
        protocol=DexProtocol.UNISWAP,
        npm="0xeaD19AE861c29bBb2101E834922B2FEee69B9091",
        clf="0xFf7B3e8C00e57ea31477c32A5B52a58Eea47b072",
        ve33=None,
    ),
    _gliquid: _cfg(
        name=_gliquid,
        protocol=DexProtocol.ALGEBRA,
        npm="0x69D57B9D705eaD73a5d2f2476C30c55bD755cc2F",
        clf="0x10253594A832f967994b44f33411940533302ACb",
    ),
    _upheaval: _cfg(
        name=_upheaval,
        protocol=DexProtocol.PANCAKE,
        npm="0xC8352A2EbA29F4d9BD4221c07D3461BaCc779088",
        clf="0x2566163ea012C9E67c1C7080e0a073f20B548030",
        ve33=None,
    ),
    _ultrasolid: _cfg(
        name=_ultrasolid,
        protocol=DexProtocol.UNISWAP,
        npm="0xE7ffA0ee20Deb1613489556062Fa8cec690C3c02",
        clf="0xD883a0B7889475d362CEA8fDf588266a3da554A1",
        ve33=None,
    ),
    # ====================
    # ve33
    # ====================
    _kitten: _cfg(
        name=_kitten,
        protocol=DexProtocol.ALGEBRA,
        npm="0x9ea4459c8DefBF561495d95414b9CF1E2242a3E2",
        clf="0x5f95E92c338e6453111Fc55ee66D4AafccE661A7",
        ve33=Ve33(
            gov_token_address=KITTEN_ADDRESS,
            farm_center="0x211BD8917d433B7cC1F4497AbA906554Ab6ee479",
        ),
    ),
}


def get_dex_config(dex_type: str) -> DexConfig:
    try:
        return HYPERLIQUID_DEX_CONFIGS[dex_type]
    except KeyError:
        available = ", ".join(HYPERLIQUID_DEX_CONFIGS.keys())
        raise KeyError(f"Unknown dex_type: {dex_type}. Available: {available}")
