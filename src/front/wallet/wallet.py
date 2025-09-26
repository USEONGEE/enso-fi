from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from ..command import Command
from .wallet_change import wallet_change_start, change_state
from .wallet_delete import wallet_delete_start, delete_state
from .wallet_create import wallet_create_start, create_states
from .wallet_import import wallet_import_start, import_state
from .wallet_export import wallet_export_start
from .wallet_start import wallet_start
from .states import WalletState
from ..utils.cancel import cancel_handler
from ..start.states import StartStates

# ================================
# ConversationHandler 등록
# ===============================
wallet_handler = ConversationHandler(
    entry_points=[
        CommandHandler(Command.WALLET, wallet_start),
        CallbackQueryHandler(
            wallet_start,
            pattern=rf"^{StartStates.START.value}:{Command.WALLET}",
        ),
    ],
    states={
        WalletState.SELECT_ACTION: [
            CallbackQueryHandler(wallet_change_start, pattern="^wallet_change"),
            CallbackQueryHandler(wallet_delete_start, pattern="^wallet_delete"),
            CallbackQueryHandler(wallet_create_start, pattern="^wallet_create"),
            CallbackQueryHandler(wallet_import_start, pattern="^wallet_import"),
            CallbackQueryHandler(wallet_export_start, pattern="^wallet_export"),
        ],
        **change_state,
        **create_states,
        **import_state,
        **delete_state,
    },
    fallbacks=[cancel_handler],
    name=Command.WALLET,
    allow_reentry=True,
)
