"""Shared type definitions and constants for the evaluation pipeline."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, TypedDict

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

# --- Path Constants ---

DATA_DIR = Path("./data")
# Remove specific directory paths
# RAW_RESULTS_DIR = DATA_DIR / "raw_results"
# EVAL_RESULTS_DIR = DATA_DIR / "evaluated_results"
# REPORTS_DIR = DATA_DIR / "reports"
SUMMARY_LOG_FILE = DATA_DIR / "evaluation_summary_log.txt"  # Keep global log file

# Define standard filenames within a run folder
RAW_FILENAME = "raw_results.json"
EVAL_FILENAME = "evaluation_results.json"
REPORT_FILENAME_TEMPLATE = "evaluation_report_{graph_key}.md"

# --- Type Definitions ---


class EvaluationDetail(BaseModel):
    """Detailed evaluation for a single question."""

    model_config = ConfigDict(extra="ignore")
    question_number: int = Field(description="The original question number (1-based).")
    evaluation: Literal["yes", "no", "partially", "unknown"]
    excerpt: Optional[str] = Field(
        default=None,
        description="Relevant text excerpt from the summary if evaluation is 'yes' or 'partially'.",
    )
    reason: Optional[str] = Field(
        default=None,
        description="Reasoning for the evaluation, especially if 'no', 'partially', or 'unknown'.",
    )


class QuestionEvaluation(BaseModel):
    """Structured output type for LLM-based question evaluation."""

    model_config = ConfigDict(extra="ignore")

    evaluation_details: List[EvaluationDetail] = Field(
        ...,
        description="List of detailed evaluations (including excerpt/reason) for each question.",
    )


class RawResult(BaseModel):
    """Represents the raw output from a single graph run for one product."""

    graph_key: str
    product: Dict[str, Any]
    summary: str
    latency_ms: float  # Overall latency for the graph run
    ttft_ms: Optional[float] = None  # Time To First Token
    node_latencies: Dict[str, float] = {}
    error: Optional[str] = None


class EvaluatedResult(RawResult):
    """Structure for final results after LLM evaluation."""

    question_details: List[EvaluationDetail]
    questions_answered: Dict[str, int]


class GraphConfiguration(TypedDict):
    """Configuration for a specific graph to be evaluated."""

    graph: Any  # Typically a CompiledGraph
    initial_state: Dict[str, Any]


# --- Unified State Definition ---
class State(BaseModel):
    """Unified state definition for all evaluation graphs."""

    # Inputs (provided initially or by nodes)
    product: Optional[str] = None
    url: Optional[str] = None
    search_engine: Optional[Literal["google", "openai"]] = None

    # Intermediate data
    search_queries: List[str] = Field(default_factory=list)
    search_results: List[str] = Field(default_factory=list)
    scraped_content: Optional[str] = None

    # Final output from the graph (populated by the last node)
    output: Optional[str] = None


# Forward reference resolution if needed
EvaluatedResult.model_rebuild()
