import base64
import hashlib
import logging

from collections import OrderedDict


from pyramidsite.security import LoginUser
from pyramidsite.utils import get_salt, random_password

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.interfaces import PoolListener
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    Boolean,
    or_,
    Table,
    Index,
    )

from datetime import datetime 

from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  relationship, backref, relation, joinedload
from sqlalchemy.sql.expression import desc, asc

DBSession = scoped_session(sessionmaker(autocommit=True, autoflush=True))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


class Common(object):
    def save(self):
        DBSession.add(self)
        DBSession.flush()

    def update(self):
        DBSession.begin()
        DBSession.merge(self)
        DBSession.commit()

    @classmethod
    def get(cls, id):
        return DBSession.query(cls).get(id)


    @classmethod
    def remove(cls, id):
        return DBSession.query(cls).filter(cls.id == id).delete()
        

    @classmethod
    def delete(cls, id):
        return DBSession.query(cls).filter(cls.id == id).delete()

    @classmethod
    def all(cls):
        return DBSession.query(cls).all()

    @classmethod
    def all_desc(cls):
        return DBSession.query(cls).order_by(desc(cls.id)).all()


    row2dict = lambda r: {c.name: getattr(r, c.name) for c in r.__table__.columns}



class User(Base, Common):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    lastname = Column(String(100))
    password = Column(String(64))
    enabled = Column(Boolean(), nullable=False, default=True, index=True)
    email = Column(String(40), default=u"", index=True)
    roles = Column(String(100))

    salt = Column(String(256))
    date = Column(DateTime, default=datetime.now)
    last_access = Column(DateTime)

    def save(self):
        DBSession.add(self)
        DBSession.flush()

    def update(self):
        DBSession.merge(self)


    @classmethod
    def get_user_by_username(cls, username):
        return DBSession.query(cls).filter(cls.username == username).first()

    @classmethod
    def get_user_by_email(cls, email):
        return DBSession.query(cls).filter(cls.email == email).first()


    @classmethod
    def get_user_by_id(cls, id):
        return DBSession.query(cls).get(id)

    def get_author_page(self):
        return '/author/%s' % self.username

    @classmethod
    def email_exists(cls, email, current_email=None):
        user = DBSession.query(cls).filter(cls.email == email).first()
        if user and user.email == current_email:
            return False
        else:
            return user is not None


    @classmethod
    def username_exists(cls, username):
        user = DBSession.query(cls).filter(cls.username == username).first()
        return user is not None


    @classmethod
    def recover_password(cls, email):
        user = cls.get_user_by_email(email)
        user.salt = get_salt()
        user.update()
        return user

    def validate_salt(self):
        salt_time = self.salt.split('-')[0]
        decoded_salt_time = base64.b64decode(salt_time)
        date_object = datetime.strptime(decoded_salt_time, '%d%b%Y%H%M%S')
        delta = datetime.now() - date_object
        return delta.total_seconds() < 28800

    @classmethod
    def get_user_by_salt(cls, salt):
        return DBSession.query(cls).filter(cls.salt == salt).first()

    def set_password(self):
        password = random_password()
        self.password = self.encrypt_password(password)
        return password

    def get_user_id(self):
        return self.username

    def encrypt_password(self, text):
        md5 = hashlib.md5()
        md5.update(text)
        return md5.hexdigest()

    def validate_user(self):
        user = DBSession.query(User).filter(User.enabled == 1).filter(User.email == self.email).filter(
            User.password == self.encrypt_password(self.password)).first()
        if user:
            login_user = LoginUser()
            login_user.id = user.id
            login_user.name = user.name
            login_user.lastname = user.lastname
            login_user.email = user.email   
            login_user.roles = user.roles         
            return login_user


    def is_already_registered(self):
        user = DBSession.query(User).filter(
            or_(User.email == self.email, User.username == self.username)).first()
        return user != None


    def get_user_name(self):
        return '%s %s' % (self.name, self.lastname)


    def get_roles(self):        
        return self.roles.split(',')
