from sqlalchmey.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


_Base = declarative_base()
DBSession = scoped_session(sessionmaker())

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    _Base.metadata.bind = engine
    _Base.metadata.drop_all()
    _Base.metadata.create_all(engine, checkfirst=False)

