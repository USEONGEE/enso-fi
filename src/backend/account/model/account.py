from typing import Optional
from pydantic import BaseModel, field_validator
from eth_account import Account as EthAccount


class Account(BaseModel):
    nickname: str
    public_key: str
    private_key: str
    is_active: bool = False  # 기본값 설정

    @field_validator("private_key")
    def validate_private_key(cls, private_key):
        try:
            # EthAccount를 이용해 private key 검증
            EthAccount.from_key(private_key)
        except Exception as e:
            raise ValueError(f"Invalid private key: {e}")
        return private_key
