from mailicorn.models import _Base, DBSession
from mailicorn.models.rules import Rule
from mailicorn.models.accounts import Account
from sqlalchemy import Integer, Unicode, Column, ForeignKey
from sqlalchemy.orm import relationship


class Message(_Base):
    __tablename__ = 'mids'
    id = Column(Unicode(255), primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))

    @classmethod
    def rules_by_mid(cls, mid):
        msg_query = DBSession.query(Message).filter(Message.id==mid)
        if msg_query.count() == 0:
            return None
        owner_id = msg_query.one().owner_id
        owner_query = DBSession.query(User).filter(User.id==owner_id)
        if owner_query.count() == 0:
            return None
        return owner_query.one().rules


class User(_Base):
    __tablename__ = "users"

    id = Column(Integer, unique=True, primary_key=True)
    email = Column(Unicode(255))
    name = Column(Unicode(255))
    password = Column(Unicode(255))
    rules = relationship("Rule", backref="user")
    accounts = relationship("Account", backref="user")
    messages = relationship("Message", backref="user")


    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'email': self.email,
                'rules': [r.to_dict() for r in self.rules],
                'accounts': [a.to_dict() for a in self.accounts],
                'mids': [m.id for m in self.messages]
                }
