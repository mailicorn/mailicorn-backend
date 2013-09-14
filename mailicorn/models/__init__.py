from sqlalchmey.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship


_Base = declarative_base()
DBSession = scoped_session(sessionmaker())
