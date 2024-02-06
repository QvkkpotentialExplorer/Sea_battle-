import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class PrizeData(SqlAlchemyBase):
    __tablename__ = 'prize_data'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    is_win = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    owner_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=True)
    date_win = sqlalchemy.Column(sqlalchemy.Text)
    prize_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('prizes.id'), nullable=True)
    prize = orm.relationship('Prize')
