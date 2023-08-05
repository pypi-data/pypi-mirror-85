from sqlalchemy import Table, Column, Integer, DateTime, String, ForeignKey, Float, Binary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from werkzeug.security import generate_password_hash, check_password_hash

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()

class User(Base):
    """
    Class for storing user data.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column('email', String, unique=True)
    fullname = Column('fullname', String)
    _password_hash = Column('password_hash', String)
    authenticated = Column(Boolean, default=False)

    def __repr__(self):
        return "<User(fullname='%s', email='%s', roles='%s')>" % (self.fullname, self.email, [role.name for role in self.roles])

    @hybrid_property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, plain_text_password):
        self._password_hash = generate_password_hash(plain_text_password)

    @hybrid_method
    def check_password(self, plain_text_password):
        return check_password_hash(self.password, plain_text_password)

    def is_authenticated(self):
        return self.authenticated

    def generate_auth_token(self, expiration = 600):
        s = Serializer(config.SECRET_KEY, expires_in = expiration)
        return s.dumps({'id': self.id })
