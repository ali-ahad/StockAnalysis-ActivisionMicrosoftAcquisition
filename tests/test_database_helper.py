import unittest
from models import Company, DailyData, Base
from sqlalchemy import create_engine
import pandas as pd
from database_helper import DatabaseHelper
from datetime import datetime

class DatabaseHelperTests(unittest.TestCase):
  def setUp(self):
    # Set up a test database
    self.db_path = "test.db"
    self.db_helper = DatabaseHelper(self.db_path)
    self.db_helper.connect()

  def tearDown(self):
    # Clean up the test database
    self.db_helper.get_session.close()
    engine = create_engine(f"sqlite+pysqlite:///{self.db_path}")
    Base.metadata.drop_all(engine)

  def test_insert_category(self):
    # Test inserting a single category
    category_name = "Test Category"
    self.db_helper.insert_category(category_name)
    category = self.db_helper.get_category_object_by_name(category_name)
    self.assertEqual(category.name, category_name)

  def test_insert_categories(self):
    # Test inserting categories into the database
    category_list = ["Category 1", "Category 2", "Category 3"]
    self.db_helper.insert_categories(category_list)

    # Verify that the categories are inserted correctly
    categories = self.db_helper.get_categories()
    category_names = []
    
    for _, row in categories.iterrows():
      category_names.append(row["name"])
    
    # Check if the inserted categories match the expected categories
    expected_category_names = ["Category 1", "Category 2", "Category 3"]
    assert set(category_names) == set(expected_category_names)

  def test_insert_company(self):
    # Test inserting a company
    ticker = "TEST"
    name = "Test Company"
    self.db_helper.insert_company(ticker, name)
    company = self.db_helper.get_session.query(Company).filter(Company.ticker == ticker).first()
    self.assertEqual(company.ticker, ticker)
    self.assertEqual(company.name, name)

  def test_get_daily_market_data(self):
    # Test retrieving daily market data for a ticker
    ticker = "TEST"
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    # Insert some test data
    daily_data = [
        DailyData(category_id=1, ticker=ticker, date=datetime.strptime(start_date, "%Y-%m-%d"), open=10.0, high=10.0, low=10.0, close=10.0, adjust_close=10.2, volume=10.0)
    ]
    self.db_helper.insert_daily_data_list(daily_data, ticker)
    # Retrieve the data
    data = self.db_helper.get_daily_market_data(ticker, start_date, end_date)
    # Check if the data is correct
    expected_data = pd.DataFrame([
        {"date": datetime.strptime(start_date, "%Y-%m-%d").date(), "high": 10.0, "close": 10.0, "volume": 10.0, 
        "ticker": "TEST", "category_id": 1, "open": 10.0, "low": 10.0, "adjust_close": 10.2},
    ])
    pd.testing.assert_frame_equal(data, expected_data, check_exact=False, check_dtype=False)

if __name__ == "__main__":
    unittest.main()