import logging
from datetime import datetime
from .forms import LoginForm, ProfileForm, RecoverPasswordForm, UserForm

from pyramidsite.events import RecoverPassword, NewPassword, NewUser

from pyramidsite.models import User

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import remember
from pyramid.security import forget
from pyramid.url import route_url
from pyramid.view import view_config

logger = logging.getLogger(__name__)


@view_config(context='pyramid.httpexceptions.HTTPForbidden',
    renderer='account/login.jinja2')
@view_config(name='login', renderer='account/login.jinja2')
def login(request):
    """ This view corresponds to the single access point to
     the system. Any invalid access to the system
     will be redirected to this page. Users will need to
     provide whatever an email or username plus a password for
     the authentication.
    """
    if request.user:
        return HTTPFound(location=request.route_url('home'))

    form = LoginForm()

    referrer = request.url
    form.came_from.data = referrer    
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.validate():
            user = User(email=form.email.data, password=form.password.data)
            login = user.validate_user()

            if login:
                came_from = form.came_from.data
                new_user = User.get(login.id)
                new_user.last_access = datetime.now()
                new_user.update()                
                headers = remember(request, login, max_age='86400')
                request.session.flash(u'Successfully logged in')
                return HTTPFound(location=came_from, headers=headers)
            else:
                request.session.flash(u'Incorrect Password')
    return {'form': form}


@view_config(name='recover-password', renderer='account/recover-password.jinja2')
def recoverPassword(request):
    """ This view is designed to makes possible to the users
    to recover their passwords. Users must enter their real emails in order to
    start the process of recovering a password.

    This process consists of:

    * Requesting a new password.
    * Instructions are sent via email, containing an auto generated password.
    * The user validate the new password and obtain a new real password
    """
    form = RecoverPasswordForm()
    if request.method == 'POST':
        form = RecoverPasswordForm(request.POST)
        if form.validate():
            user = User.recover_password(form.email.data)
            request.registry.notify(RecoverPassword(request, form.email.data, user.salt, user.get_user_name()))
            request.session.flash(u'Instructions to recover your password have been sent to your email inbox')
            return HTTPFound(location='/')
    return {'form': form}


@view_config(name='logout')
def logout(request):
    """
    Logout page. Clicking this link users will be logged out of
    the system and any session information will be deleted.
    """
    request.session.user = None
    headers = forget(request)
    request.session.flash(u'You have logged out successfully')
    return HTTPFound(location=route_url('home', request),
        headers=headers)


@view_config(route_name='set-password', renderer='string')
def setPassword(request):
    """ When an user lost its password and tries to recover it
    using the recover password page, a random salt verification
    code will be sent via email. This view is aimed to validate
    this salt code and after that a new password is sent via email.
    """
    salt = request.matchdict.get('salt')
    logger.debug(salt)
    user = User.get_user_by_salt(salt)
    if user and user.validate_salt():
        password = user.set_password()
        user.salt = ''
        user.update()
        request.registry.notify(NewPassword(request, password, user.email, user.get_user_name()))
        request.session.flash(u'Your new password has been sent to your email')
        return HTTPFound(location='/')
    else:
        request.session.flash(u'The link you followed to reset your password has already been used. Please proceed to generate a new password reset link by providing us with your new email address:')
        return HTTPFound(location='/')

