#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user"""
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes user with hashed password"""
        if "password" in kwargs:
            # Hash the password before storing it
            kwargs["password"] = hashlib.md5(
                    kwargs["password"].encode()).hexdigest()
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new_password):
        """Hash the new password before storing"""
        self.__password = hashlib.md5(
                new_password.encode()).hexdigest()
