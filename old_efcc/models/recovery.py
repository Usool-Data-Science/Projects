#!/usr/bin/python3
""" State Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import (Column, DateTime, String,
                        Integer, Enum, ForeignKey)
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import  relationship
from sqlalchemy.types import BLOB
from os import getenv

recovery_statuses = ('With Exhibit keeper', 'Tendered in Court',
                    'Interim forfeiture', 'Final Forfeiture')

top_currencies = ("USD", "EUR", "CNY", "JPY", "GBP", "AUD", "CAD", "CHF",
                  "INR", "KRW", "RUB", "BRL", "HKD", "SEK", "SGD", "TRY",
                  "MXN", "NZD", "ZAR", "NOK")



class Recovery(BaseModel, Base):
    """A fingerprint object that defines each suspects fingerprint"""
    
    __tablename__ = 'recoveries'
    petition_id = Column(String(50), ForeignKey('petitions.casefile_no'), nullable=False)
    suspect_id = Column(Integer, ForeignKey('suspects.id'), nullable=False)
    
    # Relationships
    if getenv("EFCC_TYPE_STORAGE") == "db":
        monetaries = relationship('Monetary', backref='recovery', cascade="all, delete-orphan")
        automobilies = relationship('Automobile', backref='recovery', cascade="all, delete-orphan")
        electronics = relationship('Electronic', backref='recovery', cascade="all, delete-orphan")
        jewelries = relationship('Jewelry', backref='recovery', cascade="all, delete-orphan")
        landedproperties = relationship('LandedProperty', backref='recovery', cascade="all, delete-orphan")

    else:
        @property
        def monetaries(self):
            monetary_list = []
            for id_ in models.storage.all(Monetary):
                if id_.recovery_id == self.id:
                    monetary_list.append(id_)
            return monetary_list
        @property
        def automobilies(self):
            automobile_list = []
            for id_ in models.storage.all(Automobile):
                if id_.recovery_id == self.id:
                    automobile_list.append(id_)
            return automobile_list
        @property
        def electronics(self):
            electonic_list = []
            for id_ in models.storage.all(Electronic):
                if id_.recovery_id == self.id:
                    electonic_list.append(id_)
            return electonic_list
        @property
        def jewelries(self):
            jewelry_list = []
            for id_ in models.storage.all(Jewelry):
                if id_.recovery_id == self.id:
                    jewelry_list.append(id_)
            return jewelry_list
        @property
        def landedproperties(self):
            lnd_list = []
            for id_ in models.storage.all(LandedProperty):
                if id_.recovery_id == self.id:
                    lnd_list.append(id_)
            return lnd_list

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)

# Monetary Recoveries
class Monetary(BaseModel, Base):
    """A table that contains features of monetary recoveries"""
    __tablename__ = 'monetaries'
    status = Column(Enum(*recovery_statuses), nullable=False)
    recovery_id = Column(Integer, ForeignKey('recoveries.id'))

    # Relationships
    if getenv("EFCC_TYPE_STORAGE") == "db":
        banks = relationship('Bank', backref='monetary', cascade="all, delete-orphan")
        cryptos = relationship('Crypto', backref='monetary', cascade="all, delete-orphan")
        cashes = relationship('Cash', backref='recovery', cascade="all, delete-orphan")

    else:
        @property
        def banks(self):
            bank_list = []
            for id_ in models.storage.all(Bank):
                if id_.monetary_id == self.id:
                    bank_list.append(id_)
            return bank_list
        
        @property
        def cryptos(self):
            crypto_list = []
            for id_ in models.storage.all(Crypto):
                if id_.monetary_id == self.id:
                    crypto_list.append(id_)
            return crypto_list
        @property
        def cashes(self):
            cash_list = []
            for id_ in models.storage.all(Cash):
                if id_.monetary_id == self.id:
                    cash_list.append(id_)
            return cash_list

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)

class Bank(BaseModel, Base):
    """Blueprint of Bank monetary recoveries"""

    __tablename__ = 'bank'
    bank_name = Column(String(50))
    serial_number = Column(Integer)
    amount = Column(Integer, autoincrement=False)
    favour_off = Column(String(20))
    monetary_id = Column(Integer, ForeignKey('monetaries.id'), nullable=False)

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)

class Crypto(BaseModel, Base):
    """Blueprint of crypto recoveries"""

    __tablename__ = 'crypto'
    asset_name = Column(String(50))
    asset_size = Column(String(50))
    asset_worth = Column(Integer)
    monetary_id = Column(Integer, ForeignKey('monetaries.id'), nullable=False)

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)

class Cash(BaseModel, Base):
    """Blueprint for cash recovered"""

    __tablename__ = 'cash'
    denomination = Column(Enum(*top_currencies), nullable=False)
    amount = Column(Integer, nullable=False)
    monetary_id = Column(Integer, ForeignKey('monetaries.id'))

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)

# Automobile Recoveries
class Automobile(BaseModel, Base):
    """A table that contains features of automobile recoveries"""
    
    __tablename__ = 'automobile'
    description = Column(String(200))
    plate_number = Column(VARCHAR(10))
    chasis_number = Column(VARCHAR(50))
    colar = Column(String(20))
    other_info = Column(VARCHAR(128))
    status = Column(Enum(*recovery_statuses), nullable=False)
    recovery_id = Column(Integer, ForeignKey('recoveries.id'), nullable=False)

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)


# Electronic Recoveries
class Electronic(BaseModel, Base):
    """A table that contains features of electronic recoveries"""

    __tablename__ = 'electronics'
    status = Column(Enum(*recovery_statuses), nullable=False)
    recovery_id = Column(Integer, ForeignKey('recoveries.id'), nullable=False)
    
    # Relationships
    if getenv("EFCC_TYPE_STORAGE") == "db":
        phones = relationship('Phone', backref='electronic', cascade="all, delete-orphan")
        laptops = relationship('Laptop', backref='electronic', cascade="all, delete-orphan")
        others = relationship('Other', backref='electronic', cascade="all, delete-orphan")

    else:
        @property
        def phones(self):
            phone_list = []
            for id_ in models.storage.all(Phone):
                if id_.electronic_id == self.id:
                    phone_list.append(id_)
            return phone_list

        def laptops(self):
            laptop_list = []
            for id_ in models.storage.all(Laptop):
                if id_.electronic_id == self.id:
                    laptop_list.append(id_)
            return laptop_list
        
        def others(self):
            other_list = []
            for id_ in models.storage.all(Other):
                if id_.electronic_id == self.id:
                    other_list.append(id_)
            return other_list


    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)

class Phone(BaseModel, Base):
    """Blueprint of phone recoveries"""

    __tablename__ = 'phones'
    phone_name = Column(String(50), nullable=False)
    color = Column(String(20))
    imei = Column(VARCHAR(50))
    electronic_id = Column(Integer, ForeignKey('electronics.id'))

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)

class Laptop(BaseModel, Base):
    """Blueprint for laptop recoveries"""

    __tablename__ = 'laptop'
    serial_no = Column(VARCHAR(50), nullable=False)
    color = Column(String(20))
    name = Column(String(50))
    electronic_id = Column(Integer, ForeignKey('electronics.id'))

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)

class Other(BaseModel, Base):
    """Blueprint for other recoveries"""

    __tablename__ = 'other'
    description = Column(String(128))
    electronic_id = Column(Integer, ForeignKey('electronics.id'))

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)

# Jewelry Recoveries
class Jewelry(BaseModel, Base):
    """A table that contains feautures of jewelry recoveries"""

    __tablename__ ='jewelry'
    name = Column(String(50), nullable=False)
    description = Column(String(128))
    status = Column(Enum(*recovery_statuses), nullable=False)
    recovery_id = Column(Integer, ForeignKey('recoveries.id'), nullable=False)

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)


# Landed Properties Recovery
class LandedProperty(BaseModel, Base):
    """A table that contains features of landed properties recoveries"""

    __tablename__ = 'landedproperty'
    location = Column(String(50), nullable=False)
    size = Column(Integer, autoincrement=False)
    status = Column(Enum(*recovery_statuses), nullable=False)
    recovery_id = Column(Integer, ForeignKey('recoveries.id'))

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)