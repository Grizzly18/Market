import datetime
import sqlalchemy
from sqlalchemy import orm, ForeignKey
from .db_session import SqlAlchemyBase
from flask_login import UserMixin

class Favorite(SqlAlchemyBase, UserMixin):
    __tablename__ = 'favorite'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    FavoriteProducts = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(ForeignKey("users.id"), nullable=False)
    user = orm.relationship("User", back_populates="favorite")