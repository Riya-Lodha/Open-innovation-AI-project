from datetime import datetime
from database.sqllite_connection import Base
from sqlalchemy import Column, Float, Integer, BLOB, DateTime


class Image(Base):
    __tablename__ = "Images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    depth = Column(Float, nullable=False)
    pixels = Column(BLOB, nullable=False)
    uploaded_on = Column(DateTime, default=datetime.utcnow)
