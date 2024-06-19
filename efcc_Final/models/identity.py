#!/usr/bin/python3
"""This module defines a class Identity"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, DateTime, String, Enum, Integer, ForeignKey
# from sqlalchemy.dialects.mysql import VARCHAR

id_cards = ('Licence', 'NIN', 'Passport')


class Identity(BaseModel, Base):
    """A fingerprint object that defines each suspects fingerprint"""
    
    __tablename__ = 'identities'
    id_types = Column(Enum(*id_cards), nullable=False)
    id_number = Column(Integer, nullable=False)

    # Relationships
    suspect_id = Column(Integer, ForeignKey('suspects.id'), nullable=False)

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)
