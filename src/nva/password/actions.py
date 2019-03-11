# -*- coding: utf-8 -*-

try:
    import dolmen.forms.base as forms
except ImportError:
    import zeam.form.base as forms

from .interfaces import IPasswordManager
from . import MF as _


class PasswordException(Exception):
    pass


class PasswordAction(forms.Action):

    def get_user(self, form, data):
        raise NotImplementedError('To be implemented in subclasses.')

    def assert_valid_user(self, user):
        if user is None:
            return PasswordException(
                    _(u"Sorry, this account does not exist"))
        active = getattr(user, 'is_active', None)
        if active is not None:
            if not active():
                return PasswordException(
                    _(u"Sorry this account is not active"))
        return None


class AskPasswordAction(PasswordAction):

    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return forms.FAILURE

        user = self.get_user(form, data)
        error = self.assert_valid_user(user)
        
        if error is None:
            pwd_manager = IPasswordManager(user)
            pwd_manager.request_password_reset()
            form.flash(_(u"A mail was sent to reset your password, " +
                         u"please check your inbox"))
            form.redirect(form.application_url())
            return forms.SUCCESS
        else:
            form.flash(error.message)
            return forms.FAILURE

                          
class ResetPasswordAction(PasswordAction):

    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return forms.FAILURE

        user = self.get_user(form, data)
        error = self.assert_valid_user(user)

        if error is None:
            pwd_manager = IPasswordManager(user)
            result = pwd_manager.reset_password(
                data['newpass'], data['challenge'])
            if result is True:
                form.flash(_(u"Password changes with success."))
                return forms.SUCCESS
            else:
                form.flash(_(u"An error occured during the update."))
        else:
            form.flash(error.message)
        return forms.FAILURE
