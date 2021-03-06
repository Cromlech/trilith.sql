# -*- coding: utf-8 -*-

from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, Text, ForeignKey, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from zope.interface import implementer
from .interfaces import IUser, IGrant, IToken, IClient


Base = declarative_base()


@implementer(IUser)
class User(Base):
    """User
    """
    __schema__ = [IUser]
    __tablename__ = 'users'

    username = Column(String(128), primary_key=True)
    common_name = Column(String(128))
    function = Column(String(128))


@implementer(IClient)
class Client(Base):
    """Client : may be linked to a User or stand alone.
    """
    __schema__ = [IClient]
    __tablename__ = 'clients'

    id = Column(String(40), primary_key=True)
    name = Column(String(40), unique=True)
    type = Enum('public', 'confidential')
    secret = Column(String(55))
    user_id = Column(ForeignKey(User.username), nullable=True)
    redirections = Column(Text)
    default_target_scopes = Column(Text)

    # Relationships
    user = relationship('User')

    @property
    def client_id(self):
        return self.id

    @property
    def client_secret(self):
        return self.secret

    @property
    def client_type(self):
        return self.type

    @property
    def redirect_uris(self):
        if self.redirections:
            return self.redirections.split()
        return []

    @redirect_uris.setter
    def redirect_uris(self, value):
        self.redirections = ' '.join(value)
        
    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self.default_target_scopes:
            return self.default_target_scopes.split()
        return []

    @default_scopes.setter
    def default_scopes(self, value):
        self.default_target_scopes = ' '.join(value)


@implementer(IGrant)
class Grant(Base):
    __schema__ = [IGrant]
    __tablename__ = 'grants'

    # Identity
    id = Column(Integer, primary_key=True)

    # Affiliation
    client_id = Column(String(40), ForeignKey(Client.id))
    user_id = Column(
        String(128), ForeignKey(User.username, ondelete='CASCADE'),
        nullable=True)

    # Destination
    redirect_uri = Column(String(255))

    # Restrictions
    code = Column(String(255), index=True, nullable=True)
    expires = Column(DateTime)
    allowed_scopes = Column(Text)

    # relationships
    client = relationship('Client')
    user = relationship('User')

    @property
    def scopes(self):
        if self.allowed_scopes:
            return set(self.allowed_scopes.split())
        return set()

    @scopes.setter
    def scopes(self, value):
        self.allowed_scopes = ' '.join(value)

    
@implementer(IToken)
class Token(Base):
    __schema__ = [IToken]
    __tablename__ = 'tokens'

    # Identity
    id = Column(Integer, primary_key=True)
    token_type = Enum('Bearer', 'MAC')
    access_token = Column(String(255), unique=True)
    refresh_token = Column(String(255), unique=True)

    # Affiliation
    client_id = Column(String(40), ForeignKey(Client.id))
    user_id = Column(String(128), ForeignKey(User.username), nullable=True)

    # Restrictions
    expires = Column(DateTime)
    allowed_scopes = Column(Text)

    # relationships
    client = relationship('Client')
    user = relationship('User')

    @property
    def scope(self):
        if self.allowed_scopes:
            return set(self.allowed_scopes.split())
        return set()

    @scope.setter
    def scope(self, value):
        self.allowed_scopes = value
