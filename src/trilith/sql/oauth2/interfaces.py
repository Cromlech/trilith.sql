# -*- coding: utf-8 -*-

from random import SystemRandom
from trilith.oauth2 import interfaces
from zope.schema import ASCIILine

_sys_rng = SystemRandom()
SALT_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def client_id_generator(size):
    def generate():
        if size <= 0:
            raise ValueError('Salt size must be positive')
        return ''.join(_sys_rng.choice(SALT_CHARS) for _ in xrange(size))
    return generate


class IUser(interfaces.IUser):
    pass


class IClient(interfaces.IClient):

    id = ASCIILine(
        title=u'Unique identifier',
        constraint=interfaces.sized(40),
        defaultFactory=client_id_generator(40),
        required=True)

    id.order = 0


class IGrant(interfaces.IGrant):
    pass


class IToken(interfaces.IToken):
    pass
