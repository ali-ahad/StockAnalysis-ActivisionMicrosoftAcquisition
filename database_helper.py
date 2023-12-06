from sqlalchemy.orm import sessionmaker
from models import Category, Company, DailyData, Base
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from typing import Dict

import logging
import pandas as pd

class DatabaseHelper:
    def __init__(self, db_path: str) -> None:
        self.__db_path = db_path
        self.__session = None
        
    def connect(self):
        engine = create_engine(f"sqlite+pysqlite:///{self.__db_path}")
        engine.connect()
        
        Session = sessionmaker(bind=engine)
        self.__session = Session()
        
        Base.metadata.create_all(engine)

    def insert_categories(self, category_list: str):
        for category in category_list:
            logging.info(f"Adding {category} to the database")
            self.__session.add(Category(name=category))
        self.__session.commit()
        
    def insert_category(self, category_name: str):
        logging.info(f"Adding {category_name} to the database")
        self.__session.add(Category(name=category_name))
        self.__session.commit()
        
    def insert_company(self, ticker: str, name: str):
        try:        
            logging.info(f"Adding {ticker} - {name} to the database")
            self.__session.add(Company(ticker=ticker, name=name))
            self.__session.commit()
        except IntegrityError as e:
            logging.error(f"Error while adding {ticker} - {name} to the database: {e._message()}")
            self.__session.rollback()
        
    def insert_daily_data_list(self, daily_data_list: list, ticker: str):
        logging.info(f"Adding {len(daily_data_list)} daily data records for {ticker} to the database")
        self.__session.add_all(daily_data_list)
        self.__session.commit()
    
    def get_category_object_by_name(self, category_name: str) -> Category:
        return self.__session.query(Category).filter(Category.name == category_name).first()
    
    def get_category_object_by_id(self, category_id: int) -> Category:
        return self.__session.query(Category).filter(Category.id == category_id).first()
    
  
    def get_daily_market_data(self, ticker: str, start_date: str = "", end_date: str = "") -> pd.DataFrame:
        if start_date == "" and end_date == "":
            data = self.__session.query(DailyData).filter(DailyData.ticker == ticker).all()
        elif start_date != "" and end_date == "":
            data = self.__session.query(DailyData).filter(DailyData.ticker == ticker, DailyData.date >= start_date).all()
        elif start_date == "" and end_date != "":
            data = self.__session.query(DailyData).filter(DailyData.ticker == ticker, DailyData.date <= end_date).all()
        else:
            data = self.__session.query(DailyData).filter(DailyData.ticker == ticker, DailyData.date >= start_date, DailyData.date <= end_date).all()

        return pd.DataFrame([row.__dict__ for row in data]).drop(["_sa_instance_state"], axis=1).sort_values(by="date") 

    def get_categories(self) -> pd.DataFrame:
        data = self.__session.query(Category).all()
        return pd.DataFrame([row.__dict__ for row in data]).drop(["_sa_instance_state"], axis=1).sort_values(by="name")
    
    def get_stocks_by_category_id(self, category_id: int) -> Dict[str, pd.DataFrame]:
        data = self.__session.query(DailyData).filter(DailyData.category_id == category_id).all()
        
        # convert to dataframe
        df = pd.DataFrame([row.__dict__ for row in data]).drop(["_sa_instance_state"], axis=1).sort_values(by="date")
        
        # group by ticker
        grouped = df.groupby("ticker")
        
        # create a dictionary of dataframes
        stocks_dict = {}
        for ticker, data in grouped:
            stocks_dict[ticker] = data
        
        return stocks_dict