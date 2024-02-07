import sqlalchemy
from .db_session import SqlAlchemyBase


class DeathCell(SqlAlchemyBase):
    __tablename__ = 'no_cells'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    board_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('boards.id'), nullable=True)
    x = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    y = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    status_ship = sqlalchemy.Column(sqlalchemy.BOOLEAN,nullable=True)
