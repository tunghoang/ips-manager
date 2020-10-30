from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from ..db_utils import DbInstance
__db = DbInstance.getInstance()

class User(__db.Base):
    __tablename__ = "user"
    idUser = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(100))

    constraints = list()
    if len(constraints) > 0:
        __table_args__ = tuple(constraints)

    def __init__(self, dictModel):
        if ("idUser" in dictModel) and (dictModel["idUser"] != None):
            self.idUser = dictModel["idUser"]
        if ("username" in dictModel) and (dictModel["username"] != None):
            self.username = dictModel["username"]
        if ("password" in dictModel) and (dictModel["password"] != None):
            self.password = dictModel["password"]

    def __repr__(self):
        return '<User idUser={} username={} password={} >'.format(self.idUser, self.username, self.password, )

    def json(self):
        return {
            "idUser": self.idUser, "username": self.username
        }

    def update(self, dictModel):
        if ("idUser" in dictModel) and (dictModel["idUser"] != None):
            self.idUser = dictModel["idUser"]
        if ("username" in dictModel) and (dictModel["username"] != None):
            self.username = dictModel["username"]
        if ("password" in dictModel) and (dictModel["password"] != None):
            self.password = dictModel["password"]