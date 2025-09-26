from hypurrquant.logging_config import configure_logging, LoggerFactory
from typing import Callable, Any, Coroutine
import time
import asyncio
import functools

_logger = configure_logging(__name__)

_func_runtime_logger = LoggerFactory.get_logger("func_runtime")


def measure_runtime(to_es: bool = False):
    """
    async 함수의 실행 시간을 측정하는 데코레이터.
    to_es=True 이면 OpenSearch 비즈니스 로그도 남긴다.
    (실패 시 스택트레이스는 남기지 않음: 실행시간 로그 단순화 목적)
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                runtime_ms = int((time.perf_counter() - start) * 1000)

                # system 로그: 실행시간만
                _logger.info(f"[{func.__name__!r}] Async runtime: {runtime_ms} ms")

                if to_es:
                    # business 로그: 성공 요약만 (스택 미포함)
                    _func_runtime_logger.info(
                        "",
                        extra={
                            "function": func.__name__,
                            "runtime_ms": runtime_ms,
                            "status": "success",
                        },
                    )
                return result

            except Exception as e:
                runtime_ms = int((time.perf_counter() - start) * 1000)

                # system 로그: 실행시간 + 에러 요약(스택 미포함)
                _logger.error(f"[{func.__name__!r}] Async error: {e}")
                _logger.info(f"[{func.__name__!r}] Async runtime: {runtime_ms} ms")

                if to_es:
                    # business 로그: 실패 요약만 (스택 미포함)
                    _func_runtime_logger.error(
                        "",
                        extra={
                            "function": func.__name__,
                            "runtime_ms": runtime_ms,
                            "status": "error",
                            # 선택) 최소 원인만 남기고 싶다면 다음 두 줄 추가
                            # "error_class": e.__class__.__name__,
                            # "error_message": str(e),
                        },
                    )
                raise  # 예외는 그대로 올려서 상위에서 처리

        return wrapper

    return decorator


def count_active(func: Callable[..., Coroutine]) -> Callable[..., Coroutine]:
    lock = asyncio.Lock()
    active = 0

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        nonlocal active
        async with lock:
            active += 1
            _logger.info(f"Active count: {active}")
        try:
            return await func(*args, **kwargs)
        finally:
            async with lock:
                active -= 1

    # wrapper 함수 객체에 직접 getter 할당
    def get_active_count() -> int:
        return active

    wrapper.active_count = get_active_count

    return wrapper


def tick_to_price(tick: int, decimals0: int, decimals1: int) -> float:
    # 1.0001^tick 계산
    ratio = 1.0001**tick
    # 토큰 decimal 보정
    return ratio * (10**decimals0) / (10**decimals1)


def render_lp_range(
    lower: float,
    price: float,
    upper: float,
    decimals0: int,
    decimals1: int,
    width: int = 16,
    ascii_only: bool = False,
    show_percent: bool = True,
) -> str:
    """
    하한/현재가/상한을 단일 문자열로 시각화.
    - lower >= upper 이면 'invalid' 반환
    - price가 범위 밖이면 상태(below/above) 표시
    - width는 게이지 내부(범위)의 문자 폭
    """
    if lower >= upper:
        return "invalid range (lower >= upper)"

    lower = tick_to_price(lower, decimals0, decimals1)
    upper = tick_to_price(upper, decimals0, decimals1)
    price = tick_to_price(price, decimals0, decimals1)

    # 범위 내 비율 (클램프 X: 상태 판정에 사용)
    p = (price - lower) / (upper - lower)

    # 문자셋
    if ascii_only:
        L, R, IN, OUT, CUR = "[", "]", "=", ".", "|"
    else:
        L, R, IN, OUT, CUR = "⟦", "⟧", "─", "·", "│"

    # 게이지 내부 채우기
    inside = [IN] * width
    # 포인터 위치 (게이지 내부로 클램프해서 찍음)
    cur_idx = 0 if p <= 0 else (width - 1 if p >= 1 else int(round(p * (width - 1))))
    inside[cur_idx] = CUR

    gauge = f"{L}{''.join(inside)}{R}"

    # 상태/퍼센트 텍스트
    if p < 0:
        status = "below"
    elif p > 1:
        status = "above"
    else:
        status = "in-range"

    suffix = f"\n spot={price}"
    if show_percent:
        percent = max(0.0, min(1.0, p)) * 100.0
        suffix += f" ({percent:.1f}% {status})"
    else:
        suffix += f" ({status})"

    return f"{lower:g} {gauge} {upper:g}{suffix}"
