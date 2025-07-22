"""
Main EDA Bot Class

This module contains the main EDA Bot class, which is responsible for executing the EDA process,
Preprocessing, Feature Engineering, Model Suggestion and Dataset Export.
"""

import asyncio
from pathlib import Path
from uuid import UUID
from typing import List, Dict, Tuple, Optional, Any

from .utils.config import settings
from utils.exception import EDAException
from utils.logger import logging

from .sources import UnifedLoader
from .ai import AIClient
from .tasks import TaskManager
from .process import Processor
from .suggestion import Suggestor
from .exporter import DataSetExporter

