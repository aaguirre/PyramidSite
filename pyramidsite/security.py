import logging

from pyramid.security import Allow
from pyramid.security import Everyone, Authenticated
from pyramid.security import unauthenticated_userid
from pyramid.security import has_permission


from pyramid.threadlocal import get_current_request

logger = logging.getLogger(__name__)

Owner = 'system.Owner'
Admin = 'Admin'

class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, ['add','send-comments','view-profile']),
        (Allow, Owner, 'edit'),
        (Allow, Admin, ['add','send-comments','view-profile','edit']),
    ]
    def __init__(self, request):
        self.request = request

    def get_context_roles(self):
        user = self.request.user
        return user.get_roles()


class ContentFactory(RootFactory):

    def __init__(self, request):
        self.request = request

    def get_context_roles(self):
        roles = []
        user = self.request.user
        roles.extend(user.get_roles())
        id = self.request.matchdict['id']

        if int(id) in user.content_ids:
            roles.append(Owner)
        return roles

def role_finder(userid, request):
    context = request.context
    return context.get_context_roles()

def get_current_user(request):
    user = unauthenticated_userid(request)
    if user is not None:
        return user

def can_edit(object, request):
    can = False
    if request.user is not None:
        if Admin in request.user.get_roles():
            return True
        can = object.id in request.user.content_ids
    return can


class LoginUser:
    def get_user_name(self):
        return '%s %s' % (self.name, self.lastname)  
        
    def get_roles(self):
        if self.roles:        
            return self.roles.split(',')  
        else: 
            return []    