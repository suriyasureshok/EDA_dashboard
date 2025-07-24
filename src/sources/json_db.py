"""
This module contains the JsonLoader Class to load json files.
"""

import pandas as pd
import sys
from src.utils.logger import logging
from src.utils.exception import EDAException

class JsonLoader():
    def load_json(data_file : str) -> pd.DataFrame:
        try:
            return pd.read_json(data_file)
            logging.info("JSON file loaded succuessfully")
        except Exception as e:
            raise EDAException(e, sys)