"""Shared type definitions and constants for the evaluation pipeline."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated

# --- Path Constants ---

DATA_DIR = Path("./data")
# Remove specific directory paths
# RAW_RESULTS_DIR = DATA_DIR / "raw_results"
# EVAL_RESULTS_DIR = DATA_DIR / "evaluated_results"
# REPORTS_DIR = DATA_DIR / "reports"
SUMMARY_LOG_FILE = DATA_DIR / "evaluation_summary_log.txt" # Keep global log file

# Define standard filenames within a run folder
RAW_FILENAME = "raw_results.json"
EVAL_FILENAME = "evaluation_results.json"
REPORT_FILENAME_TEMPLATE = "report_{graph_key}.md"

# --- Type Definitions ---

class EvaluationDetail(BaseModel):
    """Detailed evaluation for a single question."""
    model_config = ConfigDict(extra='ignore')
    question_number: int = Field(description="The original question number (1-based).")
    evaluation: Literal["yes", "no", "partially", "unknown"]
    excerpt: Optional[str] = Field(default=None, description="Relevant text excerpt from the summary if evaluation is 'yes' or 'partially'.")
    reason: Optional[str] = Field(default=None, description="Reasoning for the evaluation, especially if 'no', 'partially', or 'unknown'.")


class QuestionEvaluation(BaseModel):
    """Structured output type for LLM-based question evaluation."""
    model_config = ConfigDict(extra='ignore')

    evaluation_details: List[EvaluationDetail] = Field(
        ...,
        description="List of detailed evaluations (including excerpt/reason) for each question."
    )

class RawResult(BaseModel):
    """Structure for results after graph execution, before LLM evaluation."""
    model_config = ConfigDict(extra='ignore')

    graph_key: str
    graph_type: Literal["plan_google", "plan_openai", "scrape", "unknown"]
    product: Dict[str, Any]
    summary: str
    latency_ms: float
    node_latencies: Dict[str, float]
    error: Optional[str] = None

class EvaluatedResult(RawResult):
    """Structure for final results after LLM evaluation."""

    question_details: List[EvaluationDetail]
    questions_answered: Dict[str, int]

GraphConfiguration = Dict[str, Any] # Type alias for graph config dicts 