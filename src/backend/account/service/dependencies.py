# dependencies.py
import os

from .account_management_service import AccountManagementServiceInterface
from .prod_account_management_service import AccountManagementService


def get_account_management_service() -> AccountManagementServiceInterface:
    """
    AccountDetilaService의 인스턴스를 반환.
    """
    return AccountManagementService()
