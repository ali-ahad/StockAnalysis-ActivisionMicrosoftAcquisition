from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
class Company(Base):
    __tablename__ = 'company'

    ticker = Column(String, primary_key=True)
    name = Column(String)

class DailyData(Base):
    __tablename__ = 'daily_data'

    category_id = Column(Integer, ForeignKey("category.id"), primary_key=True)
    ticker = Column(String, ForeignKey("company.ticker"), primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    
    category = relationship("Category")
    company = relationship("Company")
    
    
engine = create_engine(f"sqlite+pysqlite:///marketdata.db")
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

session.add(Category(name="Technology", id=1))

session.commit()