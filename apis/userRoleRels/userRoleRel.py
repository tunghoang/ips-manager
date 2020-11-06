from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from ..db_utils import DbInstance
__db = DbInstance.getInstance()

class Userrolerel(__db.Base):
    __tablename__ = "userRoleRel"
    idUserrolerel = Column(Integer, primary_key = True)
    idRole = Column(Integer, ForeignKey('role.idRole'))
    idUser = Column(Integer, ForeignKey('user.idUser'))

    constraints = list()
    constraints.append(UniqueConstraint('idRole' ,'idUser'))
    if len(constraints) > 0:
        __table_args__ = tuple(constraints)

    def __init__(self, dictModel):
        if ("idUserrolerel" in dictModel) and (dictModel["idUserrolerel"] != None):
            self.idUserrolerel = dictModel["idUserrolerel"]
        if ("idRole" in dictModel) and (dictModel["idRole"] != None):
            self.idRole = dictModel["idRole"]
        if ("idUser" in dictModel) and (dictModel["idUser"] != None):
            self.idUser = dictModel["idUser"]

    def __repr__(self):
        return '<Userrolerel idUserrolerel={} idRole={} idUser={} >'.format(self.idUserrolerel, self.idRole, self.idUser, )

    def json(self):
        return {
            "idUserrolerel" :self.idUserrolerel ,"idRole" :self.idRole ,"idUser" :self.idUser,
        }

    def update(self, dictModel):
        if ("idUserrolerel" in dictModel) and (dictModel["idUserrolerel"] != None):
            self.idUserrolerel = dictModel["idUserrolerel"]
        if ("idRole" in dictModel) and (dictModel["idRole"] != None):
            self.idRole = dictModel["idRole"]
        if ("idUser" in dictModel) and (dictModel["idUser"] != None):
            self.idUser = dictModel["idUser"]
