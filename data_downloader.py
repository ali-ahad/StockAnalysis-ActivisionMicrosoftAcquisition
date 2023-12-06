from typing import List, Dict
from models import Category, Company, DailyData
from database_helper import DatabaseHelper

import yfinance as yf
import pandas as pd
import logging


class DataDownloader:
    def __init__(self, categorized_stocks_dict: Dict[str, List[Dict[str, str]]], start_date: str, end_date: str, db_helper: DatabaseHelper) -> None:
        self.__categorized_stocks_dict = categorized_stocks_dict
        self.__start_date = start_date
        self.__end_date = end_date
        self.__db_helper = db_helper
        
    def download_individual_stock_daily_market_data(self, ticker: str, category_id: int):
        logging.info(f"Downloading daily stock prices for {ticker}")
        
        # add company to the database
        company_name = yf.Ticker(ticker).info.get("longName")
        self.__db_helper.insert_company(ticker, company_name)
        
        # get category object
        category_obj = self.__db_helper.get_category_object_by_id(category_id)
        
        # Fetch historical data
        try:
            df = yf.download(ticker, start=self.__start_date,
                             end=self.__end_date, interval="1d")

            # Add a symbol column
            df["Ticker"] = ticker

            # Drop Adj Close column
            df.drop("Adj Close", axis=1, inplace=True)

            # Create a list of DailyData objects
            # and insert them into the database
            daily_data_list = []

            for index, row in df.iterrows():
                daily_data_list.append(DailyData(
                    category_id=category_obj.id,
                    ticker=ticker, 
                    date=index, 
                    open=row["Open"], 
                    high=row["High"], 
                    low=row["Low"], 
                    close=row["Close"], 
                    volume=row["Volume"]
                ))

            self.__db_helper.insert_daily_data_list(daily_data_list, ticker)

        except Exception as e:
            logging.error(
                f"Error downloading data for {ticker}: {e}")
            return
        
    def download_daily_market_data(self):
        for category_name, stock_list in self.__categorized_stocks_dict.items():
            
            # fetch the category object
            # if it doesn't exist, create it and insert it into the database
            category = self.__db_helper.get_category_object_by_name(category_name)
            if category is None:
                self.__db_helper.insert_category(category_name)
                category = self.__db_helper.get_category_object(category_name)
            
            logging.info(f"Processing {category_name}")
            for stock in stock_list:
                company = stock.get("Company")
                ticker = stock.get("Ticker")
                
                # add company to the database
                self.__db_helper.insert_company(ticker, company)

                logging.info(
                    f"Downloading daily stock prices for {company}-{ticker}")

                # Fetch historical data
                try:
                    df = yf.download(ticker, start=self.__start_date,
                                     end=self.__end_date, interval="1d")

                    # Add a symbol column
                    df["Ticker"] = ticker

                    # Drop Adj Close column
                    df.drop("Adj Close", axis=1, inplace=True)
                    
                    # Create a list of DailyData objects
                    # and insert them into the database
                    daily_data_list = []
                    
                    for index, row in df.iterrows():
                        daily_data_list.append(DailyData(
                            category_id=category.id, 
                            ticker=ticker, 
                            date=index, 
                            open=row["Open"], 
                            high=row["High"], 
                            low=row["Low"], 
                            close=row["Close"], 
                            volume=row["Volume"]
                        ))
                    
                    self.__db_helper.insert_daily_data_list(daily_data_list, ticker)
                    
                except Exception as e:
                    logging.error(
                        f"Error downloading data for {company}-{ticker}: {e}")
                    continue
