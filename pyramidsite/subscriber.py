import logging

from pyramidsite.events import *
from pyramidsite.interfaces import IMailSender
from pyramidsite.models import User
from pyramid.events import subscriber

from pyramidsite.utils import greenlet

logger = logging.getLogger(__name__)


@subscriber(RecoverPassword)
@greenlet
def recover_password(event):
    """ This function sent an email to the user that is
    trying to recover a lost password. It's executed any time a
    RecoverPassword event is triggered.
    """
    mail = event.request.registry.getUtility(IMailSender)
    mail.send_simple(u"Recover Password", event.email, 'account/recover-password-mail.jinja2', salt=event.salt,
        host=event.request.host_url,username=event.username)


@subscriber(NewPassword)
@greenlet
def new_password(event):
    """ Send an email when the user has successfully changed its password.
    It's executed once the New Password event is triggered
    """
    mail = event.request.registry.getUtility(IMailSender)
    mail.send_simple(u"Your New Pass", event.email, 'account/new-password-mail.jinja2', password=event.password,
        username=event.username,host=event.request.host_url)


@subscriber(NewUser)
@greenlet
def new_user(event):
    """ Send an email once a new user is created
    """
    mail = event.request.registry.getUtility(IMailSender)
    mail.send_simple(u"Welcome", event.email, 'account/mail-new-user.jinja2', password=event.password,
        username=event.username,email=event.email,host=event.request.host_url)


