# -*- coding: utf-8 -*-

import transaction
from cromlech.sqlalchemy import SQLAlchemySession
from trilith.sql.oauth2 import models
from trilith.oauth2.interfaces import IUsers, IGrants, ITokens, IClients
from zope.interface import implementer
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound


class Storage(object):

    __factory__ = None
    
    def __init__(self, engine):
        self.engine = engine

    def find(self, **params):
        try:
            with SQLAlchemySession(self.engine) as s:
                q = s.query(self.__factory__)
                for key, value in params.items():
                    q = q.filter(getattr(self.__factory__, key) == value)
                    return q.one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            # Might need logging
            return None

    def add(self, **data):
        print data
        item = self.__factory__(**data)
        with transaction.manager as tm:
            with SQLAlchemySession(self.engine, transaction_manager=tm) as s:
                s.add(item)
        return item

    def __getitem__(self, key):
        try:
            with SQLAlchemySession(self.engine) as s:
                return s.query(self.__factory__).get(key)
        except sqlalchemy.orm.exc.NoResultFound:
            raise KeyError(key)

    def __iter__(self):
        with SQLAlchemySession(self.engine) as s:
            for item in s.query(self.__factory__):
                yield item
            else:
                raise StopIteration()

    def __contains__(self, key):
        # Assumes that the primary_key is 'id'
        # In case it's not true, override in subclass.
        with SQLAlchemySession(self.engine) as s:
            q = s.query(self.__factory__.id).filter(self.__factory__.id == key)
            return bool(s.query(q.exists()))

    def delete(self, item):
        with transaction.manager as tm:
            with SQLAlchemySession(self.engine, transaction_manager=tm) as s:
                s.delete(item)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


@implementer(IUsers)
class Users(Storage):
    __factory__ = models.User


@implementer(IClients)
class Clients(Storage):
    __factory__ = models.Client


@implementer(IGrants)
class Grants(Storage):
    __factory__ = models.Grant


@implementer(ITokens)
class Tokens(Storage):
    __factory__ = models.Token
