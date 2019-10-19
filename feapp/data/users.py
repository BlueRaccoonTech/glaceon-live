import datetime
import sqlalchemy
import sqlalchemy.orm as orm
from feapp.data.modelbase import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    username = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    last_streamed = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_streaming = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    userdata = orm.relationship('UserData', backref="user", uselist=False)
    userkeys = orm.relationship('UserKeys', backref="user", uselist=False)