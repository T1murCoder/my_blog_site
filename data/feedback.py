import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Feedback(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'feedback'
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String(140), nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    author = orm.relationship("User")
    author_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id", ondelete="CASCADE"))