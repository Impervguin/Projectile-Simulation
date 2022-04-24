import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'USERS'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.TEXT, index=True, unique=True, nullable=True)
    hash_password = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)

    user_graphs = orm.relation("UserGraphs", back_populates='user')

    def set_password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)
