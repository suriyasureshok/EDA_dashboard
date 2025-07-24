"""
This module contains the UnfiedLoader Class to choose which classes of the source has to be used to return a dataframe.
"""

from .csv import CSVLoader
from .excel import ExcelLoader
from .json_db import JsonLoader
from utils.logger import logging

class UnifiedLoader():
    def ingest_data(file_obj: object):
        if file_obj.name.endswith('.csv'):
            object = CSVLoader()
            return object.load_csv(file_obj)
        elif file_obj.name.endswith('.json'):
            object = ExcelLoader()
            return object.load_excel(file_obj)
        elif file_obj.name.endswith(('.xls', '.xlsx')):
            object = JsonLoader()
            return object.load_json(file_obj)
        else:
            raise ValueError('File type not supported')
            logging.info("Failed to load file")
            