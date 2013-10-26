from pyramidsite.models import User

from wtforms import validators

class UniqueEmail(validators.Required):
    def __call__(self, form, field):
        if User.email_exists(field.data):
            if self.message is None:
                self.message = u'This email is already registered'
            field.errors[:] = []
            raise validators.StopValidation(self.message)


class ExceptMyOwnUniqueEmail(validators.Required):
    def __call__(self, form, field):
        if User.email_exists(field.data, form.current_email.data):
            if self.message is None:
                self.message = u'This email is already registered'
            field.errors[:] = []
            raise validators.StopValidation(self.message)


class NonRegisteredEmail(validators.Required):
    def __call__(self, form, field):
        if User.get_user_by_email(field.data) is None:
            if self.message is None:
                self.message = u'This email is already registered'

            field.errors[:] = []
            raise validators.StopValidation(self.message)


class UniqueUsername(validators.Required):
    def __call__(self, form, field):
        if User.username_exists(field.data):
            if self.message is None:
                self.message = u'This already exists'
            field.errors[:] = []
            raise validators.StopValidation(self.message)