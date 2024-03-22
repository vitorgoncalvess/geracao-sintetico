from config.connection.main_db import Base
from sqlalchemy import Column, Integer, String, DateTime

class Log(Base):
  id = Column(Integer, primary_key=True)

  name = Column(String(90))
  description = Column(String(250))
  sensor_origin = Column(String(90))
  created_at = Column(DateTime)

