from .validators import *

from wtforms import\
(
    Form,
    TextField,
    validators,
    PasswordField,
    FileField,
    HiddenField,
    TextAreaField,
    SelectMultipleField,
    BooleanField
    )


class LoginForm(Form):
    """ Form used to authenticate users into the system.
    """
    email = TextField(u'Email', [
        validators.Required()])
    password = PasswordField(u'Password', [
        validators.Required()])
    came_from = HiddenField()


class ProfileForm(Form):
    """ Form used by users to change their profile
    information.
    """
    name = TextField(u'Name', [validators.Required()])
    lastname = TextField(u'Lastname', [validators.Required()])

    email = TextField(u'Email', [
            validators.Required(), validators.Email(),
            ExceptMyOwnUniqueEmail()])
    enabled = BooleanField(u'Active')

    current_email = HiddenField()

class UserForm(Form):
    """ Form used by users to change their profile
    information.
    """
    password = PasswordField(u'Password', [validators.Required()])
    retype_password = PasswordField(u'Retype Password', [
        validators.EqualTo('password', message=u'Password are not identical')])



class RecoverPasswordForm(Form):
    """ Simple form used to recover or reset your
    user password
    """
    email = TextField(u'Enter your email', [
        validators.Required(),
        validators.Email(),
        NonRegisteredEmail(message=u'Not valid email')])


