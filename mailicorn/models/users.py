from mailicorn.models import _Base
from sqlalchemy import Integer, Unicode, Column
from sqlalchemy.orm import relationship


class User(_Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))
    password = Column(Unicode(255))
    rules = relationship("Rule")
    accounts = relationship("Account")

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'rules': [r.to_dict() for r in self.rules],
                'accounts': [a.to_dict() for a in self.accounts]
                }
