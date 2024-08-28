from sqlalchemy import Column, Integer, Text, Boolean

from base import Base


class Teddy360(Base):
    __tablename__ = "teddy_360"

    id = Column(Integer, primary_key=True)
    userId = Column(Integer)
    title = Column(Text)
    completed = Column(Boolean)
