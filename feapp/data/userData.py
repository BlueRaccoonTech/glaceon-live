import datetime
import sqlalchemy
from feapp.data.modelbase import SqlAlchemyBase
from feapp.data.users import User


class UserData(SqlAlchemyBase):
    __tablename__ = 'userData'

    username = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey(User.username), primary_key=True)
    displayName = sqlalchemy.Column(sqlalchemy.String)
    tagline = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=False, default="/static/img/glaceon-icon.png")
    background = sqlalchemy.Column(sqlalchemy.String, nullable=False, default="/static/img/glaceon-bg-blurred.png")
    videoBanner = sqlalchemy.Column(sqlalchemy.String, nullable=False, default="/static/img/glaceon-bg-blurred.png")