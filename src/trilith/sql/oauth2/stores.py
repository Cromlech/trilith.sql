# -*- coding: utf-8 -*-

import transaction
from cromlech.sqlalchemy import SQLAlchemySession
from trilith.sql.oauth2 import models
from trilith.oauth2.interfaces import IUsers, IGrants, ITokens, IClients
from zope.interface import implementer


@implementer(IUsers)
class Users(object):

    __factory__ = models.User

    def __init__(self, engine):
        self.engine = engine

    def add(self, **data):
        item = self.__factory__(**data)
        with SQLAlchemySession(self.engine) as session:
            session.add(item)
        return item

    def get(self, username, password, client, request, *args, **kwargs):
        import pdb
        pdb.set_trace()

    def set(self, user):
        pass

    def __iter__(self):
        return iter([])

    def __contains__(self, key):
        pass


@implementer(IClients)
class Clients(object):

    __factory__ = models.Client

    def __init__(self, engine):
        self.engine = engine

    def get(self, access_token=None, refresh_token=None):
        import pdb
        pdb.set_trace()
        
    def add(self, **data):
        item = self.__factory__(**data)
        with transaction.manager as tm:
            with SQLAlchemySession(self.engine, transaction_manager=tm) as s:
                s.add(item)
        return item

    def __getitem__(self, key):
        with SQLAlchemySession(self.engine) as s:
            return s.query(self.__factory__).get(key)

    def __iter__(self):
        with SQLAlchemySession(self.engine) as s:
            for item in s.query(self.__factory__):
                yield item
            else:
                raise StopIteration()

    def __contains__(self, key):
        pass


@implementer(ITokens)
class Tokens(object):

    __factory__ = models.Token

    def __init__(self, engine):
        self.engine = engine

    def add(self, **data):
        data['id'] = gen_salt(40)
        item = self.__factory__(**data)
        with SQLAlchemySession(self.engine) as session:
            session.add(item)
        return item
    
    def __getitem__(self, key):
        pass

    def __iter__(self):
        return iter([])

    def __contains__(self, key):
        pass

    def get(self, access_token=None, refresh_token=None):
        import pdb
        pdb.set_trace()

    def set(self, token, request, *args, **kwargs):
        pass


@implementer(IGrants)
class Grants(object):

    __factory__ = models.Grant

    def __init__(self, engine):
        self.engine = engine

    def add(self, **data):
        item = self.__factory__(**data)
        with SQLAlchemySession(self.engine) as session:
            session.add(item)
        return item
    
    def __getitem__(self, key):
        pass

    def __iter__(self):
        return iter([])

    def __contains__(self, key):
        pass

    def get(self, client_id, code):
        import pdb
        pdb.set_trace()

    def set(self, client_id, code, request, *args, **kwargs):
        pass
