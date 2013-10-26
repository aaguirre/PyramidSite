class NewContent(object):
    def __init__(self, request, path, name, id):
        self.request = request
        self.path = path
        self.name = name
        self.id = id


class RecoverPassword(object):
    def __init__(self, request, email, salt, username):
        self.request = request
        self.email = email
        self.salt = salt
        self.username = username


class NewPassword(object):
    def __init__(self, request, password, email, username):
        self.request = request
        self.password = password
        self.email = email
        self.username = username

class NewUser(object):
    def __init__(self, request, password, email, username):
        self.request = request
        self.password = password
        self.email = email
        self.username = username

class NewComment(object):
    def __init__(self, request, comment):
        self.request = request
        self.comment = comment

