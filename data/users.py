import sqlalchemy
from db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'USERS'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.TEXT, index=True, unique=True, nullable=True)
    hash_password = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)

