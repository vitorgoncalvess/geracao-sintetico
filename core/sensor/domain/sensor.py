from sqlalchemy import Column, Integer, String, DECIMAL
from config.connection.db import Base

class Sensor(Base):
    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True)
    name = Column(String(90))
    min = Column(DECIMAL(10,2))
    max = Column(DECIMAL(10,2))
    offset = Column(DECIMAL(10,2))