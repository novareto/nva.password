# -*- coding: utf-8 -*-

from zope.interface import Interface


class IPasswordManager(Interface):

    def request_password_reset():
        """ask for password reset, generate a challenge available
        in PasswordRequestedEvent"""

    def reset_password(newpass, challenge):
        """reset password to newpass giving the challenge

        return True if operation was successful"""
