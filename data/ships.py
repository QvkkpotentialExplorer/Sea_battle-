import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Ship(SqlAlchemyBase):
    __tablename__ = 'ships'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    board_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('boards.id'), nullable=True)
    x = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    y = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    prize_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('prize_data.id'), nullable=True)
    prize_data = sqlalchemy.orm.relationship('PrizeData')

