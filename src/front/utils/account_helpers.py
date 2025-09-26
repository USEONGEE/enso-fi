from telegram.ext import (
    ContextTypes,
)

from hypurrquant.logging_config import configure_logging
from hypurrquant.models.account import Account
from .account_manager import AccountManager
from typing import List, Dict

logger = configure_logging(__name__)

# ================================
# 외부 API
# ================================

ACCOUNT_MANAGER_KEY = "account_manager"


# ================================
# AccountManager 가져오기
# ================================
async def fetch_account_manager(context: ContextTypes.DEFAULT_TYPE) -> AccountManager:
    if context.user_data.get(ACCOUNT_MANAGER_KEY):
        return context.user_data[ACCOUNT_MANAGER_KEY]

    account_manager = AccountManager(telegram_id=str(context._user_id))
    context.user_data[ACCOUNT_MANAGER_KEY] = account_manager

    return account_manager


async def fetch_active_account(
    context: ContextTypes.DEFAULT_TYPE, force: bool = False
) -> Account:
    """
    현재 활성화된 계정을 가져옵니다.
    만약 활성화된 계정이 없다면, AccountManager를 통해 새로 가져옵니다.
    """
    account_manager: AccountManager = await fetch_account_manager(context)
    active_account: Account = await account_manager.get_active_account(force=force)

    if not active_account:
        raise ValueError(
            "Something went wrong. No active account found. Please contact support."
        )

    return active_account
