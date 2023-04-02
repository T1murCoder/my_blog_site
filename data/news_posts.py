import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class NewsPost(SqlAlchemyBase):
    __tablename__ = "posts"
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    post_tg_url = sqlalchemy.Column(sqlalchemy.String, unique=True)

    def __repr__(self):
        return '<NewsPost %r>' % self.post_tg_url