# -*- coding: utf-8 -*-

import zeam.form.base as forms
from . import MF as _


class AskPasswordAction(forms.Action):

    def get_user(self, form, data):
        raise NotImplementedError('To be implemented in subclasses.')
    
    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return forms.FAILURE

        user = self.get_user(form, data)

        if user is None:
            form.flash(_(u"Sorry, this account does not exist"))
            return forms.FAILURE
        elif hasattr(user, 'is_active') and user.is_active():
            pwd_manager = IPasswordManager(user)
            pwd_manager.request_password_reset()
            form.flash(_(u"A mail was sent to reset your password, " +
                         u"please check your inbox"))
            form.redirect(form.application_url()
            return forms.SUCCESS
        else:
            form.flash(_(u"Sorry this account is not active"))
            return forms.FAILURE


class AskPasswordAction(forms.Action):

    def get_user(self, form, data):
        raise NotImplementedError('To be implemented in subclasses.')
    
    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return forms.FAILURE

        user = self.get_user(form, data)

        if user is None:
            form.flash(_(u"Sorry, this account does not exist"))
            form.redirect(form.application_url(name='login'))
        elif hasattr(user, 'is_active') and user.is_active():
            pwd_manager = IPasswordManager(user)
            pwd_manager.request_password_reset()
            website_message(_(u"A mail was sent to reset your password, " +
                              u"please check your inbox"))
            return forms.SUCCESS
        else:
            website_message(_(u"Sorry this account is not active"))
            raise exceptions.HTTPFound(form.request.application_url + '/login')
