"""Handles the LLM-based evaluation of raw graph results."""

import asyncio
import json
import logging
from typing import Any, Dict, List, Literal, Optional
from pathlib import Path

from langchain_core.messages import HumanMessage

from src.evaluation.common_defs import (RawResult, EvaluatedResult, QuestionEvaluation,
                          RAW_FILENAME, EVAL_FILENAME)
from src.common.llm_models import create_gemini, create_openai

logger = logging.getLogger(__name__)

async def check_summary_answers_questions(summary: str, questions: List[str]) -> List[str]:
    """
    Evaluates if the product summary answers each question using an LLM.

    Args:
        summary: The product summary text.
        questions: List of questions to check.

    Returns:
        List of evaluation statuses ("yes", "no", "partially", "unknown").
    """
    if not summary or summary == "No summary generated." or not isinstance(summary, str):
        logger.warning("Invalid or empty summary provided for evaluation.")
        return ["unknown"] * len(questions)

    if not questions:
        return []

    try:
        eval_llm = create_openai()
        structured_llm = eval_llm.with_structured_output(QuestionEvaluation)

        prompt = f"""Evaluate if this product summary answers these questions:

Summary:
---
{summary}
---

Questions:
{chr(10).join([f"{i+1}. {q}" for i, q in enumerate(questions)])}

Return evaluations ONLY as a JSON object matching the QuestionEvaluation schema, using: yes, no, partially, unknown.
"""
        messages = [HumanMessage(content=prompt)]
        result: QuestionEvaluation = await structured_llm.ainvoke(messages)

        return result.evaluations

    except Exception as e:
        logger.error(f"LLM Evaluation failed for summary starting with '{summary[:50]}...': {e}", exc_info=False)
        return ["unknown"] * len(questions)

async def evaluate_raw_results(raw_results: List[RawResult]) -> List[EvaluatedResult]:
    """
    Performs LLM-based question evaluation on a list of raw results.

    Args:
        raw_results: List of RawResult dictionaries.

    Returns:
        List of EvaluatedResult dictionaries.
    """
    evaluated_results: List[EvaluatedResult] = []
    for raw_result in raw_results:
        summary = raw_result.summary
        product_dict = raw_result.product if isinstance(raw_result.product, dict) else {}
        questions = product_dict.get("questions", [])
        product_name = product_dict.get('name', 'Unknown')

        logger.info(f"Evaluating questions for [{raw_result.graph_key}]: {product_name}")
        question_evaluations = await check_summary_answers_questions(summary, questions)

        # Log evaluation results
        # for i, (q, e) in enumerate(zip(questions, question_evaluations)):
        #     q_short = q[:50] + "..." if len(q) > 50 else q
        #     logger.info(f"  Q{i+1}: {q_short} - {e.upper()}")

        # Create EvaluatedResult Pydantic model
        try:
            evaluated_result = EvaluatedResult(
                **raw_result.model_dump(), # Unpack existing raw result fields
                question_evaluations=question_evaluations,
                questions_answered={
                    "yes": question_evaluations.count("yes"),
                    "partially": question_evaluations.count("partially"),
                    "no": question_evaluations.count("no"),
                    "unknown": question_evaluations.count("unknown"),
                    "total": len(question_evaluations)
                }
            )
            evaluated_results.append(evaluated_result)
        except Exception as pydantic_error:
             logger.error(f"Pydantic validation failed for EvaluatedResult [{raw_result.graph_key}] {product_name}: {pydantic_error}")
             # Optionally append a placeholder or skip if validation fails

    return evaluated_results

async def execute_single_evaluation(graph_key: str, run_dir: Path) -> Optional[List[EvaluatedResult]]:
    """Loads raw results from run_dir, performs evaluation, saves evaluated results to run_dir."""
    logger.info(f"--- Starting Evaluation for: {graph_key.upper()} --- Dir: {run_dir}")
    # EVAL_RESULTS_DIR.mkdir(parents=True, exist_ok=True) # Not needed, run_dir exists

    # Load from run_dir using standard filename
    raw_input_path = run_dir / RAW_FILENAME
    if not raw_input_path.exists():
        logger.warning(f"Raw results file not found for '{graph_key}' at {raw_input_path}. Skipping evaluation.")
        return None # Return None if input is missing

    logger.info(f"{'='*15} Evaluating Results for: {graph_key.upper()} {'='*15}")
    raw_results_to_eval: List[RawResult] = [] # Initialize
    try:
        with open(raw_input_path, "r", encoding="utf-8") as f:
            raw_data_list = json.load(f)
            if not isinstance(raw_data_list, list):
                raise TypeError(f"Expected a list in {raw_input_path}, but got {type(raw_data_list)}")

            # Simplified parsing: If any item fails, the whole stage fails for this run
            raw_results_to_eval = [RawResult(**item) for item in raw_data_list if isinstance(item, dict)]
            # Log if any items were skipped because they weren't dicts
            skipped_items = [item for item in raw_data_list if not isinstance(item, dict)]
            if skipped_items:
                logger.warning(f"Skipped non-dictionary items found in {raw_input_path}: {len(skipped_items)} items.")

    except (IOError, json.JSONDecodeError, TypeError, Exception) as e: # Catch Pydantic errors too
        logger.exception(f"Failed to load or parse raw results for '{graph_key}' from {raw_input_path}. Halting evaluation.") # Log full traceback
        raise e # Re-raise the exception to stop the process

    # Perform evaluation only if parsing was successful
    # (The exception handling above ensures this)
    evaluated_results = await evaluate_raw_results(raw_results_to_eval)

    # Save evaluated results to run_dir using standard filename
    eval_output_path = run_dir / EVAL_FILENAME
    try:
        evaluated_dicts = [res.model_dump() for res in evaluated_results]
        with open(eval_output_path, "w", encoding="utf-8") as f:
            json.dump(evaluated_dicts, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"Evaluated results for '{graph_key}' saved to {eval_output_path}")
    except (IOError, TypeError) as e:
        logger.exception(f"Failed to save evaluated JSON results for '{graph_key}'.") # Log full traceback
        raise e # Re-raise exception

    logger.info(f"--- Evaluation Complete for: {graph_key.upper()} ---")
    return evaluated_results # Return the list of evaluated results 