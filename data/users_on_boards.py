import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class UserOnBoard(SqlAlchemyBase):
    __tablename__ = 'users_on_board'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    board_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('boards.id'), nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey('users.id'))
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    can_join = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=True)