from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from hypurrquant.logging_config import (
    configure_logging,
    force_coroutine_logging,
)
from .settings import WalletSetting
from ..utils.account_helpers import fetch_account_manager
from ..utils.account_manager import AccountManager
from ..utils.utils import answer, send_or_edit
from ..utils.cancel import (
    create_cancel_inline_button,
    initialize_handler,
)
from .states import LendState
from backend.lend.service.service import (
    LendService,
    TokenInfo,
    TokenAsset,
    PortfolioItem,
)

from ..command import Command
import asyncio

logger = configure_logging(__name__)
service = LendService()


# ================================
# 지갑 조회
# ================================
@force_coroutine_logging
@initialize_handler(setting_cls=WalletSetting)
async def lend_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"triggerred by user: {context._user_id}")
    await answer(update)

    # 1. wallet 목록 조회
    account_holder: AccountManager = await fetch_account_manager(context)
    items: list[PortfolioItem] = await service.get_user_portfolio_for_project(
        account_holder.active_account.public_key
    )
    msg = "your lending portfolio:\n\n"
    for item in items:
        token = item.asset.symbol  # or name
        supply_apy = item.rate.supply_apy
        borrow_apy = item.rate.borrow_apy
        protocol = "Hyperlend"
        quantity = item.quantity
        value = item.value

        msg += (
            f"Token: {token}\n"
            f"Protocol: {protocol}\n"
            f"Quantity: {quantity}\n"
            f"Value (USD): {value:.2f}\n"
            f"Supply APY: {supply_apy:.2f}%\n"
            f"Borrow APY: {borrow_apy:.2f}%\n"
            "-----------------------\n"
        )

    await send_or_edit(
        update,
        context,
        msg,
        reply_markup=InlineKeyboardMarkup(
            [[create_cancel_inline_button(Command.START)]]
        ),
    )
    return LendState.SELECT_ACTION
