# -*- coding: utf-8 -*-

import grokcore.component as grok
from zope.component import getUtility
from zope.event import notify
from zope.interface import implementer, provider

from .interfaces import IPasswordManager
from .events import PasswordRequestedEvent
from .token import ITokenFactory


@provider(IPasswordManager)
@implementer(IPasswordManager)
class PasswordManagerAdapter(grok.Adapter):
    grok.baseclass()

    tokenizer = "sha_tokenizer"

    def get_user(self):
        raise NotImplementedError('Implement in subclasses.')

    def set_new_password(self, user, newpass):
        """Generic implementation
        """
        user.password = newpass
        return True
    
    def request_password_reset(self):
        """sends a challenge to users which will be usable to reset password
        """
        try:
            user = self.get_user()
            tokenizer = getUtility(ITokenFactory, name=self.tokenizer)
            challenge = tokenizer.create(user.username)
            notify(PasswordRequestedEvent(user, challenge))
            return challenge
        except KeyError:
            pass  # silently pass for security sakes

    def reset_password(self, newpass, challenge):
        """set new password given valid challenge.
        """
        user = self.get_user()
        tokenizer = getUtility(ITokenFactory, name=self.tokenizer)
        if not tokenizer.verify(user.username, challenge):
            return False
        else:
            return self.set_new_password(user, newpass)
