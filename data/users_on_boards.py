import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import orm


class UserOnBoard(SqlAlchemyBase):
    __tablename__ = 'users_on_board'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey('users.id'))
    board_id = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey('boards.id'))
    count = sqlalchemy.Column(sqlalchemy.Integer,nullable=True)
    can_join = sqlalchemy.Column(sqlalchemy.BOOLEAN)