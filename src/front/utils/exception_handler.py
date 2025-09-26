from typing import TYPE_CHECKING
from telegram.ext import ContextTypes, ConversationHandler
from hypurrquant.api.exception import BaseOrderException
from hypurrquant.logging_config import configure_logging, coroutine_id
from .utils import send_or_edit
from pydantic import ValidationError
import traceback

logger = configure_logging(__name__)


async def exception_error_handler(
    update: object, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Log the error and send a telegram message to notify the developer."""

    # 에러 메시지 및 로그 아이디 추출
    exc_info = context.error
    cor_id = coroutine_id.get()
    short_id = cor_id[-8:]  # 마지막 8자리만 사용\
    if isinstance(exc_info, ValidationError):
        logger.debug("ValidationError")
        stack_trace = "".join(
            traceback.format_exception(type(exc_info), exc_info, exc_info.__traceback__)
        )
        await send_or_edit(
            update,
            context,
            f"Something went wrong. Please contact our support team with the following error ID: `{short_id}`",
            parse_mode="Markdown",
        )
        logger.exception(
            stack_trace,
        )

    elif isinstance(exc_info, ValueError):
        logger.debug("ValueError")
        stack_trace = "".join(
            traceback.format_exception(type(exc_info), exc_info, exc_info.__traceback__)
        )
        logger.exception(
            stack_trace,
        )
        await send_or_edit(update, context, str(exc_info))

    else:
        logger.debug("Exception")
        stack_trace = "".join(
            traceback.format_exception(type(exc_info), exc_info, exc_info.__traceback__)
        )
        await send_or_edit(
            update,
            context,
            f"Something went wrong. Please contact our support team with the following error ID: `{short_id}`",
            parse_mode="Markdown",
        )
        logger.exception(
            stack_trace,
        )

    return ConversationHandler.END
