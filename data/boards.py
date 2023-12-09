import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Board(SqlAlchemyBase):
    __tablename__ = 'boards'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    admin_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=True)
    n = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
