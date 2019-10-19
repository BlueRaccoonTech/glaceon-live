import datetime
import sqlalchemy
import string
import random
from feapp.data.modelbase import SqlAlchemyBase
from feapp.data.users import User


def genstreamkey(size=64, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


class UserKeys(SqlAlchemyBase):
    __tablename__ = 'userKeys'

    username = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey(User.username), primary_key=True)
    streamingKey = sqlalchemy.Column(sqlalchemy.String, nullable=False, default=genstreamkey())
