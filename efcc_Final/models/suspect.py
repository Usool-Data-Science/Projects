#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, ForeignKey
from sqlalchemy import Column, DateTime, String, Integer, Enum
from sqlalchemy.orm import  relationship
from sqlalchemy.types import BLOB
from os import getenv

nigeria_skin_colors = ('Dark Brown', 'Brown', 'Light Brown',
                                           'Dark', 'Fair', 'Caramel')
religion_types = ('Islam', 'Christianity', 'Traditional', 'Others')
offence_types = ("False Pretence", "Impersonation", "Forgery", "Conspiracy",
           "Aiding and Abetting", "Stealing", "Theft", "Bribery", "Tax Evasion")


association_pet_susp = Table("petition_suspect", Base.metadata,
                         Column("petition_id", ForeignKey("petitions.id"),
                         primary_key=True, nullable=False),
                         Column("suspect_id", ForeignKey("suspects.id"),
                         primary_key=True, nullable=False))

association_feud = Table("complainant_suspect", Base.metadata,
                         Column("complainant_id", ForeignKey("complainants.id"),
                         primary_key=True, nullable=False),
                         Column("suspect_id", ForeignKey("suspects.id"),
                         primary_key=True, nullable=False))

class Suspect(BaseModel, Base):
    """A suspect object that defines each suspects features"""  
    
    __tablename__ = 'suspects'
    name = Column(String(128), nullable=False)
    height = Column(Integer, nullable=False)
    skin_color = Column(Enum(*nigeria_skin_colors), default='Dark')
    passport = Column(String, nullable=False)
    mugshot = Column(String, nullable=False)
    address = Column(String(50), nullable=False)
    nationality = Column(String(20), default="Nigerian")
    place_of_birth = Column(String(50), nullable=False)
    gender = Column(Enum('Male', 'Female'), nullable=False)
    religion = Column(Enum(*religion_types), nullable=False)
    occupation = Column(String(50), nullable=False)
    phone_no = Column(String(15), nullable=False)
    parent_name = Column(String(50), nullable=False)
    offence = Column(Enum(*offence_types), nullable=False)
    recovery_ids = []
    petition_ids = []
    complainant_ids = []
    

    # Relationships

    """
        If the storage type is db, sqlalchemy will handle it with relationship.
        Otherwise(i.e. FileStorage) retrieve all the Identities from the database,
        And filter out only those that have id equal to the id of our current object.
    """

    # Relationships
    if getenv("EFCC_TYPE_STORAGE") == "db":
        identities = relationship('Identity', backref='suspect',
                                  cascade='all, delete-orphan')
        fingerprints = relationship('FingerPrint', backref='suspect',
                                  cascade='all, delete-orphan')
        recoveries = relationship("Recovery", cascade="all, delete-orphan", backref="suspect")
        petitions = relationship("Petition", secondary="petition_suspect", viewonly=False, back_populates="suspects")
        complainants = relationship("Complainant", secondary="complainant_suspect", viewonly=False, back_populates="suspects")
    else:
        @property
        def recoveries(self):
            """
                Specifies what we get when we query petition.recoveries.
                It returns only the recoveries whose id are in the recovery_ids
                that we declared its setter below.
            """
            
            from models.recovery import Recovery
            all_recoveries = models.storage.all(Recovery).values()
            recovery_list = [recov for recov in all_recoveries if recov.id in self.recovery_ids]
            return recovery_list

        @recoveries.setter
        def recoveries(self, value):
            """
            Ensures that what goes into the petition.recoveries are only recovery objects.
            Its also keeps track of the recovery ids into the recovery_ids list.
            """
            if isinstance(value, Recovery):
                self.recovery_ids.append(value.id)
            else:
                print("{} is not a Recovery instance".format(value))
        
        @property
        def petitions(self):
            import models
            from models.petition import Petition
            all_petitions = models.storage.all(Petition).values()
            petition_list = [pet for pet in all_petitions if pet.id in self.petition_ids]
            return petition_list
        
        @petitions.setter
        def petitions(self, value):
            """Checks what goes into suspect.petitions and tracks it"""
            if isinstance(value, Petition):
                self.petition_ids.append(value.id)
            else:
                print("{} is not a Petition instance".format(value))

        @property
        def complainants(self):
            import models
            from models.complainant import Complainant
            all_complainants = models.storage.all(Complainant).values()
            complainant_list = [comp for comp in all_complainants if comp.id in self.complainant_ids]
            return complainant_list

        @complainants.setter
        def complainants(self, value):
            """Checks what goes into petition.complainants and tracks it"""
            if isinstance(value, Complainant):
                self.complainant_ids.append(value.id)
            else:
                print("{} is not a Complainant instance".format(value))


    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)


