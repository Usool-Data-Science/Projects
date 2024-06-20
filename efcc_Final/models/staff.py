# from api.v1.app import login_manager
from datetime import datetime
# from flask_login import UserMixin
from models.base_model import BaseModel, Base
from sqlalchemy import Column, DateTime, String, Integer, Enum
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import  relationship
from sqlalchemy.dialects.mysql import VARCHAR
from os import getenv

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

nigeria_states = ("Abia", "Abuja", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi",
                  "Bayelsa", "Benue", "Borno", "Cross River", "Delta",
                  "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo",
                  "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi",
                  "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger",
                  "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers",
                  "Sokoto", "Taraba", "Yobe", "Zamfara")


association_pet_staff = Table("petition_staff", Base.metadata,
                         Column("petition_id", ForeignKey("petitions.id"),
                         primary_key=True, nullable=False),
                         Column("staff_id", ForeignKey("staffs.id"),
                         primary_key=True, nullable=False))

# Create the database models
class Staff(BaseModel, Base):
    """A Staff object that defines each Efcc staff features"""

    __tablename__ = 'staffs'
    name = Column(String(128), nullable=False)
    address = Column(VARCHAR(128), nullable=False)
    state = Column(Enum(*nigeria_states), nullable=False)
    gender = Column(Enum('Male', 'Female'), nullable=False)
    age = Column(Integer, nullable=False)
    religion = Column(Enum('Islam', 'Christianity',
                           'Traditional', 'Others'),
                      nullable=False)
    education = Column(Enum('Primary', 'Secondary',
                            'Tertiary'),
                       nullable=False)
    phone_no = Column(VARCHAR(15), nullable=False)
    petition_ids = []

    # Relationships
    if getenv("EFCC_TYPE_STORAGE") == "db":
        petitions = relationship("Petition", secondary="petition_staff", viewonly=False, back_populates="staffs")

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