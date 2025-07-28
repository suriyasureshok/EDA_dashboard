"""
Training data Curation bot

Training data curation bot for LLM fine-tuning Python automation.
"""

__version__ = "0.1.0"
__author__ = "Suriya Sureshkumar"
__email__ = "suriyasureshkumarkannian@gmail.com"
__description__ = "Enterprise-grade training data curation bot for LLM fine-tuning"

from src.core.config import settings
from src.core.logging import get_logger
from src.core.exceptions import TrainingDataCurationError

