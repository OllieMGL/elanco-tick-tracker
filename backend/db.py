from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

engine = create_engine("sqlite:///ticks.db")  # sets up the connection SQLite
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)  # creates any tables from models.py that don't exist yet
