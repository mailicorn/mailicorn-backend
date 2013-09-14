from mailicorn.models import _Base
from sqlalchemy import Integer, Unicode, Column, ForeignKey, CheckConstraint


RULE_ACTIONS = ('MV', 'RM', 'READ', 'FLAG')


class Rule(_Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True)
    query = Column(Unicode(255))
    action = Column(Unicode(255))
    owner_id = Column(Integer, ForeignKey('users.id'))
    __table_args = (
        CheckConstraint(action in RULE_ACTIONS, name='Only have 4 actions possible')
    )
    destination = Column(Unicode(255))

    def to_dict(self):
        return {'id': self.id,
                'query': self.query,
                'action': self.action,
                'owner_id': self.owner_id,
                'destination': self.destination,
                }

