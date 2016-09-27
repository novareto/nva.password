# -*- coding: utf-8 -*-

from zope.interface import implementer, Attribute
from zope.component.interfaces import IObjectEvent, ObjectEvent


class IPasswordRequestedEvent(IObjectEvent):
    """A user ask for his password
    """
    challenge = Attribute(u"The secret challenge")


@implementer(IPasswordRequestedEvent)
class PasswordRequestedEvent(ObjectEvent):
    """A basic implementation of an IPasswordRequestedEvent.
    """

    def __init__(self, user, challenge):
        super(PasswordRequestedEvent, self).__init__(user)
        self.challenge = challenge
