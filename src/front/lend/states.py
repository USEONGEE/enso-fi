from enum import Enum, auto


# ================================
# state
# ================================
class LendState(Enum):
    SELECT_ACTION = auto()  # 전체매도/부분매도/종목선택 옵션 표시
    REFRESH = auto()
