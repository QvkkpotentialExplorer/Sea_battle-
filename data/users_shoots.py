import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class UserShoot(SqlAlchemyBase):
    __tablename__ = 'users_shoots'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=True)
    board_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('boards.id'), nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
