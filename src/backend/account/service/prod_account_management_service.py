from hypurrquant.logging_config import configure_logging
from hypurrquant.utils.singleton import singleton
from hypurrquant.db.mongo import get_mongo_client
from hypurrquant.constant.kafka import (
    RebalanceKafkaTopic,
    get_topic,
    CopyTradingKafkaTopic,
)
from hypurrquant.server.exception_handler import handle_api_errors
from hypurrquant.exception import (
    AlreadyRegisteredAccountException,
    NoSuchAccountByProvidedPublicKey,
    CannotApproveBuilderFeeException,
)
from .account_management_service import AccountManagementServiceInterface
from ..model.account import Account
from ..repository.dependencies import (
    get_account_repository,
)
from ..repository.account_repository import AccountRepository

from hypurrquant.messaging.dependencies import get_producer

from typing import List
from pymongo import ReadPreference, WriteConcern

logger = configure_logging(__name__)


REBALANCE_DELETE_TOPIC = get_topic(RebalanceKafkaTopic.REBLANACE_ACCOUNT_DELETE.value)
COPY_TRADING_ACCOUNT_DELETE_TOPIC = get_topic(
    CopyTradingKafkaTopic.ACCOUNT_DELETE.value
)


@singleton
class AccountManagementService(AccountManagementServiceInterface):
    def __init__(self, mongo_client=None):

        self.account_repository: AccountRepository = get_account_repository()
        self.mongo_client = mongo_client or get_mongo_client()
        self.producer = get_producer()

    async def create_account(self, telegram_id: str, nickname: str) -> Account:
        """
        Create a new account for the user.

        Args:
            telegram_id (str): User's unique identifier.

        Returns:
            dict: New account details.
        """
        # 1. 새로운 계좌 생성
        new_account = self.account_repository.create_account(nickname)

        # 2. 계좌 저장
        created_account = await self.account_repository.save_account(
            telegram_id, Account(**new_account)
        )
        return created_account

    async def get_active_account(self, telegram_id: str) -> Account:
        return await self.account_repository.get_active_account(telegram_id)

    async def activate_account(self, telegram_id: str, nickname: str) -> bool:
        return await self.account_repository.activate_account(telegram_id, nickname)

    async def get_all_accounts(self, telegram_id: str) -> List[Account]:
        logger.debug(f"service")
        return await self.account_repository.get_all_accounts(telegram_id)

    async def get_account_by_nickname(self, telegram_id: str, nickname: str) -> Account:
        return await self.account_repository.get_account_by_nickname(
            telegram_id, nickname
        )

    async def get_account_by_public_key(self, public_key: str) -> Account:
        return await self.account_repository.get_account_by_public_key(public_key)

    @handle_api_errors
    async def import_account(
        self, telegram_id, private_key: str, nickname: str
    ) -> Account:
        # private key를 통해 eth account 로드
        from eth_account import Account as EthAccount

        eth_account = EthAccount.from_key(private_key)

        # 중복 계좌 검사: 이미 동일한 public key의 계좌가 존재하는지 확인
        try:
            existing_account = await self.account_repository.get_account_by_public_key(
                eth_account.address
            )
        except NoSuchAccountByProvidedPublicKey:
            # 계좌가 존재하지 않으면 예외가 발생하므로, 여기서는 중복 없음.
            existing_account = None

        if existing_account:
            logger.info(
                f"중복 계좌 등록 시도: public_key {eth_account.address} 이미 존재합니다."
            )
            raise AlreadyRegisteredAccountException(
                f"Account with public key {eth_account.address} already exists."
            )

        # 계좌 저장
        saved_account = await self.account_repository.save_account(
            telegram_id,
            Account(
                nickname=nickname,
                public_key=eth_account.address,
                private_key=private_key,
            ),
        )
        # 레퍼럴 적용 및 거래소 초기화
        try:
            await self.approve_builder_fee(telegram_id, nickname)
        except CannotApproveBuilderFeeException as e:
            logger.info(
                f"레퍼럴 적용 및 거래소 초기화 실패: {telegram_id}, {nickname}",
            )
        except Exception as e:
            logger.error(
                f"레퍼럴 적용 및 거래소 초기화 중 오류 발생: {telegram_id}, {nickname}",
                exc_info=True,
            )
        logger.info(f"Account imported: {saved_account.public_key}")
        return saved_account

    async def delete_account(self, telegram_id: str, nickname: str) -> bool:
        # 계좌 조회
        account: Account = await self.account_repository.get_account_by_nickname(
            telegram_id, nickname
        )

        if not account:
            logger.error(f"{telegram_id}의 {nickname} 계좌가 존재하지 않습니다.")
            return False

        # 데이터베이스 세션 시작
        async with await self.mongo_client.start_session() as session:

            async def txn(sess):
                # 계좌 삭제
                response = await self.account_repository.delete_account_by_nickname(
                    telegram_id,
                    nickname,
                    session=sess,  # <- sess로 변경
                )
                return response  # 콜백의 리턴값

            # with_transaction: TransientTransactionError 발생 시 최대 3회 자동 재시도
            response = await session.with_transaction(
                txn,
                read_preference=ReadPreference.PRIMARY,
                write_concern=WriteConcern("majority"),
            )

        return response
