"""
This module contains the ExcelLoader Class to load xlsx files.
"""

import pandas as pd
import sys
from src.utils.logger import logging
from src.utils.exception import EDAException

class ExcelLoader():
    def load_excel(data_file : str) -> pd.DataFrame:
        try:
            return pd.read_excel(data_file)
            logging.info("Excel file loaded succuessfully")
        except Exception as e:
            raise EDAException(e, sys)