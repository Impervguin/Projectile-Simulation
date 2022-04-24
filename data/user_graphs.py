import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class UserGraphs(SqlAlchemyBase):
    __tablename__ = 'USER_GRAPHS'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("USERS.id"))
    speed = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    mass = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    substance = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    angle = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    height = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    planet = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    air_env = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    resistance = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    calc_step = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)

    user = orm.relation('User')