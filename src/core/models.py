"""
Core data models for Training Data Bot

This module defines Pydantic models for all data structures and throughout
the application, ensuring type safety and validation.
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

class BaseEntity(BaseModel):
    """Base class for all entities with common fields."""
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class DocumentType(str, Enum):
    """Document types supported by the application."""
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    TXT = "txt"
    CSV = "csv"
    MD = "md"
    JSON = "json"
    HTML = "html"
    URL = "url"

class TaskType(str, Enum):
    """Task types supported by the application."""
    CLASSIFICATION = "classification"
    QA_GENERATOR = "qa_generator"
    SUMMARIZATION = "summarization"
    NER = "ner"
    RED_TEAMING = "red_teaming"
    INSTRUCTION_RESPONSE = "instruction_response"

class QualityMetrics(str, Enum):
    """Quality metrics supported by the application."""
    TOXICITY = "toxicity"
    BIAS = "bias"
    DIVERSITY = "diversity"
    COHERENCE = "coherence"
    RELEVANCE = "relevance"

class ProcessingStatus(str, Enum):
    """Processing status of a task."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ExportFormat(str, Enum):
    """Export formats supported by the application."""
    JSONL = "Jsonl"
    CSV = "csv"
    PARQUET = "parquet"
    HUGGINGFACE = "huggingface"

class Document(BaseEntity):
    """Represents a source document."""
    title:str
    content:str
    source: str
    doc_type: DocumentType
    language: Optional[str] = "en"
    encoding: Optional[str] = "utf-8"
    size: int = 0
    word_count: int = 0
    char_count: int = 0

    #Processing Info
    extraction_method: Optional[str] = None
    processing_time: Optional[float] = None

    @field_validator("word_count", mode="before")
    @classmethod
    def calculate_word_count(cls, v, values):
        if v == 0 and "content" in values.data:
            return len(values.data["content"].split())
        return v

    @field_validator("char_count", mode="before")
    @classmethod
    def calculate_char_count(cls, v, values):
        if v == 0 and "content" in values.data:
            return len(values.data["content"])
        return v
    
class TextChunk(BaseEntity):
    """Represents a chunk of text extracted from a document."""
    document_id: UUID
    content: str
    start_index: int
    end_index: int
    chunk_index: int
    token_count: int = 0

    #Context preservation
    preceding_content: Optional[str] = None
    following_content: Optional[str] = None

    #Semantic Info
    embeddings: Optional[List[float]] = None
    topics: List[str] = Field(default_factory=list)

    @field_validator("token_count", mode="before")
    @classmethod
    def estimate_token_count(cls, v, values):
        if v == 0 and "content" in values:
            #Rough estimation: 1 = 4 characters
            return len(values["content"]) // 4
        return v
    
class TaskTemplate(BaseEntity):
    """Represents a task template for text extraction and processing."""
    name: str
    task_type: TaskType
    description: str
    prompt_template: str

    #Task-specific configuration
    parameters: Dict[str, Any] = Field(default_factory=dict)

    #Quality requirements
    min_output_length: int = 10
    max_output_length: int = 2000
    quality_threshold: Dict[QualityMetrics, float] = Field(default_factory=dict)

class TaskResult(BaseEntity):
    """Represents the result of a task execution."""
    task_id: UUID
    template_id: UUID
    input_chunck_id: UUID

    #Output
    output: str
    confidence: Optional[float] = None

    #Processing Info
    processing_time: float
    token_usage: int = 0
    cost: Optional[float] = None

    #Status
    status: ProcessingStatus = ProcessingStatus.PENDING
    error_message: Optional[str] = None

class TrainingExample(BaseEntity):
    """Represents a training example for a task."""
    input_text: str
    output_text: str
    task_type: TaskType

    #Source tracking
    source_document_id: UUID
    source_chunk_id: Optional[UUID] = None
    template_id: Optional[UUID] = None

    #Quality Assessment
    quality_metrics: Dict[QualityMetrics, float] = Field(default_factory=dict)
    quality_approved: Optional[bool] = None

    #Additional fields for different formats
    instruction: Optional[str] = None
    context: Optional[str] = None
    category: Optional[str] = None

class Dataset(BaseEntity):
    """Represents a dataset for a task."""
    name: str
    description: str
    version: str = "1.0.0"

    examples: List[TrainingExample] = Field(default_factory=list)

    #Statistics
    total_examples: int = 0
    task_type_counts: Dict[TaskType, int] = Field(default_factory=dict)
    quality_stats: Dict[QualityMetrics, Dict[str, float]] = Field(default_factory=dict)

    # Splits
    train_split: float = 0.8
    validation_split: float = 0.1
    test_split: float = 0.1

    #Export Info
    export_format: ExportFormat = ExportFormat.JSONL
    exported_at: Optional[datetime] = None
    export_path: Optional[Path] = None

    @field_validator("total_examples", mode="before")
    @classmethod
    def calculate_total_examples(cls, v, values):
        if "examples" in values:
            return len(values["examples"])
        return v
    
class APIRequest(BaseModel):
    """Represents a request to the API."""
    request_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))

class APIResponse(BaseModel):
    """Represents a response from the API."""
    response_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))
    succes: bool
    message: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None

class ScraperRequest(APIRequest):
    """Represents a request to the scraper."""
    prompt: str
    input_text: str
    parameter: Dict[str, Any] = Field(default_factory=dict)
    task_type: Optional[TaskType] = None

class ScraperResponse(APIRequest):
    """Represents a response from a scraper."""
    output: Optional[str] = None
    confidence: Optional[float] = None
    token_usage: int = 0
    cost: Optional[float] = None
    processing_time: Optional[float] = None

class QualityReport(BaseEntity):
    """Represents a quality report for a task."""
    target_id: UUID
    target_type: str

    #Overalll Quality Score
    overall_score: float
    passed: bool

    #Individual Metric Score
    metric_scores: Dict[QualityMetrics, float] = Field(default_factory=dict)
    metric_details: Dict[QualityMetrics, Dict[str, Any]] = Field(default_factory=dict)

    #Issues Found
    issues: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    #Assessment Metadata
    assessed_at: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))
    assessor: str = "System"
    assessment_time: float = 0.0

class ProcessingJob(BaseEntity):
    """Represents a processing job."""
    name: str
    job_type: str
    status: ProcessingStatus = ProcessingStatus.PENDING

    #I/O
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)

    #Process tracking
    total_items: int = 0
    processed_items: int = 0
    failed_items: int = 0

    #Timing
    started_at: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3

    @property
    def progress_percentage(self) -> float:
        """Calculates the progress percentage of the job."""
        if self.total_items == 0:
            return 0.0
        return (self.processed_items / self.total_items) * 100.0
    
class ProjectConfig(BaseModel):
    """Represents a project configuration."""
    name: str
    description: str
    version: str = "1.0.0"

    #Task configuration
    default_task_types: List[TaskType] = Field(default_factory=list)
    quality_requirements: Dict[QualityMetrics, float] = Field(default_factory=dict)

    #Processing settings
    batch_size: int = 10
    max_workers: int = 4
    timeout: int = 300

    #Export settings
    default_export_format: ExportFormat = ExportFormat.JSONL
    output_directory: Path = Path("./outputs")

    #DataSource Settings
    supported_formats: List[DocumentType] = Field(default_factory=list)


class FileInfo(BaseModel):
    """Represents a file information."""
    path: Path
    name: str
    size: int
    modified_at: datetime
    file_type: DocumentType
    encoding: Optional[str] = None

    @field_validator("name", mode="before")
    @classmethod
    def extract_name(cls, v, values):
        if not v and "path" in values:
            return values["path"].name
        
        return v

class ProgressInfo(BaseModel):
    """Progress information for operations."""
    current: int = 0
    total: int = 0
    message: str = ""
    percentage: float = 0.0
    eta: Optional[datetime] = None

    @field_validator("percentage", mode="before")
    @classmethod
    def calculate_percentage(cls, v, values):
        total = values.data.get("total", 0)
        current = values.data.get("current", 0)
        if total > 0:
            return (current / total) * 100
        return 0.0