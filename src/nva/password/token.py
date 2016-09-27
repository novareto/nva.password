# -*- coding: utf-8 -*-

import hashlib
import hmac
import grokcore.component as grok
from zope.interface import Interface, implementer, provider
from datetime import date, timedelta


class ITokenFactory(Interface):
    """A unique token factory
    """

    def create(word):
        """returns a hex representation of a tokenized word.
        """

    def verify(word, challenger):
        """returns a bool. True is tokenized word == challenged.
        False otherwise.
        """


@implementer(ITokenFactory)
@provider(ITokenFactory)
class ShaTokenFactory(grok.GlobalUtility):
    """A sha based token factory

    An alternative would be a token factory storing random token.
    The advantage of this solution is that we don't need to manage sweeping
    of old entry.

    The token is valid for a few days
    """
    grok.name("sha_tokenizer")

    secret = "The raven himself is hoarse"
    validity = 3  # validity in days

    @property
    def today(self):
        """isolated for testing purpose"""
        return date.today()

    def create(self, word):
        token = hmac.new(key=self.secret, digestmod=hashlib.sha256)
        token.update(word)
        token.update(str(self.today))
        return token.hexdigest()

    def verify(self, word, challenger):
        today = self.today
        basetoken = hmac.new(key=self.secret, digestmod=hashlib.sha256)
        basetoken.update(word)
        for n in range(self.validity):
            token = basetoken.copy()
            token.update(str(today - timedelta(n)))
            if token.hexdigest() == challenger:
                return True
        return False
