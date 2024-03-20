from sqlalchemy import Column, Integer, DECIMAL, DateTime, ForeignKey
from config.connection.db import Base


class Report(Base):
    __tablename__ = "report"

    id = Column(Integer, primary_key=True)
    data = Column(DECIMAL)
    date = Column(DateTime)
    sensor_id = Column(Integer, ForeignKey("sensor.id"))

