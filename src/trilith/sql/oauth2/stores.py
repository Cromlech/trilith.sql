# -*- coding: utf-8 -*-

import transaction
from cromlech.sqlalchemy import SQLAlchemySession
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound
from trilith.oauth2.interfaces import IUsers, IGrants, ITokens, IClients
from trilith.sql.oauth2 import models
from zope.interface import implementer
from zope.location import ILocation, LocationProxy


@implementer(ILocation)
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
        item = self.__factory__(**data)
        with transaction.manager as tm:
            with SQLAlchemySession(self.engine, transaction_manager=tm) as s:
                s.add(item)
        return item

    def __getitem__(self, key):
        try:
            with SQLAlchemySession(self.engine) as s:
                item = s.query(self.__factory__).get(key)
                if item is not None:
                    return LocationProxy(item, self, key)
        except NoResultFound:
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

    def delete(self, key):
        with transaction.manager as tm:
            with SQLAlchemySession(self.engine, transaction_manager=tm) as s:
                item = s.query(self.__factory__).get(key)
                s.delete(item)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, item, **values):
        print values
        with transaction.manager as tm:
            with SQLAlchemySession(self.engine, transaction_manager=tm) as s:
                for key, value in values.items():
                    setattr(item, key, value)
                    s.add(item)


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
