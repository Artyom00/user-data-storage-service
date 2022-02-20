from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    other_name = Column(String(50))
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(20))
    birthday = Column(Date)
    city = Column(Integer,
                  ForeignKey('cities.id', onupdate='CASCADE',
                             ondelete='SET NULL'))
    additional_info = Column(String(100))
    is_admin = Column(Boolean, nullable=False)
    password = Column(String(200), nullable=False)


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    users = relationship('User', backref='city_ref')
