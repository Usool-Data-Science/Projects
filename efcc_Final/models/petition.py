#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from datetime import datetime
from sqlalchemy import ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy import Column, DateTime, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import  relationship


class Petition(BaseModel, Base):
    """A petition object that defines each petition
         information received from a client.
    """

    __tablename__ = 'petitions'
    casefile_no = Column(String(50), nullable=False)
    cr_no = Column(String(50), nullable=False)
    date_received = Column(DateTime, nullable=False,
                            default=datetime.now())
    date_assigned = Column(DateTime, nullable=False,
                            default=datetime.now())
    amount_involved = Column(Integer, default=0)
    status_signal = Column(Enum('Convicted', 'In-Progress'))
    petition_source = Column(Enum('Intelligence', 'Regular-Complain'))
    recovery_ids = []
    suspect_ids = []
    complainant_ids = []
    staff_ids = []

    # Relationships
    if getenv("EFCC_TYPE_STORAGE") == "db":
        recoveries = relationship("Recovery", cascade="all, delete-orphan", backref="petition")
        suspects = relationship("Suspect", secondary="petition_suspect", viewonly=False, back_populates="petitions")
        complainants = relationship("Complainant", secondary="petition_complainant", viewonly=False, back_populates="petitions")
        staffs = relationship("Staff", secondary="petition_staff", viewonly=False, back_populates="petitions")
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
            if isinstance(value, Recovery) and self.id == value.petition_id:
                self.recovery_ids.append(value.id)
            else:
                print("{} is not a Recovery instance".format(value))
        
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
            if isinstance(value, Suspect) and self.id == value.petition_id:
                self.suspect_ids.append(value.id)
            else:
                print("{} is not a Suspect instance".format(value))

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
            if isinstance(value, Complainant) and self.id == value.petition_id:
                self.complainant_ids.append(value.id)
            else:
                raise TypeError("{} is not a Complainant istance".format(value))
        @property
        def staffs(self):
            import models
            from models.staff import Staff
            all_staffs = models.storage.all(Staff).values()
            staff_list = [stf for stf in all_staffs if stf.id in self.complainant_ids]
            return staff_list

        @staffs.setter
        def staffs(self, value):
            """Checks what goes into petition.staffs and tracks it"""
            if isinstance(value, Staff) and self.id == value.petition_id:
                self.staff_ids.append(value.id)
            else:
                raise TypeError("{} is not a Staff istance".format(value))

    # def __init__(self, *args, **kwargs):
    #     """Initializes the object"""
    #     super().__init__(*args, **kwargs)
