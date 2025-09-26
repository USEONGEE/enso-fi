from hypurrquant.db import init_db, close_db
from hypurrquant.logging_config import configure_logging
from telegram.warnings import PTBUserWarning
from telegram import BotCommand
from telegram.ext import (
    Application,
    PicklePersistence,
)
from backend.account.repository.dependencies import (
    get_account_repository,
    AccountRepository,
)
from front.command import Command
from front.utils.exception_handler import exception_error_handler
from warnings import filterwarnings
import asyncio
import logging
import os

# Disable httpx _logger completely
logging.getLogger("httpx").disabled = True

filterwarnings(
    action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning
)

_logger = configure_logging(__name__)


bot_token = os.getenv("BOT_TOKEN")
profile = os.getenv("PROFILE", "dev")  # 기본값 dev

_logger.info(f"bot_token: {bot_token}")


# PicklePersistence (dev 용)
persistence_dev = PicklePersistence("bot_data.pickle")


async def common(application: Application) -> None:
    # 명령어 메뉴 설정

    from front.start.start import start_handler
    from front.wallet.wallet import wallet_handler
    from front.lend.lend import lend_handler

    commands = [
        BotCommand(Command.START, "Start the bot"),
    ]
    await application.bot.set_my_commands(commands)

    # 핸들러 등록
    application.add_handler(start_handler)
    application.add_handler(wallet_handler)
    application.add_handler(lend_handler)
    application.add_error_handler(exception_error_handler)


async def start_app_polling(application: Application) -> None:
    """
    Polling 방식으로 봇을 실행 (dev용).
    """
    await common(application)
    # 앱 시작
    await application.initialize()
    await application.start()
    try:
        # Polling 시작
        await application.updater.start_polling()
        # 무기한 대기
        await asyncio.Event().wait()
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()


async def main_async():

    init_db()
    # index 생성
    repo = get_account_repository()
    await repo.create_indexes()
    try:
        # task = asyncio.create_task(
        #     consumer.run(20)
        # )  # FIXME 몇 초에 한 번씩 실행할 건지 수정해야함.

        application = (
            Application.builder().token(bot_token).persistence(persistence_dev).build()
        )

        _logger.debug("dev profile")
        try:
            await start_app_polling(application)
        finally:
            pass
            # task.cancel()
            # try:
            #     await task
            # except asyncio.CancelledError:
            #     logging.info("Periodic task cancelled.")
    except Exception as e:
        _logger.exception(f"Error in main_async: {e}")
    finally:
        await close_db()


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
