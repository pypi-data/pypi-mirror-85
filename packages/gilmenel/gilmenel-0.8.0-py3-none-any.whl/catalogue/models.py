import math

# models created from: http://bytefish.de/blog/first_steps_with_sqlalchemy/

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Index,
    inspect,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import (
    as_declarative,
    declarative_base,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship


# returns a row as a dictionary
@as_declarative()
class Base:
    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Catalog(Base):
    __tablename__ = 'catalogs'

    catalog_id = Column(Integer(), unique=True, primary_key=True)
    name = Column(String(20))
    prefix = Column(String(20))


class Source(Base):

    __tablename__ = 'sources'

    # Columns
    # -------
    # source
    # ra
    # dec
    # g_mag
    # rp_mag

    source_id = Column(Integer(), unique=True, primary_key=True)
    catalog_id = Column(Integer(), ForeignKey('catalogs.catalog_id'))
    catalog = relationship("Catalog")
    source = Column(String(20))
    ra = Column(Float())
    dec = Column(Float())
    g_mag = Column(Float())
    rp_mag = Column(Float())

    @hybrid_property
    def ra_square(self):
        return int(math.floor(self.ra))

    @hybrid_property
    def dec_square(self):
        return int(math.floor(self.dec)) + 90

    @hybrid_property
    def ra_deg_dist(self):
        return int(math.floor(self.ra % 1 * 100))

    @hybrid_property
    def dec_deg_dist(self):
        return int(math.floor(self.dec % 1 * 100))

    @hybrid_property
    def source_name(self):
        return f"{self.catalog.prefix}{self.source}"

    def __repr__(self):
        return (
            f"<Source ("
            f"id='{self.source_id}', "
            f"source='{self.source}', "
            f"ra='{self.ra}', "
            f"dec='{self.dec}', "
            f"g_mag='{self.g_mag}', "
            f"rp_mag='{self.rp_mag}'"
            f")>"
        )

    def create_indexes(engine):
        # indexes
        sources_ra_index = Index('sources_ra_idx', Source.ra)
        sources_dec_index = Index('sources_dec_idx', Source.dec)
        sources_gmag_index = Index('sources_gmag_idx', Source.g_mag)

        sources_ra_index.create(bind=engine)
        sources_dec_index.create(bind=engine)
        sources_gmag_index.create(bind=engine)


# constants
GAIA_DR2 = Catalog(name="Gaia DR2", prefix="Gaia DR2 ")
