#!.venv/bin/python3

import config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import (
    Base,
    GAIA_DR2,
)

engine = create_engine(f"sqlite:///{config.catalogue_db_path}", echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.commit()

session.add(GAIA_DR2)
session.commit()

session.execute('PRAGMA journal_mode=WAL;')
