from hypurrquant.db.mongo import get_mongo
from .account_repository import AccountRepository


def get_account_repository():
    db = get_mongo()
    return AccountRepository(db)
