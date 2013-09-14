from mailicorn.models import _Base
from sqlalchemy import Integer, Unicode, Column, ForeignKey


class Account(_Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    username = Column(Unicode(255))
    password = Column(Unicode(255))
    host = Column(Unicode(255))
    port = Column(Integer)
    imap_root = Column(Unicode(255))
    seperator = Column(Unicode(255))
    sync_int = Column(Integer) # time in secs between sync jobs

    def to_dict(self):
        return {"id": self.id,
                "owner_id": self.owner_id,
                "username": self.username,
                "host": self.host,
                "port": self.port,
                "imap_root": self.imap_root,
                "seperator": self.seperator,
                "sync_int": self.sync_int
                }
