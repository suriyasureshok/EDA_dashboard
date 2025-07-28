"""
The main factory where all the executions take place.
"""
import asyncio
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Union, Any
from uuid import UUID

from .core.config import settings
from .core.logging import get_logger
from .core.exceptions import TrainingDataCurationError, ConfigurationError

from .sources import UnifiedLoader
from .decodo import DecodoClient
from .ai import AIClient
from .preprocessing import TextProcessor
from .tasks import Taskmanager
from .evaluation import QualityEvaluator
from .storage import DatasetExporter, DatabaseManager

class TrainingDataBot():
    """
    Main Training Data Bot class.
    This class provides a high-level interface for:- Loading documents from various sources- Processing text with task templates- Quality assessment and filtering- Dataset creation and export
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Training Data Bot.
        Args:
            config: Optional configuration overrides
        """
        self.logger = get_logger("Training_data_bot")
        self.config = config or {}

        self._init_components()
        self.logging,info("Training Data Bot initialized successfully")

    def _init_components(self):
        """Initialize all bot components"""
        try:
            self.loader = UnifiedLoader
            self.decodo_client = DecodoClient
            self.ai_client = AIClient
            self.processor = TextProcessor
            self.task_manager = Taskmanager
            self.evaluator = QualityEvaluator
            self.exporter = DatasetExporter
            self.db_manager = DatabaseManager
            #Memory
            self.documents: Dict[UUID, Document] = {}
            self.datasets: Dict[UUID, Dataset] = {}
            self.jobs: Dict[UUID, ProcessingJob] = {}

        except Exception as e:
             raise ConfigurationError(
                 "Failed to initialize bot components",
                 context = {"error":str(e)}, 
                 cause = e
                )
        
    async def load_documents(
        self, 
        sources: Union[str, Path, List[Union[str, Path]]], 
        doc_types: Optional[List[DocumentType]] = None, 
        **kwargs
    ) -> List[Document]:
        """
        Load documents from various sources.
        Args:
            sources: Source(s) to load documents from
            doc_types: Optional list of document types to load
            **kwargs: Additional keyword arguments for the loader
        Returns:
            List of loaded documents
        """
        
        if isinstance(sources, (str, Path)):
            sources = [source]

        documents = []
        for source in sources:
            source_path = Path(source)
            if source_path.is_dir():
                dir_docs = await self.loader.load_directory(source_path)
                documents.extend(dir_docs)

            else:
                doc = await self.loader.load_file(source_path, **kwargs)
                documents.append(doc)

        for doc in documents:
            self.documents[doc.id] = doc

    async def process_document(
        self,
        documents: Optional[List[Document]],
        task_types = Optional[List[TaskTypes]], 
        quality_filter: bool = True, **kwargs
    ) -> Dataset:
        """
        
        """        

