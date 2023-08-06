#!.venv/bin/python3
'''
To be run after populating the database and before using it for queries.
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from models import Source

engine = create_engine(
    f"sqlite:///{config.catalogue_db_path}", echo=True, pool_pre_ping=True
)

Session = sessionmaker(bind=engine)
session = Session()

# create indexes for Ra, Dec, Gmag
Source.create_indexes(engine)

# commit all wal changes
session.execute('PRAGMA wal_checkpoint;')
# exit wal journal mode
session.execute('PRAGMA journal_mode=delete;')
