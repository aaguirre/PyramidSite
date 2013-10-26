from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid_beaker import session_factory_from_settings

from pyramidsite.services.mail import MailHost
from pyramidsite.interfaces import IMailSender
from pyramidsite.security import role_finder, get_current_user

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    authn_policy = SessionAuthenticationPolicy('secret_word', callback=role_finder)
    authz_policy = ACLAuthorizationPolicy()
    session_factory = session_factory_from_settings(settings)

    # In case you use MySQL
    # engine = engine_from_config(settings, 'sqlalchemy.',listeners=[MySqlListener()])

    engine = engine_from_config(settings, 'sqlalchemy.')    
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings,
        root_factory='pyramidsite.security.ContentFactory',
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
        session_factory=session_factory)    
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')


    config.set_request_property(get_current_user, 'user', reify=True)
    config.scan()

    # Utilities
    config.registry.registerUtility(MailHost(config.registry.settings), IMailSender)

    # Modules
    config.include('pyramidsite.modules.account')

    return config.make_wsgi_app()
