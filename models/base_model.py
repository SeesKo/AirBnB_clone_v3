#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
        for key, value in kwargs.items():
            if key == '__class__':
                continue
            setattr(self, key, value)
            if key == 'created_at' and isinstance(value, str):
                self.created_at = datetime.strptime(value, datetime_format)
            if key == 'updated_at' and isinstance(value, str):
                self.updated_at = datetime.strptime(value, datetime_format)

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_password=False):
        """
        Returns a dictionary of the instance,
        excluding the password field
        """
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(
                    "%Y-%m-%dT%H:%M:%S.%f")
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(
                    "%Y-%m-%dT%H:%M:%S.%f")
        new_dict["__class__"] = self.__class__.__name__

        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        if "password" in new_dict and not save_password:
            del new_dict["password"]

        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
