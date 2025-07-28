"""
Base loader class for document sources.

This module provides the abstract base class that all document loaders
inherit from, ensuring consistent interface and behavior.
"""

import asyncio
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union, Optional, AsyncGenerator
from pathlib import Path

from .core.models import Document, DocumentType