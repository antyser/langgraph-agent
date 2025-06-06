"""Handles the LLM-based evaluation of raw graph results."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, TypedDict

from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from evaluation_data import GENERAL_EVALUATION_RUBRICS_V2
from src.common.llm_models import create_gemini, create_openai
from src.evaluation.common_defs import (
    EVAL_FILENAME,
    RAW_FILENAME,
    AccuracyMetricResult,
    EvaluatedResult,
    EvaluationDetail,
    GeneralRubricResult,
    QuestionEvaluation,
    RawResult,
)

logger = logging.getLogger(__name__)


def count_words(text: str) -> int:
    """Counts the number of words in a given text string."""
    if not isinstance(text, str) or not text.strip():
        return 0
    return len(text.split())


async def check_general_rubrics(summary: str) -> List[GeneralRubricResult]:
    """
    Evaluates if the product summary follows the general evaluation rubrics using an LLM.
    """
    if (
        not summary
        or summary == "No summary generated."
        or not isinstance(summary, str)
    ):
        logger.warning(
            "Invalid or empty summary provided for general rubric evaluation."
        )
        return [
            GeneralRubricResult(
                rubric=rubric,
                evaluation="no",
                reason="Invalid or empty summary provided.",
            )
            for rubric in GENERAL_EVALUATION_RUBRICS_V2
        ]

    try:
        # Define a structured output schema
        class RubricEvaluation(BaseModel):
            evaluation_results: List[GeneralRubricResult]

        eval_llm = create_openai()
        structured_llm = eval_llm.with_structured_output(RubricEvaluation)

        rubrics_text = "\n".join(
            [f"{i+1}. {rubric}" for i, rubric in enumerate(GENERAL_EVALUATION_RUBRICS_V2)]
        )

        prompt = f"""Evaluate if this product summary follows these general formatting and content rubrics. 
For each rubric, determine if the summary follows it (yes) or not (no). 
If the answer is "no", provide a brief reason why.

Summary:
---
{summary}
---

General Rubrics:
{rubrics_text}

For each rubric, evaluate and return:
1. The text of the rubric
2. Your evaluation: Either "yes" or "no"
3. A reason if the evaluation is "no" 

Return ONLY a JSON object matching the RubricEvaluation schema with a list of evaluation results.
"""
        messages = [HumanMessage(content=prompt)]
        result: RubricEvaluation = await structured_llm.ainvoke(messages)

        # Get the existing rubrics we have results for
        processed_rubrics = {r.rubric for r in result.evaluation_results}

        # For any missing rubrics, add them with "no" evaluation
        for rubric in GENERAL_EVALUATION_RUBRICS_V2:
            if rubric not in processed_rubrics:
                result.evaluation_results.append(
                    GeneralRubricResult(
                        rubric=rubric,
                        evaluation="no",
                        reason="LLM did not evaluate this rubric",
                    )
                )

        # Add after the LLM invocation to see what we're getting back
        logger.info(f"Raw evaluation results: {result.evaluation_results}")
        logger.info(f"Processed rubrics: {processed_rubrics}")
        logger.info(
            f"Missing rubrics: {set(GENERAL_EVALUATION_RUBRICS_V2) - processed_rubrics}"
        )

        return result.evaluation_results

    except Exception as e:
        logger.error(f"General rubric evaluation failed: {e}", exc_info=True)
        return [
            GeneralRubricResult(
                rubric=rubric,
                evaluation="no",
                reason=f"Evaluation failed: {e}",
            )
            for rubric in GENERAL_EVALUATION_RUBRICS_V2
        ]


async def check_general_rubrics_one_by_one(summary: str) -> List[GeneralRubricResult]:
    """
    Evaluates each rubric individually to avoid overloading the LLM context.
    """
    results = []
    eval_llm = create_openai()

    for rubric in GENERAL_EVALUATION_RUBRICS_V2:
        try:
            # Define the per-rubric schema
            class SingleRubricEvaluation(BaseModel):
                rubric: str
                evaluation: Literal["yes", "no"]
                reason: Optional[str] = None

            structured_llm = eval_llm.with_structured_output(SingleRubricEvaluation)

            prompt = f"""Evaluate if this product summary follows this specific rubric. 
Determine if the summary follows it (yes) or not (no).
If the answer is "no", provide a brief reason why.

Summary:
---
{summary}
---

Rubric to evaluate:
"{rubric}"

Return a JSON object with:
1. The text of the rubric
2. Your evaluation: Either "yes" or "no"
3. A reason if the evaluation is "no" 
"""
            messages = [HumanMessage(content=prompt)]
            result = await structured_llm.ainvoke(messages)
            results.append(GeneralRubricResult(**result.model_dump()))

        except Exception as e:
            logger.error(f"Evaluation failed for rubric '{rubric}': {e}")
            results.append(
                GeneralRubricResult(
                    rubric=rubric,
                    evaluation="no",
                    reason=f"Evaluation failed: {e}",
                )
            )

    return results


async def check_summary_answers_questions(
    summary: str, questions: List[str]
) -> List[EvaluationDetail]:
    """
    Evaluates if the product summary answers each question using an LLM,
    providing detailed results including excerpts and reasons.

    Args:
        summary: The product summary text.
        questions: List of questions to check.

    Returns:
        List of EvaluationDetail objects.
    """
    if (
        not summary
        or summary == "No summary generated."
        or not isinstance(summary, str)
    ):
        logger.warning("Invalid or empty summary provided for evaluation.")
        return [
            EvaluationDetail(
                question_number=i + 1,
                evaluation="unknown",
                reason="Invalid or empty summary provided.",
            )
            for i in range(len(questions))
        ]

    if not questions:
        return []

    try:
        eval_llm = create_openai()
        structured_llm = eval_llm.with_structured_output(QuestionEvaluation)

        prompt = f"""Evaluate if this product summary answers these questions. For each question, provide:
1.  `question_number`: The original question number (1-based).
2.  `evaluation`: Your assessment ('yes', 'no', 'partially', 'unknown').
3.  `excerpt`: (OPTIONAL) A *brief*, directly quoted text excerpt from the summary that supports a 'yes' or 'partially' answer. Only include if directly relevant.
4.  `reason`: (OPTIONAL) A *brief* explanation for 'no', 'partially', or 'unknown' evaluations, or if the answer is inferred rather than explicit.

Summary:
---
{summary}
---

Questions:
{chr(10).join([f"{i+1}. {q}" for i, q in enumerate(questions)])}

Return ONLY a JSON object matching the QuestionEvaluation schema, containing a list under the key `evaluation_details`.
"""
        messages = [HumanMessage(content=prompt)]
        result: QuestionEvaluation = await structured_llm.ainvoke(messages)

        return result.evaluation_details

    except Exception as e:
        logger.error(
            f"LLM Evaluation failed for summary starting with '{summary[:50]}...': {e}",
            exc_info=False,
        )
        return [
            EvaluationDetail(
                question_number=i + 1,
                evaluation="unknown",
                reason=f"LLM evaluation failed: {e}",
            )
            for i in range(len(questions))
        ]


async def check_accuracy_against_true_statements(
    summary: str, true_statements: List[str]
) -> List[AccuracyMetricResult]:
    """
    Evaluates if the product summary accurately covers the key information of each true statement.
    Focuses on whether the core message of the true statement is present in the summary.
    """
    results: List[AccuracyMetricResult] = []
    if (
        not summary
        or summary == "No summary generated."
        or not isinstance(summary, str)
    ):
        logger.warning(
            "Invalid or empty summary provided for accuracy metric evaluation."
        )
        return [
            AccuracyMetricResult(
                true_statement=ts,
                evaluation="no",
                reason="Invalid or empty summary provided.",
            )
            for ts in true_statements
        ]

    if not true_statements:
        return []

    eval_llm = create_openai()

    class SingleAccuracyEvaluation(BaseModel):
        true_statement: str
        evaluation: Literal["yes", "no"]
        reason: Optional[str] = None

    structured_llm = eval_llm.with_structured_output(SingleAccuracyEvaluation)

    for stmt_idx, true_statement_text in enumerate(true_statements):
        try:
            prompt = f"""Evaluate if the provided product summary accurately covers the KEY INFORMATION of the following true statement.
The summary does NOT need to mention every single specific detail from the true statement, but it MUST capture the main point or an essential piece of information.

Product Summary:
---
{summary}
---

True Statement to Evaluate (Statement #{stmt_idx + 1}):
"{true_statement_text}"

Does the summary accurately cover the KEY INFORMATION of this true statement?
- Answer "yes" if the summary contains the core message or an essential piece of information from the true statement.
- Answer "no" if the summary omits the key information from the true statement.
- Provide a brief reason if your evaluation is "no".

Return a JSON object with:
1.  `true_statement`: The exact text of the true statement being evaluated.
2.  `evaluation`: Your evaluation: "yes" or "no".
3.  `reason`: A brief reason if the evaluation is "no".
"""
            messages = [HumanMessage(content=prompt)]
            # logger.debug(f"Accuracy prompt for statement {stmt_idx+1}:\\n{prompt}") # Optional: for debugging prompts
            result = await structured_llm.ainvoke(messages)
            results.append(AccuracyMetricResult(**result.model_dump()))

        except Exception as e:
            logger.error(
                f"Accuracy evaluation failed for true statement '{true_statement_text[:50]}...': {e}"
            )
            results.append(
                AccuracyMetricResult(
                    true_statement=true_statement_text,
                    evaluation="no",
                    reason=f"Evaluation failed: {e}",
                )
            )
    return results


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
        product_dict = (
            raw_result.product if isinstance(raw_result.product, dict) else {}
        )
        questions = product_dict.get("questions", [])
        true_statements = product_dict.get("true_statements", [])
        product_name = product_dict.get("name", "Unknown")

        logger.info(
            f"Evaluating questions for [{raw_result.graph_key}]: {product_name}"
        )

        # Evaluate product-specific questions
        evaluation_details: List[EvaluationDetail] = (
            await check_summary_answers_questions(summary, questions)
        )

        # Evaluate general rubrics
        logger.info(
            f"Evaluating general rubrics for [{raw_result.graph_key}]: {product_name}"
        )
        general_rubric_results_models = await check_general_rubrics_one_by_one(summary)
        general_rubric_results_dicts = [
            r.model_dump() for r in general_rubric_results_models
        ]

        # Evaluate accuracy against true statements
        logger.info(
            f"Evaluating accuracy metrics for [{raw_result.graph_key}]: {product_name}"
        )
        accuracy_metric_details: List[AccuracyMetricResult] = (
            await check_accuracy_against_true_statements(summary, true_statements)
        )

        # Compute summary counts from the detailed results
        eval_counts = {"yes": 0, "no": 0, "partially": 0, "unknown": 0}
        for detail in evaluation_details:
            eval_counts[detail.evaluation] = eval_counts.get(detail.evaluation, 0) + 1
        questions_answered_summary = {
            "yes": eval_counts["yes"],
            "partially": eval_counts["partially"],
            "no": eval_counts["no"],
            "unknown": eval_counts["unknown"],
            "total": len(evaluation_details),
        }

        # Compute rubric counts
        rubric_counts = {"yes": 0, "no": 0}
        for rubric_result in general_rubric_results_models:
            rubric_counts[rubric_result.evaluation] = (
                rubric_counts.get(rubric_result.evaluation, 0) + 1
            )
        rubrics_summary = {
            "yes": rubric_counts["yes"],
            "no": rubric_counts["no"],
            "total": len(general_rubric_results_models),
        }

        # Compute accuracy summary
        accuracy_counts = {"yes": 0, "no": 0}
        for acc_detail in accuracy_metric_details:
            accuracy_counts[acc_detail.evaluation] = (
                accuracy_counts.get(acc_detail.evaluation, 0) + 1
            )
        accuracy_summary = {
            "yes": accuracy_counts["yes"],
            "no": accuracy_counts["no"],
            "total": len(accuracy_metric_details),
        }

        # Count words in the summary
        summary_word_count = count_words(summary)

        # Create EvaluatedResult Pydantic model with detailed results
        try:
            evaluated_result = EvaluatedResult(
                **raw_result.model_dump(),
                question_details=evaluation_details,
                questions_answered=questions_answered_summary,
                general_rubric_results=general_rubric_results_dicts,
                rubrics_summary=rubrics_summary,
                accuracy_metric_details=[result for result in accuracy_metric_details],
                accuracy_summary=accuracy_summary,
                summary_word_count=summary_word_count,
            )
            evaluated_results.append(evaluated_result)
        except Exception as pydantic_error:
            logger.error(
                f"Pydantic validation failed for EvaluatedResult [{raw_result.graph_key}] {product_name}: {pydantic_error}"
            )
            # Optionally append a placeholder or skip if validation fails

    return evaluated_results


async def execute_single_evaluation(
    graph_key: str, run_dir: Path
) -> Optional[List[EvaluatedResult]]:
    """Loads raw results from run_dir, performs evaluation, saves evaluated results to run_dir."""
    logger.info(f"--- Starting Evaluation for: {graph_key.upper()} --- Dir: {run_dir}")
    # EVAL_RESULTS_DIR.mkdir(parents=True, exist_ok=True) # Not needed, run_dir exists

    # Load from run_dir using standard filename
    raw_input_path = run_dir / RAW_FILENAME
    if not raw_input_path.exists():
        logger.warning(
            f"Raw results file not found for '{graph_key}' at {raw_input_path}. Skipping evaluation."
        )
        return None  # Return None if input is missing

    logger.info(f"{'='*15} Evaluating Results for: {graph_key.upper()} {'='*15}")
    raw_results_to_eval: List[RawResult] = []  # Initialize
    try:
        with open(raw_input_path, "r", encoding="utf-8") as f:
            raw_data_list = json.load(f)
            if not isinstance(raw_data_list, list):
                raise TypeError(
                    f"Expected a list in {raw_input_path}, but got {type(raw_data_list)}"
                )

            # Simplified parsing: If any item fails, the whole stage fails for this run
            raw_results_to_eval = [
                RawResult(**item) for item in raw_data_list if isinstance(item, dict)
            ]
            # Log if any items were skipped because they weren't dicts
            skipped_items = [
                item for item in raw_data_list if not isinstance(item, dict)
            ]
            if skipped_items:
                logger.warning(
                    f"Skipped non-dictionary items found in {raw_input_path}: {len(skipped_items)} items."
                )

    except (
        IOError,
        json.JSONDecodeError,
        TypeError,
        Exception,
    ) as e:  # Catch Pydantic errors too
        logger.exception(
            f"Failed to load or parse raw results for '{graph_key}' from {raw_input_path}. Halting evaluation."
        )  # Log full traceback
        raise e  # Re-raise the exception to stop the process

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
        logger.exception(
            f"Failed to save evaluated JSON results for '{graph_key}'."
        )  # Log full traceback
        raise e  # Re-raise exception

    logger.info(f"--- Evaluation Complete for: {graph_key.upper()} ---")
    return evaluated_results  # Return the list of evaluated results
