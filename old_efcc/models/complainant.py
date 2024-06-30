#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, DateTime, String, Integer, Enum
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import  relationship
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.types import BLOB
from os import getenv

nigeria_states = ("Abia", "Abuja", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi",
                  "Bayelsa", "Benue", "Borno", "Cross River", "Delta",
                  "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo",
                  "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi",
                  "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger",
                  "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers",
                  "Sokoto", "Taraba", "Yobe", "Zamfara")


association_pet_comp = Table("petition_complainant", Base.metadata,
                         Column("petition_id", ForeignKey("petitions.id"),
                         primary_key=True, nullable=False),
                         Column("complainant_id", ForeignKey("complainants.id"),
                         primary_key=True, nullable=False))

class Complainant(BaseModel, Base):
    """A complainant object that defines each complainant features"""

    __tablename__ = 'complainants'
    name = Column(String(128), nullable=False)
    address = Column(VARCHAR(128), nullable=False)
    nationality = Column(String(20), default="Nigerian", nullable=False)
    state = Column(Enum(*nigeria_states), nullable=False)
    gender = Column(Enum('Male', 'Female'), nullable=False)
    age = Column(Integer, nullable=False)
    occupation = Column(String(50), nullable=False)
    religion = Column(Enum('Islam', 'Christianity',
                           'Traditional', 'Others'),
                      nullable=False)
    education = Column(Enum('Primary', 'Secondary',
                            'Tertiary'),
                       nullable=False)
    phone_no = Column(VARCHAR(15), nullable=False)
    suspect_ids = []
    petition_ids = []

    # Relationships
    if getenv("EFCC_TYPE_STORAGE") == "db":
        suspects = relationship("Suspect", secondary="complainant_suspect", viewonly=False, back_populates="complainants")
        petitions = relationship("Petition", secondary="petition_complainant", viewonly=False, back_populates="complainants")

    else:        
        @property
        def suspects(self):
            import models
            from models.suspect import Suspect
            all_suspects = models.storage.all(Suspect).values()
            suspect_list = [susp for susp in all_suspects if susp.id in self.suspect_ids]
            return suspect_list
        
        @suspects.setter
        def suspects(self, value):
            """Checks what goes into petition.suspects and tracks it"""
            if isinstance(value, Suspect):
                self.suspect_ids.append(value.id)
            else:
                print("{} is not a Suspect instance".format(value))

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