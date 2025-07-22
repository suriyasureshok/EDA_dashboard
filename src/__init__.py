"""
Auto EDA and preprocessing bot.

Gives all the description and a summary about the data with visualization and preprocessing steps.
"""

__version__ = "0.1.1"
__author__ = "Suriya Sureshkumar, Ivan Nilash"
__email__ = "suriyasureshkumar1312@gmail.com"
__description__ = "Gives all the description and a summary about the data with visualization and preprocessing steps."

#Importing the util classes
from .utils.config import settings
from .utils.logger import logging
from .utils.exception import EDAException

#Importing the manager bot
from .bot import EDABot

from .sources import (
    CSVLoader,
    ExcelLoader,
    JsonLoader,
    SQLLoader,
    APILoader,
    S3Loader,
    GSheetLoader,
    DBLoader,
    UnifiedLoader,
)

from .tasks import(
    AutoEDA,
    SummaryGenerator,
    QAGenerator,
    VisualGenerator,
    TaskManager,
)

from .process import Preprocess, Featurize 
from .suggestion import Suggest
from .exporter import DataSetExporter

__all__ = [
    #Utils
    "settings",
    "logging",
    "EDAException",

    #Bot
    "EDABot",

    #Sources
    "CSVLoader",
    "ExcelLoader",
    "JsonLoader",
    "SQLLoader",
    "APILoader",
    "S3Loader",
    "GSheetLoader",
    "DBLoader",
    "UnifiedLoader",

    #Tasks
    "AutoEDA",
    "SummaryGenerator",
    "QAGenerator",
    "VisualGenerator"
    "TaskManager",

    #Services
    "Preprocess",
    "Featurize",
    "DataSetExporter",
    "Suggest",
]