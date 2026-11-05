from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# one row per tick sighting
class Sighting(Base):
    __tablename__ = "sightings"

    id = Column(Integer, primary_key=True)
    # Elanco's id - unique so the same record can never be saved twice. Empty for user reports
    external_id = Column(String, unique=True)
    date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    species = Column(String, nullable=False)
    latin_name = Column(String, nullable=False)
    source = Column(String, nullable=False)  # "elanco" or "user"
