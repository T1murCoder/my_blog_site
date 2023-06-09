import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Token(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tokens'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    token = sqlalchemy.Column(sqlalchemy.String, default='token')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)

    def set_token(self, token):
        self.token = token