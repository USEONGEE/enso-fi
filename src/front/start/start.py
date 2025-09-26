from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    ContextTypes,
)
from hypurrquant.models.account import Account
from hypurrquant.logging_config import (
    configure_logging,
    force_coroutine_logging,
)
from hypurrquant.evm import Chain
from .states import StartStates
from .settings import FirstRegisterSetting
from front.utils.utils import send_or_edit
from front.command import Command
from front.utils.account_helpers import fetch_account_manager
from front.utils.account_manager import AccountManager

logger = configure_logging(__name__)


def _register_message() -> str:
    return "Type message"


@force_coroutine_logging
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"triggerred by user: {context._user_id}")
    account_manager: AccountManager = await fetch_account_manager(context)
    account: Account = await account_manager.get_active_account(force=True)

    message = f"your account: {account.public_key}\n"
    kb = [
        [
            InlineKeyboardButton(
                "lend", callback_data=f"{StartStates.START.value}:{Command.LEND}"
            ),
            InlineKeyboardButton(
                "⚙️ Wallet", callback_data=f"{StartStates.START.value}:{Command.WALLET}"
            ),
        ],
    ]

    await send_or_edit(
        update,
        context,
        message,
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown",
    )

    return StartStates.START


start_handler = CommandHandler(Command.START, start)
