"""
This module contains the CSVLoader Class to load CSV files.
"""
import pandas as pd
import sys
from src.utils.logger import logging
from src.utils.exception import EDAException

class CSVLoader():
    def load_csv(data_file : str) -> pd.DataFrame:
        try:
            return pd.read_csv(data_file)
            logging.info("CSV file loaded succuessfully")
        except Exception as e:
            raise EDAException(e, sys)