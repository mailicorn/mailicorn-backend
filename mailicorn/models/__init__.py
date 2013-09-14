from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine


_Base = declarative_base()
DBSession = scoped_session(sessionmaker())


def GimmieDatDB(config):
    engine = create_engine(config.get('app:main', 'sqlalchemy.uri'))
    DBSession.configure(bind=engine)
    _Base.metadata.bind = engine


def create_test_user():
    import sys
    from ConfigParser import ConfigParser
    import getpass
    from mailicorn.models.users import User
    from mailicorn.models.accounts import Account, Folder
    import hashlib
    config = ConfigParser()
    config.read(sys.argv[1])
    engine = create_engine(config.get('app:main', 'sqlalchemy.uri'))
    DBSession.configure(bind=engine)
    _Base.metadata.bind = engine
    username = raw_input('Username: ')
    password = getpass.getpass('Password: ')
    email = raw_input('Email: ')
    imap_pass = getpass.getpass('Imap pass: ')
    host = raw_input('host: ')
    port = int(raw_input('port: '))

    new_user = User(email=email,
                    name=username,
                    password=hashlib.sha512(password).hexdigest(),
                    )
    folder = Folder(name='INBOX')
    new_acc = Account(
        username=email,
        password=imap_pass,
        host=host,
        port=port,
        imap_root='',
        seperator='/',
        sync_int=500,
        ssl=False,
    )
    new_acc.folders = [folder, ]
    new_user.accounts = [new_acc, ]
    DBSession.add(new_user)
    DBSession.commit()


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    _Base.metadata.bind = engine
    _Base.metadata.drop_all()
    _Base.metadata.create_all(engine, checkfirst=False)
    from mailicorn.models.users import User
    from mailicorn.models.accounts import Account, Folder
    import hashlib
    new_user = User(email='sterling@isis.com',
                    name='archer',
                    password=hashlib.sha512('herpderp').hexdigest(),
                    )
    folder = Folder(name='INBOX')
    new_acc = Account(
        username='sterling@isis.com',
        password='thisisntapassword',
        host='localhost',
        port=666,
        imap_root='',
        seperator='/',
        sync_int=500,
        ssl=True,
    )
    new_acc.folders = [folder, ]
    new_user.accounts = [new_acc, ]
    DBSession.add(new_user)
    DBSession.commit()
