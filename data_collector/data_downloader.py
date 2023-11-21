from typing import List, Dict

import yfinance as yf
import pandas as pd
import os
import logging


class DataDownloader:
    def __init__(self, categorized_stocks_dict: Dict[str, List[Dict[str, str]]], start_date: str, end_date: str) -> None:
        self.__categorized_stocks_dict = categorized_stocks_dict
        self.__start_date = start_date
        self.__end_date = end_date

    def download_daily_market_data(self):
        # remove the direct if present
        if os.path.exists("./daily_interval_files"):
            os.system("rm -rf ./daily_interval_files")

        for category, stock_list in self.__categorized_stocks_dict.items():
            category = category.lower().replace(" ", "_")

            logging.info(f"Processing {category}")
            for stock in stock_list:
                company = stock.get("Company").lower().replace(" ", "_")
                ticker = stock.get("Ticker")

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

                    # create the directory if not present
                    os.makedirs(
                        f"./daily_interval_files/{category}", exist_ok=True)

                    # save to csv
                    df.to_csv(
                        f"./daily_interval_files/{category}/{company}-{self.__start_date.replace('-', '')}-{self.__end_date.replace('-', '')}.csv")

                except Exception as e:
                    logging.error(
                        f"Error downloading data for {company}-{ticker}: {e}")
                    continue
