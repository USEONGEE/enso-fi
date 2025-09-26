from enum import Enum


class Command(str, Enum):
    START = "start"
    WALLET = "wallet"
    LEND = "lend"
    FIRST_REGISTER = "first_register"

    def __str__(self) -> str:  # f-string에서 값이 나오게
        return self.value
