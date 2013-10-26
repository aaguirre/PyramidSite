import transaction

from pyramidsite.interfaces import IMailSender
from jinja2 import Environment, PackageLoader

from pyramid_mailer import get_mailer, mailer_factory_from_settings

from pyramid_mailer.message import Message
from pyramid.settings import aslist

from zope.interface import implements

import logging
logger = logging.getLogger(__name__)

class MailHost(object):
    """ Wrapper for pyramid_mailer which adds the feature of
        apply a template for each email
    """

    implements(IMailSender)

    def __init__(self, settings ):
        self.settings = settings
        #self.mailer = get_mailer(config.registry)
        self.mailer = mailer_factory_from_settings(settings)

    def render_template(self, template, kwargs):
        package_name = aslist(self.settings['jinja2.directories'])[0].split(':')[0]
        env = Environment(loader=PackageLoader(package_name,'templates'))
        template = env.get_template(template)
        result =  template.render(kwargs)
        result = result.replace('\n','')
        return result

    def send_simple(self, subject, to, template, **kwargs):
        message = Message(subject=subject,
                          recipients=[to],
                          html= self.render_template(template, kwargs),
                          sender = self.settings['mail.default_sender'],
                          extra_headers = dict(From=self.settings['mail.from'])
        )
        self.mailer.send_immediately(message,fail_silently=False)
        #transaction.commit()


