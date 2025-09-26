from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from hypurrquant.logging_config import (
    configure_logging,
    force_coroutine_logging,
)
from .states import WalletState
from .settings import WalletSetting
from ..utils.account_helpers import fetch_account_manager
from ..utils.account_manager import AccountManager
from ..utils.utils import answer, send_or_edit
from ..utils.cancel import (
    create_cancel_inline_button,
    initialize_handler,
)

from ..command import Command
import asyncio

logger = configure_logging(__name__)


# ================================
# 지갑 조회
# ================================
@force_coroutine_logging
@initialize_handler(setting_cls=WalletSetting)
async def wallet_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"triggerred by user: {context._user_id}")
    await answer(update)

    # 1. wallet 목록 조회
    account_holder: AccountManager = await fetch_account_manager(context)
    setting: WalletSetting = WalletSetting.get_setting(context)
    active_account, items = await asyncio.gather(
        account_holder.get_active_account(),
        account_holder.get_all_accounts(),
        return_exceptions=False,  # 예외는 바로 끌어올리기
    )
    # items를 돌면서 nickname이 acitve_account.nickname과 일치하는 것을 추출하고 List에서 제거
    for i in range(len(items) - 1, -1, -1):
        if items[i].nickname == active_account.nickname:
            active_account_item = items.pop(i)

    # 만약 active_account가 없으면 대화 종료
    if not active_account:
        logger.error("No active account found, ending conversation.")
        return ConversationHandler.END

    logger.debug(f"Active account: {active_account.model_dump()}")

    # 메시지 내용
    text = f"✅\[{active_account_item.nickname}] `{active_account_item.public_key}`(tap to copy) \n"

    for item in items:
        text += "\n\n" f"\[{item.nickname}] `{item.public_key}`(tap to copy)\n"

    # 버튼 구성
    keyboard = [
        [
            InlineKeyboardButton("Create Wallet", callback_data="wallet_create"),
            InlineKeyboardButton("Delete Wallet", callback_data="wallet_delete"),
        ],
        [
            InlineKeyboardButton("Import Wallet", callback_data="wallet_import"),
            InlineKeyboardButton("Change Wallet", callback_data="wallet_change"),
        ],
        [
            InlineKeyboardButton("Export Wallet", callback_data="wallet_export"),
        ],
    ]
    keyboard.append([create_cancel_inline_button(setting.return_to)])

    # 메시지 전송
    await send_or_edit(
        update,
        context,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )
    return WalletState.SELECT_ACTION
