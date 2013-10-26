from zope.interface import Interface

class IPublish(Interface):
    """ Marker intarface to declare if a event has to be published
        in social networks
    """

class IPhotoRepository(Interface):
    """ Service responsible to store photos in a remote
        repository
    """

    def storePhoto(self): pass


class IMailSender(Interface):
    """ Service responsible to send emails.
    """
