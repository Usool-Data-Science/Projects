#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
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

class_list = ["BaseModel", "Complainant", "Suspect", "FingerPrint",
              "Identity", "Petition", "Monetary", "Bank", "Crypto", "Cash",
              "Recovery", "Electronic", "Phone", "Laptop", "Other", "Automobile",
              "Jewelry", "LandedProperty"]


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'databases/file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Args:
            cls (optional class), if specified will filter the
            result for only the cls class.
        Returns a dictionary of models currently in storage
        """
        if cls:
            if isinstance(cls, str):
                cls = globals().get(cls)
            if cls and issubclass(cls, BaseModel):
                cls_dict = {k: v for k,
                    v in self.__objects.items() if isinstance(v, cls)}
                return cls_dict
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def close(self):
        """Reloads the file"""
        self.reload()

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except Exception:
            pass

    def delete(self, obj=None):
        """
            Deletes an object instance from the storage
            Using the key i.e. [Class_name].obj_id
        """
        if not obj:
            return 
        obj_key = f"{obj.__class__.__name__}.{obj.id}"

        try:
            del self.__objects[obj_key]
        except Exception:
            pass

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
            if cls in classes.values and isinstance(id, str):
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
    
    def get_by_feature(self, cls, attribute, value):
        """Returns an instance with a unique feature"""
        if cls and attribute:
            """If the class is provided as a python class instance"""
            if cls in classes.values() and isinstance(attribute, str):
                specific_obj = self.all(cls).values()
                for obj in specific_obj:
                    if attribute in obj.to_dict() and obj.to_dict().get(attribute) == value:
                        return obj
            elif cls in classes and isinstance(attribute, str):
                """If the class is provided as a string instead of class instance"""
                cls = eval(cls.title())
                specific_obj = self.all(cls).values()
                for obj in specific_obj:
                    if attribute in obj.to_dict() and obj.to_dict().get(attribute) == value:
                        return obj
            else:
                return
        else:
            return