import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin

class Favorite(SqlAlchemyBase, UserMixin):
    __tablename__ = 'favorite'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    FavoriteProducts = sqlalchemy.Column(sqlalchemy.String)
