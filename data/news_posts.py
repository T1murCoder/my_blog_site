import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class NewsPost(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "posts"
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    post_tg_url = sqlalchemy.Column(sqlalchemy.String, unique=True)
    comments = orm.relationship("Comment", back_populates='post')

    def __repr__(self):
        return '<NewsPost %r>' % self.post_tg_url