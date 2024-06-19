#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
# from sqlalchemy.types import BLOB

class FingerPrint(BaseModel, Base):
    """A fingerprint object that defines each suspects fingerprint"""
    __tablename__ = 'fingerprints'
    finger_print = Column(String(128))
    mugshot = Column(String(128)) # Change this later to BLOB
    suspect_id = Column(Integer, ForeignKey('suspects.id'))

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)
