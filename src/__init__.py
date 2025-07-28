"""
Training data Curation bot

Training data curation bot for LLM fine-tuning Python automation.
"""

__version__ = "0.1.0"
__author__ = "Suriya Sureshkumar"
__email__ = "suriyasureshkumarkannian@gmail.com"
__description__ = "Enterprise-grade training data curation bot for LLM fine-tuning"

from .core.config import settings
from .core.logging import get_logger
from .core.exceptions import TrainingDataCurationError

from .bot import TrainingDataBot

from .sources import (
    PDFLoader,
    WebLoader,
    DocumentLoader,
    UnifiedLoader,
)

from .tasks import (
    QAGenerator,
    ClassificationGenerator,
    SummarizationGenerator,
    TaskTemplate,
)

from .decodo import DecodoClient
from .prerocessing import TextProcessor
from .evaluation import QualityEvaluator
from .storage import DatasetExporter

__all__ = [
    #Core
    "TrainingDataBot",
    "settings",
    "get_logger",
    "TrainingDataCurationError",

    #Sources
    "PDFLoader",
    "WebLoader",
    "DocumentLoader",
    "UnifiedLoader",
    
    #Tasks
    "QAGenerator",
    "SummarizationGenerator",
    "ClassificationGenerator",
    "TaskTemplate",

    # Services
    "DecodoClient",
    "TextPreprocessor",
    "QualityEvaluator",
    "DatasetExporter",
]