#!.venv/bin/python3

from sqlalchemy import create_engine

import config
from models import Base

engine = create_engine(f"sqlite:///{config.catalogue_db_path}", echo=True)

Base.metadata.drop_all(engine)
