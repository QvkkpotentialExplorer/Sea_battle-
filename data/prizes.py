import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm



class Prize(SqlAlchemyBase):
    __tablename__ = 'prizes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

