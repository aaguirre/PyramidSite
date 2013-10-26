import gevent
import random
import base64

from datetime import datetime, date

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def get_salt():
    now = datetime.now()
    date = base64.b64encode(now.strftime('%d%b%Y%H%M%S'))
    return date + '-' + ''.join(random.choice(ALPHABET) for i in range(27))


def random_password():
    return ''.join(random.choice(ALPHABET) for i in range(6))

def greenlet(fn):
    def wrapped(*args):
        g = gevent.Greenlet(fn, *args)
        g.start()
    return wrapped