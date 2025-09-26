from hypurrquant.logging_config import configure_logging
from hypurrquant.utils.singleton import singleton
from hypurrquant.db.mongo import get_mongo_client
from hypurrquant.exception import CannotDeleteAllAccounts
from hypurrquant.exception import (
    MaxAccountsReachedException,
    DuplicateNicknameException,
    NoSuchAccountByProvidedNickName,
    NoSuchAccountByProvidedTelegramId,
    NoSuchAccountByProvidedPublicKey,
    NoSuchReferralCodeException,
)
from ..model.account import Account
from eth_account import Account as EthAccount
from typing import Optional, List

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReadPreference, WriteConcern
import uuid

logger = configure_logging(__name__)


MAX_ACCOUNTS_PER_USER = 10  # 최대 계정 개수


@singleton
class AccountRepository:
    def __init__(self, db: AsyncIOMotorDatabase, mongo_client=None):
        # 기존 계좌 기본정보 컬렉션
        self.accounts_collection = db["accounts"]
        self.mongo_client = mongo_client or get_mongo_client()

    async def upsert_user_chat(self, telegram_id: str, chat_id: str):
        """telegram_id에 해당하는 문서에 chat_id를 추가 또는 업데이트"""
        logger.debug(f"Upserting chat_id for telegram_id: {telegram_id}")
        await self.accounts_collection.update_one(
            {"telegram_id": telegram_id},
            {"$set": {"chat_id": chat_id}},
            upsert=True,
        )
        return True

    async def create_indexes(self):
        """
        필요한 필드에 대한 인덱스를 생성한다.
        이미 존재하는 경우 중복 생성하지 않음.
        """
        existing_indexes = await self.accounts_collection.index_information()
        existing_index_names = existing_indexes.keys()

        indexes_to_create = [
            ("telegram_id", True),  # 사용자별 계좌 조회 최적화 (고유 인덱스)
            ("accounts.public_key", False),  # 배열 내 public_key 조회 최적화
        ]

        await self.accounts_collection.create_index(
            [("referral_code", 1)], unique=True, sparse=True
        )

        await self.accounts_collection.create_index("accounts.public_key")
        for field, unique in indexes_to_create:
            if field not in existing_index_names:
                await self.accounts_collection.create_index([(field, 1)], unique=unique)

    async def save_account(
        self, telegram_id: str, account: Account, session=None
    ) -> Account:
        """
        MongoDB에 Account 객체를 추가한다.
        계정 중복 및 최대 계정 개수(최대 MAX_ACCOUNTS_PER_USER개) 검사를 수행한다.
        """
        account_data = account.model_dump()
        user_document = await self.accounts_collection.find_one(
            {"telegram_id": telegram_id}
        )

        # 닉네임 중복 검사
        if user_document:
            for existing_account in user_document.get("accounts", []):
                if existing_account.get("nickname") == account.nickname:
                    raise DuplicateNicknameException(
                        f"Nickname '{account.nickname}' already exists."
                    )

        # 계정 개수 검사 (최대 MAX_ACCOUNTS_PER_USER개)
        if (
            user_document
            and len(user_document.get("accounts", [])) >= MAX_ACCOUNTS_PER_USER
        ):
            raise MaxAccountsReachedException(
                f"Maximum of {MAX_ACCOUNTS_PER_USER} accounts per user is allowed."
            )

        await self.accounts_collection.update_one(
            {"telegram_id": telegram_id},
            {"$push": {"accounts": account_data}},
            upsert=True,
            session=session,
        )

        return Account(**account_data)

    def create_account(self, nickname: str = "default") -> dict:
        """
        새로운 이더리움 계좌를 생성한다.
        public_key, private_key 등을 반환.
        """
        acct = EthAccount.create("KEYSMASH FJAFJKLDSKF7JKFDJ 1530")
        return {
            "nickname": nickname,
            "public_key": acct.address,
            "private_key": acct.key.hex(),
        }

    async def create_new_account(self, telegram_id: str) -> Account:
        async with await self.mongo_client.start_session() as session:
            # 트랜잭션 콜백: session 객체를 인자로 받아야 자동 재시도 기능이 동작합니다.
            async def txn(sess):
                new_account = self.create_account("default")
                new_account["is_active"] = True
                # save_account에도 session을 전달하도록 시그니처를 바꿔야 합니다.
                return await self.save_account(
                    telegram_id, Account(**new_account), session=sess
                )

            # with_transaction 내부에서 TransientTransactionError 발생 시 최대 3회까지 재시도
            account = await session.with_transaction(
                txn,
                read_preference=ReadPreference.PRIMARY,
                write_concern=WriteConcern("majority"),
            )
            return account

    async def activate_account(self, telegram_id: str, nickname: str) -> Account:
        """
        주어진 닉네임의 계좌를 활성화하고 나머지는 비활성화한다.
        """
        user_document = await self.accounts_collection.find_one(
            {"telegram_id": telegram_id}
        )
        if not user_document:
            raise NoSuchAccountByProvidedTelegramId("Invalid telegram id.")

        updated_accounts = []
        activated_account: Optional[dict] = None

        for account in user_document.get("accounts", []):
            if account.get("nickname") == nickname:
                account["is_active"] = True
                activated_account = account
            else:
                account["is_active"] = False
            updated_accounts.append(account)

        if not activated_account:
            error_message = (
                f"{telegram_id} 의 계정 중 {nickname}을(를) 찾을 수 없습니다."
            )
            raise Exception(error_message)

        await self.accounts_collection.update_one(
            {"telegram_id": telegram_id}, {"$set": {"accounts": updated_accounts}}
        )
        return Account(**activated_account)

    async def delete_account_by_nickname(
        self, telegram_id: str, nickname: str, session=None
    ) -> Account:
        """
        주어진 닉네임의 계좌를 삭제한다.
        단, 계좌가 1개밖에 없으면 삭제할 수 없으며,
        삭제된 계좌가 활성 상태라면 남은 계좌 중 첫 번째를 활성화한다.
        """
        user_document = await self.accounts_collection.find_one(
            {"telegram_id": telegram_id}, session=session
        )
        if not user_document:
            raise NoSuchAccountByProvidedTelegramId("Invalid telegram id.")

        accounts = user_document.get("accounts", [])
        if len(accounts) == 1:
            error_message = f"계정이 1개뿐이어서 삭제할 수 없습니다. (nickname: {accounts[0].get('nickname')})"
            raise CannotDeleteAllAccounts(error_message)

        index_to_remove: Optional[int] = None
        for i, account in enumerate(accounts):
            if account.get("nickname") == nickname:
                index_to_remove = i
                break

        if index_to_remove is None:
            error_message = f"{telegram_id} 의 {nickname} 계정을 찾을 수 없습니다."
            raise NoSuchAccountByProvidedNickName(error_message)

        removed_account = accounts.pop(index_to_remove)
        if removed_account.get("is_active", False) and accounts:
            accounts[0]["is_active"] = True

        await self.accounts_collection.update_one(
            {"telegram_id": telegram_id}, {"$set": {"accounts": accounts}}
        )

        return Account(**removed_account)

    async def get_active_account(self, telegram_id: str) -> Account:
        """
        현재 활성화된 계좌를 반환한다.
        활성 계좌가 없으면 첫 번째 계좌를 활성화하고 반환한다.
        """
        user_document = await self.accounts_collection.find_one(
            {"telegram_id": telegram_id}
        )
        if not user_document:
            raise NoSuchAccountByProvidedTelegramId("Invalid telegram id.")

        for account in user_document.get("accounts", []):
            if account.get("is_active"):
                return Account(**account)

        # 활성 계좌가 없는 경우 첫 번째 계좌를 활성화
        default_account = user_document["accounts"][0]
        default_account["is_active"] = True
        await self.accounts_collection.update_one(
            {"telegram_id": telegram_id},
            {"$set": {"accounts": user_document["accounts"]}},
        )
        return Account(**default_account)

    async def get_all_accounts(self, telegram_id: str) -> List[Account]:
        """
        사용자의 모든 계좌를 반환한다.
        계좌가 하나도 없으면 새 계좌를 생성하여 반환한다.
        """
        user_document = await self.accounts_collection.find_one(
            {"telegram_id": telegram_id}
        )
        if not user_document or "accounts" not in user_document:
            return [await self.create_new_account(telegram_id)]

        return [Account(**acct) for acct in user_document["accounts"]]

    async def get_account_by_nickname(self, telegram_id: str, nickname: str) -> Account:
        """
        사용자의 닉네임으로 계좌를 조회하여 반환한다.
        """
        user_document = await self.accounts_collection.find_one(
            {"telegram_id": telegram_id}
        )
        if not user_document:
            raise NoSuchAccountByProvidedTelegramId("Invalid telegram id.")

        for account in user_document.get("accounts", []):
            if account.get("nickname") == nickname:
                return Account(**account)

        error_message = f"{telegram_id} 의 {nickname} 계정을 찾을 수 없습니다."
        raise NoSuchAccountByProvidedNickName(error_message)

    async def get_account_by_public_key(self, public_key: str) -> Optional[Account]:
        """
        public_key를 기준으로 계좌를 조회한다.
        여러 건이 조회되면 첫 번째 계좌(Account 객체)를 반환하며,
        조회 결과가 없으면 None을 반환한다.
        """
        # "accounts.public_key"가 일치하는 문서를 조회
        doc = await self.accounts_collection.find_one(
            {"accounts.public_key": public_key}
        )
        if doc:
            # 문서 내의 accounts 배열에서 public_key가 일치하는 첫 번째 항목을 찾음
            for account_data in doc.get("accounts", []):
                if account_data.get("public_key") == public_key:
                    return Account(**account_data)

        raise NoSuchAccountByProvidedPublicKey(
            f"No account found with public key: {public_key}"
        )

    async def get_chat_id_by_public_key(self, public_key: str) -> str:
        """
        주어진 public_key에 해당하는 계좌의 chat_id를 반환한다.
        chat_id가 없거나 계정이 없으면 NoSuchAccountByProvidedPublicKey 예외를 던진다.
        """
        doc = await self.accounts_collection.find_one(
            {"accounts.public_key": public_key},
            {"accounts.$": 1, "chat_id": 1},  # chat_id도 함께 조회
        )
        # 계정 배열이 있으면
        if doc and doc.get("accounts"):
            # 최상위 chat_id 반환
            chat_id = doc.get("chat_id")
            if chat_id:
                return chat_id
            # 계정은 있지만 chat_id 필드가 비어 있거나 None일 때
            raise NoSuchAccountByProvidedPublicKey(
                f"Account with public key {public_key} has no associated chat_id"
            )

        # 일치하는 계정 자체가 없을 때
        raise NoSuchAccountByProvidedPublicKey(
            f"No account found with public key: {public_key}"
        )

    async def get_chat_ids_by_public_key(self, public_key: str) -> List[str]:
        """
        주어진 public_key를 가진 모든 계좌에서 chat_id를 수집하여 반환한다.
        (accounts 컬렉션 내 각 문서의 accounts 배열을 순회)
        """
        chat_ids = []
        cursor = await self.accounts_collection.find(
            {"accounts.public_key": public_key}
        )
        async for doc in cursor:
            for account_data in doc.get("accounts", []):
                if account_data.get("public_key") == public_key:
                    # 문서에 chat_id가 존재하면 수집 (chat_id가 없으면 None이므로 필터)
                    if account_data.get("chat_id"):
                        chat_ids.append(account_data["chat_id"])
        if not chat_ids:
            raise NoSuchAccountByProvidedPublicKey(
                f"No account found with public key: {public_key}"
            )
        return chat_ids
