from sqlalchemy import Column, Float, Integer, BLOB
from database.sqllite_connection import Base


class Image(Base):
    __tablename__ = 'Images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    depth = Column(Float, unique=True, nullable=False)
    pixels = Column(BLOB, nullable=False)
