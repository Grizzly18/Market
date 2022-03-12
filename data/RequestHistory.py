import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin

class RequestHistory(SqlAlchemyBase, UserMixin):
    __tablename__ = 'RequestHistory'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    RequestHistory = sqlalchemy.Column(sqlalchemy.String)
