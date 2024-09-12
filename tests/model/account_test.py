from uuid import uuid4

import pytest
from config import get_db_session
from model.account import Account
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy_model_faker import factory
from sqlalchemy_utils import UUIDType

Base = declarative_base()


### モデル
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    name = Column(String)


### Query 関数
def query_accounts(name: str):
    session = get_db_session()
    return session.query(Account).where(Account.name == name)


### 呼び出し関数
def fetch_accounts():
    res = query_accounts('Tokyo').all()
    return res


### モック
class AllFake:
    def all(self):
        product = factory(Account).make({'name': 'Tokyo'})
        return [product]

    def where(self, name):
        return AllFake()


### テスト
def test_query_accounts():
    res = query_accounts('Tokyo').statement.compile()
    assert res.string == 'SELECT accounts.id, accounts.name \nFROM accounts \nWHERE accounts.name = :name_1'


def test_fetch_accounts(mocker):
    m = mocker.patch('sqlalchemy.orm.Session.query', return_value=AllFake())
    res = fetch_accounts()
    assert res[0].name == 'Tokyo'


@pytest.mark.dbtest()
def test_fetch_accounts_db():
    """
    DB を使ったテストは、マークをつけておいて、 TDD とは別に pre-commit で実行する
    """
    pass
