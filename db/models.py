from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Double, DateTime
from .database import Base


class Coil(Base):
    __tablename__ = "coils"

    id = Column(Integer, primary_key=True)
    length = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    added = Column(String)
    deleted = Column(String, nullable=True, default=None)

