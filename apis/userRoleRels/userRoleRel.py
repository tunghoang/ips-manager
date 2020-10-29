from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from ..db_utils import DbInstance
__db = DbInstance.getInstance()

class Userrolerel(__db.Base):
    __tablename__ = "userRoleRel"
    idUserRoleRel = Column(Integer, primary_key = True)
    idRole = Column(Integer, ForeignKey('role.idRole'))
    idUser = Column(Integer, ForeignKey('user.idUser'))

    constraints = list()
    constraints.append(UniqueConstraint('idRole' ,'idUser'))
    if len(constraints) > 0:
        __table_args__ = tuple(constraints)

    def __init__(self, dictModel):
        if ("idUserRoleRel" in dictModel) and (dictModel["idUserRoleRel"] != None):
            self.idUserRoleRel = dictModel["idUserRoleRel"]
        if ("idRole" in dictModel) and (dictModel["idRole"] != None):
            self.idRole = dictModel["idRole"]
        if ("idUser" in dictModel) and (dictModel["idUser"] != None):
            self.idUser = dictModel["idUser"]

    def __repr__(self):
        return '<Userrolerel idUserRoleRel={} idRole={} idUser={} >'.format(self.idUserRoleRel, self.idRole, self.idUser, )

    def json(self):
        return {
            "idUserRoleRel" :self.idUserRoleRel ,"idRole" :self.idRole ,"idUser" :self.idUser,
        }

    def update(self, dictModel):
        if ("idUserRoleRel" in dictModel) and (dictModel["idUserRoleRel"] != None):
            self.idUserRoleRel = dictModel["idUserRoleRel"]
        if ("idRole" in dictModel) and (dictModel["idRole"] != None):
            self.idRole = dictModel["idRole"]
        if ("idUser" in dictModel) and (dictModel["idUser"] != None):
            self.idUser = dictModel["idUser"]