import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class NewsPost(SqlAlchemyBase):
    pass

    def __repr__(self):
        return '<NewsPost %r>' % self.title