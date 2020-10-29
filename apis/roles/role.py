from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.exc import *
from ..db_utils import DbInstance
__db = DbInstance.getInstance()

class Role(__db.Base):
    __tablename__ = "role"
    idRole = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(255))

    constraints = list()
    if len(constraints) > 0:
        __table_args__ = tuple(constraints)

    def __init__(self, dictModel):
        if ("idRole" in dictModel) and (dictModel["idRole"] != None):
            self.idRole = dictModel["idRole"]
        if ("name" in dictModel) and (dictModel["name"] != None):
            self.name = dictModel["name"]
        if ("description" in dictModel) and (dictModel["description"] != None):
            self.description = dictModel["description"]

    def __repr__(self):
        return '<Role idRole={} name={} description={} >'.format(self.idRole, self.name, self.description, )

    def json(self):
        return {
            "idRole": self.idRole, "name": self.name, "description": self.description,
        }

    def update(self, dictModel):
        if ("idRole" in dictModel) and (dictModel["idRole"] != None):
            self.idRole = dictModel["idRole"]
        if ("name" in dictModel) and (dictModel["name"] != None):
            self.name = dictModel["name"]
        if ("description" in dictModel) and (dictModel["description"] != None):
            self.description = dictModel["description"]