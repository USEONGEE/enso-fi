from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from ..command import Command
from .states import LendState
from .lend_start import lend_start
from ..utils.cancel import cancel_handler
from ..start.states import StartStates

# ================================
# ConversationHandler 등록
# ================================
lend_handler = ConversationHandler(
    entry_points=[
        CommandHandler(Command.LEND, lend_start),
        CallbackQueryHandler(
            lend_start,
            pattern=rf"^{StartStates.START.value}:{Command.LEND}",
        ),
    ],
    states={},
    fallbacks=[cancel_handler],
    name=Command.LEND,
    allow_reentry=True,
)
