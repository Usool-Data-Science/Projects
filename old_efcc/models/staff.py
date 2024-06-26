from datetime import datetime
from flask_login import UserMixin
from models.base_model import BaseModel, Base
from sqlalchemy import Column, DateTime, String, Integer, Enum
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import  relationship
from sqlalchemy.dialects.mysql import VARCHAR
from os import getenv
from api.v1.app import login_manager

nigeria_states = ("Abia", "Abuja", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi",
                  "Bayelsa", "Benue", "Borno", "Cross River", "Delta",
                  "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo",
                  "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi",
                  "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger",
                  "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers",
                  "Sokoto", "Taraba", "Yobe", "Zamfara") 

# Create the database models
class Staff(BaseModel, Base, UserMixin):
    """A Staff object that defines each Efcc staff features"""

    __tablename__ = 'staffs'
    # staff_no = ''
    # admin_pass = ''
    # location = ''
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(VARCHAR(128), nullable=False, unique=True)
    password = Column(VARCHAR(128), nullable=False)
    age = Column(Integer, nullable=False)
    state = Column(Enum(*nigeria_states), nullable=False)

    petition_ids = []

    # Relationships
    if getenv("EFCC_TYPE_STORAGE") == "db":
        petitions = relationship("Petition", backref="staff", lazy=True)

    else:        
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

    def __repr__(self):
        return f"Staff('{self.first_name}', '{self.last_name}', '{self.id}')"