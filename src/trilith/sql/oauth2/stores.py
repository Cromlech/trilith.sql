# -*- coding: utf-8 -*-

from trilith.sql import models
from trilith.oauth2.interfaces import IUsers, IGrants, ITokens, IClients
from zope.interface import implementer


@implementer(IUsers)
class Users(object):

    __model__ = models.User

    def __init__(self, engine):
        self.engine = engine

    def __getitem__(self, key):
        pass
        
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

    __model__ = models.Client

    def __init__(self, engine):
        self.engine = engine

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

    
@implementer(ITokens)
class Tokens(object):

    __model__ = models.Token

    def __init__(self, engine):
        self.engine = engine

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

    __model__ = models.Grant

    def __init__(self, engine):
        self.engine = engine

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
