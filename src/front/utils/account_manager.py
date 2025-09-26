from hypurrquant.models.account import Account
from hypurrquant.logging_config import configure_logging

from backend.account.service.dependencies import AccountManagementService
from pydantic import BaseModel
from typing import List, Optional

accountService = AccountManagementService()


logger = configure_logging(__name__)


# ================================
# Account를 보관하는 Utility Manager
# ================================
class AccountManager(BaseModel):
    telegram_id: str
    active_account: Optional[Account] = None

    # Private fields for locks

    async def get_active_account(self, force=False) -> Account:
        if force:
            account_list: List[Account] = await self.get_all_accounts()
            for account in account_list:
                if account.is_active:
                    self.active_account = account

        if not self.active_account or not self.active_account.is_active:
            account_list: List[Account] = await self.get_all_accounts()
            for account in account_list:
                if account.is_active:
                    self.active_account = account

        if not self.active_account:  # 서버 에러임
            logger.error(f"telegram_id: {self.telegram_id} No active account")
            raise ValueError("No active account")

        return self.active_account

    async def get_all_accounts(self) -> List[Account]:
        return await accountService.get_all_accounts(self.telegram_id)

    # ================================
    # wallet-setting에서 사용
    # ================================
    async def create_wallet(self, nickname: str = "default") -> Account:
        accounts: List[Account] = await self.get_all_accounts()
        for account in accounts:
            if account.nickname == nickname:
                raise ValueError("Nickname already exists")

            return await accountService.create_account(self.telegram_id, nickname)

    async def import_wallet(self, private_key: str, nickname: str) -> Account:
        return await accountService.import_account(
            self.telegram_id, private_key, nickname
        )

    async def change_wallet(self, nickname: str) -> Account:
        account = await accountService.activate_account(self.telegram_id, nickname)

        self.active_account = account

        return self.active_account

    async def delete_wallet(self, nickname: str):
        await accountService.delete_account(self.telegram_id, nickname)

        account: Account = await self.get_active_account(force=True)
        self.active_account = account

        return self.active_account
