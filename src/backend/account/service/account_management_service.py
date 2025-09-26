from abc import ABC, abstractmethod
from typing import List
from ..model.account import Account


class AccountManagementServiceInterface(ABC):
    @abstractmethod
    async def create_account(self, telegram_id: str, nickname: str) -> Account:
        """
        Create a new account for the user.

        Args:
            telegram_id (str): The user's unique Telegram identifier.
            nickname (str): The nickname for the new account.

        Returns:
            Account: The newly created account.
        """
        pass

    @abstractmethod
    async def get_active_account(self, telegram_id: str) -> Account:
        """
        Retrieve the currently active account for the given telegram_id.

        Args:
            telegram_id (str): The user's unique Telegram identifier.

        Returns:
            Account: The active account.
        """
        pass

    @abstractmethod
    async def activate_account(self, telegram_id: str, nickname: str) -> bool:
        """
        Activate the account with the given nickname and deactivate all others.

        Args:
            telegram_id (str): The user's unique Telegram identifier.
            nickname (str): The nickname of the account to activate.

        Returns:
            bool: True if the activation was successful, else False.
        """
        pass

    @abstractmethod
    async def get_all_accounts(self, telegram_id: str) -> List[Account]:
        """
        Retrieve all accounts associated with the given telegram_id.

        Args:
            telegram_id (str): The user's unique Telegram identifier.

        Returns:
            List[Account]: A list of all accounts.
        """
        pass

    @abstractmethod
    async def get_account_by_nickname(self, telegram_id: str, nickname: str) -> Account:
        """
        Retrieve the account that matches the given nickname.

        Args:
            telegram_id (str): The user's unique Telegram identifier.
            nickname (str): The nickname to search for.

        Returns:
            Account: The account matching the nickname.
        """
        pass

    @abstractmethod
    async def get_account_by_public_key(self, public_key: str) -> Account:
        """
        Retrieve the account that matches the given public key.

        Args:
            public_key (str): The public key of the account.

        Returns:
            Account: The account matching the public key.
        """
        pass

    @abstractmethod
    async def import_account(
        self, telegram_id: str, private_key: str, nickname: str
    ) -> Account:
        """
        Import an account using the provided private key and assign it the given nickname.

        Args:
            telegram_id (str): The user's unique Telegram identifier.
            private_key (str): The private key of the account.
            nickname (str): The nickname for the imported account.

        Returns:
            Account: The imported account.
        """
        pass

    @abstractmethod
    async def delete_account(self, telegram_id: str, nickname: str) -> bool:
        """
        Delete the account identified by the given nickname for the specified telegram_id.

        Args:
            telegram_id (str): The user's unique Telegram identifier.
            nickname (str): The nickname of the account to delete.

        Returns:
            bool: True if deletion was successful, else False.
        """
        pass
