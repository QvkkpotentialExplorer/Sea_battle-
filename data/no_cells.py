import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class DeathCell(SqlAlchemyBase):
    __tablename__ = 'on_cells'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    board_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('boards.id'), nullable=True)
    x = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    u = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    board = orm.relationship("Board", back_populates='death_cells')
