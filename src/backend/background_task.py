import asyncio
from hypurrquant.logging_config import configure_logging
from .lpvault.consumers import ExecuteConsumer

_logger = configure_logging(__name__)

execute_consumer = ExecuteConsumer()


def start_periodic_task(interval: int = 5):
    """
    FastAPI 이벤트 루프에서 주기적인 작업을 실행
    """
    asyncio.create_task(execute_consumer.start())
