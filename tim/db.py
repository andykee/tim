import os

import sqlalchemy


def create_engine():
    if 'TIMDB' in os.environ.keys():
        timdb = os.environ['TIMDB']
    else:
        timdb = os.path.join(os.path.expanduser('~'), '.timdb')
    return sqlalchemy.create_engine(f'sqlite:///{timdb}')


def create_session(engine):
    return sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
