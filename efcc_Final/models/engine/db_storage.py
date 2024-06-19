#!/usr/bin/python3
""" Our EFCC database """
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.complainant import Complainant
from models.suspect import Suspect
from models.fingerprint import FingerPrint
from models.identity import Identity
from models.petition import Petition
from models.recovery import (Monetary, Bank, Crypto, Cash, Recovery,
                                Electronic, Phone, Laptop, Other,
                                Automobile, Jewelry, LandedProperty)



classes = {"BaseModel": BaseModel, "Complainant": Complainant, "Suspect": Suspect,
            "FingerPrint": FingerPrint, "Identity": Identity, "Petition": Petition,
            "Monetary": Monetary, "Bank": Bank, "Crypto": Crypto, "Cash": Cash,
            "Recovery": Recovery, "Electronic": Electronic, "Phone": Phone,
            "Laptop": Laptop, "Other": Other, "Automobile": Automobile,
            "Jewelry": Jewelry, "LandedProperty": LandedProperty}


class DBStorage:
    """
    A blueprint for the database storage
        Parameters:
        pool_pre_ping: Check if a connection is available first.
        Always delete the engines if its just for testing.
    """

    __engine = None
    __session = None

    def __init__(self):
        """An instantiator for the database"""
        username = getenv("EFCC_MYSQL_USER")
        password = getenv("EFCC_MYSQL_PWD")
        host = getenv("EFCC_MYSQL_HOST")
        db_name = getenv("EFCC_MYSQL_DB")

        # db_url = "mysql+pymsql://{}:{}@{}/{}".format(username, password,
        #                                              host, db_name)
        db_url = "sqlite:///databases/efcc_db.db"
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if getenv("EFCC_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
            Return dict of object of a particular class if specified,
            otherwise return the list of object for all the tables i.e
            all subclasses of the Base class.
        """
        obj_list = []
        if cls and isinstance(cls, str):
            try: 
                cls = globals()[cls]
                obj_list = self.__session.query(cls).all()
            except Exception:
                pass
        elif cls and issubclass(cls, Base):
            obj_list = self.__session.query(cls).all()
        else:
            for subclass_ in Base.__subclasses__():
                obj_ = self.__session.query(subclass_).all()
                obj_list.extend(obj_)

        final_dict = {}
        for obj in obj_list:
            key_ = "{}.{}".format(obj.__class__.__name__, obj.id)
            final_dict[key_] = obj

        return final_dict

    def new(self, obj): 
        """add the object to the current database session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session (self.__session)"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        self.__session.delete(obj)

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def reload(self):
        """
            Create all tables in the database (feature of SQLAlchemy).
            Reset the database schema and allows for easy refresh.
            It simply accomodate dynamic changes
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def count(self, cls=None):
        """
            Counts the number of occurence of an object
        """
        if not cls:
            all_ = self.all()
            return len(all_)
        for class_, value in classes.items():
            if cls == class_ or cls == value:
                everything = self.all(cls)
                return len(everything)
        if cls not in classes.values():
            return

    def get(self, cls, id):
        """Retrieves the object of a specific class, otherwise all objects"""
        if cls and id:
            if cls in classes.values() and isinstance(id, str):
                specific_obj = self.all(cls)
                for v in specific_obj.values():
                    if v.id == id:
                        return v
            elif cls in classes and isinstance(id, str):
                cls = eval(cls)
                specific_obj = self.all(cls)
                for v in specific_obj.values():
                    if v.id == id:
                        return v
            else:
                return
        else:
            return