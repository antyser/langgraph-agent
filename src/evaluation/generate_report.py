"""Handles generation of Markdown and text summary reports from evaluated results."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.evaluation.common_defs import (
    EVAL_FILENAME,
    REPORT_FILENAME_TEMPLATE,
    SUMMARY_LOG_FILE,
    EvaluatedResult,
    EvaluationDetail,
)

logger = logging.getLogger(__name__)


def generate_markdown_report(
    evaluated_results: List[EvaluatedResult], graph_key: str, run_dir: Path
):
    """Generates a Markdown report file for a set of evaluated results within the run_dir."""
    if not evaluated_results:
        logger.warning(
            f"No evaluated results provided for graph key '{graph_key}'. Skipping Markdown report."
        )
        return

    report_filename = REPORT_FILENAME_TEMPLATE.format(graph_key=graph_key)
    report_path = run_dir / report_filename
    num_products = len(evaluated_results)
    total_overall_latency = sum(r.latency_ms for r in evaluated_results)
    avg_overall_latency = total_overall_latency / num_products if num_products else 0

    # Calculate TTFT average
    ttfts_ms = [r.ttft_ms for r in evaluated_results if r.ttft_ms is not None]
    num_ttfts = len(ttfts_ms)
    avg_ttft_ms = sum(ttfts_ms) / num_ttfts if num_ttfts else None

    node_latency_sums: Dict[str, float] = {}
    node_latency_counts: Dict[str, int] = {}
    for r in evaluated_results:
        for node, latency in r.node_latencies.items():
            if latency is not None:
                node_latency_sums[node] = node_latency_sums.get(node, 0) + latency
                node_latency_counts[node] = node_latency_counts.get(node, 0) + 1
    node_latency_avgs: Dict[str, float] = {
        node: node_latency_sums[node] / node_latency_counts[node]
        for node in node_latency_sums
        if node_latency_counts.get(node, 0) > 0
    }

    total_questions = sum(
        r.questions_answered.get("total", 0) for r in evaluated_results
    )
    total_yes = sum(r.questions_answered.get("yes", 0) for r in evaluated_results)
    total_partially = sum(
        r.questions_answered.get("partially", 0) for r in evaluated_results
    )
    yes_pct = (total_yes / total_questions * 100) if total_questions else 0
    yes_partially_pct = (
        ((total_yes + total_partially) / total_questions * 100)
        if total_questions
        else 0
    )

    # Calculate general rubric metrics
    total_rubrics = sum(
        r.rubrics_summary.get("total", 0)
        for r in evaluated_results
        if hasattr(r, "rubrics_summary")
    )
    total_rubrics_yes = sum(
        r.rubrics_summary.get("yes", 0)
        for r in evaluated_results
        if hasattr(r, "rubrics_summary")
    )
    rubrics_yes_pct = (total_rubrics_yes / total_rubrics * 100) if total_rubrics else 0

    # Calculate average word count
    total_word_count = sum(
        r.summary_word_count
        for r in evaluated_results
        if hasattr(r, "summary_word_count")
    )
    avg_word_count = total_word_count / num_products if num_products else 0

    # Calculate accuracy metrics
    total_accuracy_checks = sum(
        r.accuracy_summary.get("total", 0)
        for r in evaluated_results
        if hasattr(r, "accuracy_summary")
    )
    total_accuracy_yes = sum(
        r.accuracy_summary.get("yes", 0)
        for r in evaluated_results
        if hasattr(r, "accuracy_summary")
    )
    accuracy_yes_pct = (
        (total_accuracy_yes / total_accuracy_checks * 100)
        if total_accuracy_checks
        else 0
    )

    md = []
    md.append(f"# Evaluation Report: {graph_key}")
    md.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md.append(f"Number of Products Evaluated: {num_products}")
    md.append("\n## Overall Metrics")
    md.append(f"- **Average Overall Latency:** {avg_overall_latency / 1000:.3f} s")
    if avg_ttft_ms is not None:
        md.append(f"- **Average Time To First Token (TTFT):** {avg_ttft_ms:.2f} ms")
    if node_latency_avgs:
        md.append("- **Average Node Latencies (seconds):**")
        for node, avg_lat in sorted(node_latency_avgs.items()):
            md.append(f"  - `{node}`: {avg_lat:.3f} s")
    if total_questions > 0:
        md.append("- **Question Answering:**")
        md.append(f"  - Total Questions Asked: {total_questions}")
        md.append(f"  - Answered 'Yes': {total_yes} ({yes_pct:.1f}%)")
        md.append(
            f"  - Answered 'Yes' or 'Partially': {total_yes + total_partially} ({yes_partially_pct:.1f}%)"
        )
    if total_rubrics > 0:
        md.append("- **Formatting & Content Rubrics:**")
        md.append(f"  - Total Rubrics Evaluated: {total_rubrics}")
        md.append(
            f"  - Met Successfully ('Yes'): {total_rubrics_yes} ({rubrics_yes_pct:.1f}%)"
        )
    if num_products > 0:
        md.append(f"- **Average Summary Word Count:** {avg_word_count:.0f}")
    if total_accuracy_checks > 0:
        md.append("- **Accuracy vs True Statements:**")
        md.append(f"  - Total Accuracy Checks: {total_accuracy_checks}")
        md.append(
            f"  - Met Successfully ('Yes'): {total_accuracy_yes} ({accuracy_yes_pct:.1f}%)"
        )

    md.append("\n## Individual Product Results")
    md.append(
        "| # | Product | Overall Latency (s) | TTFT (ms) | Node Latencies (s) | Q's Answered | Rubrics Met | Accuracy Met | Word Count | Error |"
    )
    md.append(
        "|---|---------|---------------------|-----------|--------------------|--------------|-------------|--------------|------------|-------|"
    )

    for i, r in enumerate(evaluated_results):
        product_info = r.product
        product_name = product_info.get("name", product_info.get("url", "Unknown"))[:50]
        latency_s = f"{r.latency_ms / 1000:.3f}"
        ttft_str = f"{r.ttft_ms:.2f}" if r.ttft_ms is not None else "N/A"
        node_lats = r.node_latencies
        q_answered = r.questions_answered
        rubrics_summary = getattr(r, "rubrics_summary", {})
        error = r.error

        node_lat_str = "N/A"
        if node_lats:
            node_lat_str = " / ".join(
                [
                    f"{node}: {lat:.3f}"
                    for node, lat in sorted(node_lats.items())
                    if lat is not None
                ]
            )

        q_answered_str = f"{q_answered.get('yes', 0) + q_answered.get('partially', 0)}/{q_answered.get('total', 0)}"
        rubrics_met_str = (
            f"{rubrics_summary.get('yes', 0)}/{rubrics_summary.get('total', 0)}"
        )
        accuracy_summary_data = getattr(r, "accuracy_summary", {})
        accuracy_met_str = f"{accuracy_summary_data.get('yes', 0)}/{accuracy_summary_data.get('total', 0)}"
        word_count_str = str(getattr(r, "summary_word_count", "N/A"))

        error_str = error if error else "None"

        md.append(
            f"| {i+1} | {product_name} | {latency_s} | {ttft_str} | {node_lat_str} | {q_answered_str} | {rubrics_met_str} | {accuracy_met_str} | {word_count_str} | {error_str} |"
        )

    # Add section for detailed Q&A
    md.append("\n## Detailed Question Evaluation")
    for i, r in enumerate(evaluated_results):
        product_info = r.product
        product_name = product_info.get("name", product_info.get("url", "Unknown"))
        questions = product_info.get("questions", [])
        details = r.question_details

        md.append(f"\n### {i+1}. {product_name}")
        md.append(f"**Summary Snippet:** {r.summary[:150].replace('\n', ' ')}...")
        if r.error:
            md.append(f"**ERROR:** {r.error}")
        md.append("")  # Blank line

        # Add general rubric evaluation section
        general_rubric_results = getattr(r, "general_rubric_results", [])
        if general_rubric_results:
            md.append("#### General Formatting & Content Rubrics")
            md.append("| Rubric | Met | Reason if Not Met |")
            md.append("|--------|-----|------------------|")
            for rubric_result in general_rubric_results:
                rubric_text = rubric_result.get("rubric", "Unknown rubric").replace(
                    "|", "\\|"
                )
                evaluation = rubric_result.get("evaluation", "unknown")
                reason = rubric_result.get("reason", "")

                eval_icon = "✅" if evaluation == "yes" else "❌"
                md.append(f"| {rubric_text} | {eval_icon} | {reason} |")
            md.append("")  # Blank line

        # Add accuracy metric evaluation section
        accuracy_metric_details = getattr(r, "accuracy_metric_details", [])
        if accuracy_metric_details:
            md.append("#### Accuracy Against True Statements")
            md.append("| True Statement | Accurate | Reason if Not Accurate |")
            md.append("|----------------|----------|------------------------|")
            for acc_detail in accuracy_metric_details:
                true_statement_text = acc_detail.true_statement.replace(
                    "|", "\\|"
                ).replace("\n", "<br>")
                acc_evaluation = acc_detail.evaluation
                acc_reason = acc_detail.reason or ""
                acc_eval_icon = "✅" if acc_evaluation == "yes" else "❌"
                md.append(f"| {true_statement_text} | {acc_eval_icon} | {acc_reason} |")
            md.append("")  # Blank line

        md.append("#### Product-Specific Questions")
        if not details:
            md.append("*No evaluation details available.*")
            continue

        md.append("| Q# | Evaluation | Excerpt / Reason | Question |")
        md.append("|----|------------|------------------|----------|")

        # Ensure details list matches questions list length for safe zip
        num_q = len(questions)
        num_d = len(details)
        if num_q != num_d:
            md.append(
                f"| *Mismatch* | *Error: {num_q} questions vs {num_d} details* | | |"
            )

        # Iterate through questions and corresponding details (up to the shorter list length)
        for q_idx, (question, detail) in enumerate(zip(questions, details)):  # Safe zip
            q_num = q_idx + 1
            # Use detail.question_number if available and matches, otherwise use loop index + 1
            display_q_num = (
                detail.question_number if detail.question_number == q_num else q_num
            )

            eval_status = detail.evaluation.upper()
            excerpt_reason = ""
            if detail.evaluation in ["yes", "partially"] and detail.excerpt:
                excerpt_reason = f"*Excerpt:* {detail.excerpt.replace('|','\\').replace('\n', '<br>')}"
            elif detail.reason:
                excerpt_reason = (
                    f"*Reason:* {detail.reason.replace('|','\\').replace('\n', '<br>')}"
                )

            question_text = question.replace("|", "\\").replace("\n", "<br>")

            md.append(
                f"| {display_q_num} | **{eval_status}** | {excerpt_reason} | {question_text} |"
            )

    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))
        logger.info(f"Markdown report saved to {report_path}")
    except IOError as e:
        logger.exception(f"Failed to write Markdown report to {report_path}")
        raise e


def update_combined_log(graph_key: str, evaluated_results: List[EvaluatedResult]):
    """Appends a summary of a single evaluation run to the combined log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not evaluated_results:
        logger.warning(f"No evaluated results provided for {graph_key} to update log.")
        return

    try:
        SUMMARY_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SUMMARY_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n\n{'=' * 60}")
            f.write(f"\nEVALUATION RUN - {graph_key.upper()} - {timestamp}")
            f.write(f"\n{'=' * 60}")

            # Calculate stats for this specific run
            num_products = len(evaluated_results)
            total_overall_latency = sum(r.latency_ms for r in evaluated_results)
            avg_overall_latency = (
                total_overall_latency / num_products if num_products else 0
            )

            # Calculate TTFT average
            ttfts_ms = [r.ttft_ms for r in evaluated_results if r.ttft_ms is not None]
            num_ttfts = len(ttfts_ms)
            avg_ttft_ms = sum(ttfts_ms) / num_ttfts if num_ttfts else None

            node_latency_sums: Dict[str, float] = {}
            node_latency_counts: Dict[str, int] = {}
            for r in evaluated_results:
                for node, latency in r.node_latencies.items():
                    if latency is not None:
                        node_latency_sums[node] = (
                            node_latency_sums.get(node, 0) + latency
                        )
                        node_latency_counts[node] = node_latency_counts.get(node, 0) + 1
            node_latency_avgs: Dict[str, float] = {
                node: node_latency_sums[node] / node_latency_counts[node]
                for node in node_latency_sums
                if node_latency_counts.get(node, 0) > 0
            }

            # Calculate general rubric metrics
            total_rubrics = sum(
                r.rubrics_summary.get("total", 0)
                for r in evaluated_results
                if hasattr(r, "rubrics_summary")
            )
            total_rubrics_yes = sum(
                r.rubrics_summary.get("yes", 0)
                for r in evaluated_results
                if hasattr(r, "rubrics_summary")
            )
            rubrics_yes_pct = (
                (total_rubrics_yes / total_rubrics * 100) if total_rubrics else 0
            )

            # Calculate average word count
            total_word_count = sum(
                r.summary_word_count
                for r in evaluated_results
                if hasattr(r, "summary_word_count")
            )
            avg_word_count = total_word_count / num_products if num_products else 0

            # Calculate accuracy metrics
            total_accuracy_checks = sum(
                r.accuracy_summary.get("total", 0)
                for r in evaluated_results
                if hasattr(r, "accuracy_summary")
            )
            total_accuracy_yes = sum(
                r.accuracy_summary.get("yes", 0)
                for r in evaluated_results
                if hasattr(r, "accuracy_summary")
            )
            accuracy_yes_pct = (
                (total_accuracy_yes / total_accuracy_checks * 100)
                if total_accuracy_checks
                else 0
            )

            f.write(f"\nAverage Overall Latency: {avg_overall_latency:.2f} ms")
            if node_latency_avgs:
                f.write("\nAverage Node Latencies (seconds):")
                for node, avg_lat in sorted(node_latency_avgs.items()):
                    f.write(f"\n  - {node}: {avg_lat:.3f} s")

            if total_rubrics > 0:
                f.write(
                    f"\nGeneral Formatting & Content Rubrics: {total_rubrics_yes}/{total_rubrics} met ({rubrics_yes_pct:.1f}%)"
                )

            if num_products > 0:
                f.write(f"\nAverage Summary Word Count: {avg_word_count:.0f}")

            if total_accuracy_checks > 0:
                f.write(
                    f"\nAccuracy vs True Statements: {total_accuracy_yes}/{total_accuracy_checks} met ({accuracy_yes_pct:.1f}%)"
                )

            f.write(f"\n\n--- Individual Product Details ---")
            for i, r in enumerate(evaluated_results):
                product_info = r.product
                product_name = product_info.get(
                    "name", product_info.get("url", "Unknown Product")
                )
                latency_ms = r.latency_ms
                q_answered_data = r.questions_answered
                q_answered = q_answered_data.get("yes", 0) + q_answered_data.get(
                    "partially", 0
                )
                q_total = q_answered_data.get("total", 0)

                # Get rubrics summary
                rubrics_summary = getattr(r, "rubrics_summary", {})
                rubrics_yes = rubrics_summary.get("yes", 0)
                rubrics_total = rubrics_summary.get("total", 0)

                # Get accuracy summary and word count
                accuracy_summary_data = getattr(r, "accuracy_summary", {})
                accuracy_yes = accuracy_summary_data.get("yes", 0)
                accuracy_total = accuracy_summary_data.get("total", 0)
                word_count = getattr(r, "summary_word_count", "N/A")

                node_lats = r.node_latencies
                summary = r.summary
                error = r.error

                f.write(f"\n\n{i+1}. Product: {product_name}")
                f.write(f"\n   Overall Latency: {latency_ms:.2f} ms")
                if node_lats:
                    node_lat_str = " / ".join(
                        [
                            f"{node}: {lat:.3f}s"
                            for node, lat in sorted(node_lats.items())
                            if lat is not None
                        ]
                    )
                    f.write(f"\n   Node Latencies: {node_lat_str}")
                f.write(f"\n   Questions answered: {q_answered}/{q_total}")
                f.write(f"\n   Rubrics met: {rubrics_yes}/{rubrics_total}")
                f.write(f"\n   Accuracy met: {accuracy_yes}/{accuracy_total}")
                f.write(f"\n   Summary Word Count: {word_count}")
                f.write(
                    f"\n   Summary Snippet: {summary[:150].replace(chr(10), ' ')}..."
                )
                if error:
                    f.write(f"\n   ERROR: {error}")

                # Add general rubric evaluation to log
                general_rubric_results = getattr(r, "general_rubric_results", [])
                if general_rubric_results:
                    f.write("\n   General Rubric Evaluation:")
                    for result in general_rubric_results:
                        eval_str = "✓" if result.get("evaluation") == "yes" else "✗"
                        reason = (
                            f" - {result.get('reason')}" if result.get("reason") else ""
                        )
                        f.write(
                            f"\n     - [{eval_str}] {result.get('rubric', 'Unknown')}{reason}"
                        )

                # Add detailed accuracy evaluation to log
                accuracy_details_log = getattr(r, "accuracy_metric_details", [])
                if accuracy_details_log:
                    f.write("\n   Accuracy Against True Statements:")
                    for acc_res in accuracy_details_log:
                        acc_eval_str = "✓" if acc_res.evaluation == "yes" else "✗"
                        acc_reason_log = (
                            f" - {acc_res.reason}" if acc_res.reason else ""
                        )
                        f.write(
                            f"\n     - [{acc_eval_str}] {acc_res.true_statement[:80]}...{acc_reason_log}"
                        )

                # Add detailed Q&A to log
                questions = product_info.get("questions", [])
                details = r.question_details
                f.write("\n   Detailed Question Evaluation:")
                if details:
                    num_q = len(questions)
                    num_d = len(details)
                    if num_q != num_d:
                        f.write("\n     - !! Mismatch between questions and details !!")
                    for q_idx, (question, detail) in enumerate(zip(questions, details)):
                        q_num = q_idx + 1
                        display_q_num = (
                            detail.question_number
                            if detail.question_number == q_num
                            else q_num
                        )
                        excerpt_reason_log = (
                            f" (Excerpt: {detail.excerpt})"
                            if detail.excerpt
                            else f" (Reason: {detail.reason})" if detail.reason else ""
                        )
                        f.write(
                            f"\n     - Q{display_q_num}: {detail.evaluation.upper()}{excerpt_reason_log} [{question[:60]}...] "
                        )
                else:
                    f.write("\n     - No details available.")

            f.write(f"\n\n{'=' * 60}\n")  # End of block
        logger.info(
            f"Combined summary log updated with run for {graph_key}: {SUMMARY_LOG_FILE}"
        )

    except IOError as e:
        logger.error(f"Failed to write to summary log file {SUMMARY_LOG_FILE}: {e}")


def execute_single_report_generation(graph_key: str, run_dir: Path):
    """Loads evaluated results from run_dir for a single graph key and generates reports."""
    logger.info(
        f"--- Starting Report Generation for: {graph_key.upper()} --- Dir: {run_dir}"
    )

    # Load evaluated results for the specified key from run_dir
    evaluated_results: Optional[List[EvaluatedResult]] = None
    eval_input_path = run_dir / EVAL_FILENAME
    if eval_input_path.exists():
        logger.info(
            f"Loading evaluated results for '{graph_key}' from {eval_input_path} for reporting."
        )
        try:
            with open(eval_input_path, "r", encoding="utf-8") as f:
                evaluated_data_list = json.load(f)
                evaluated_results = [
                    EvaluatedResult(**item) for item in evaluated_data_list
                ]
        except (IOError, json.JSONDecodeError, Exception) as e:
            logger.exception(
                f"Failed to load or parse evaluated results file {eval_input_path} for reporting. Halting report generation."
            )
            raise e
    else:
        logger.warning(
            f"Evaluated results file not found for '{graph_key}' at {eval_input_path}. Cannot generate report."
        )
        return  # Exit if no data

    # Generate reports if data was loaded successfully
    if evaluated_results:
        logger.info(f"Generating Markdown report for: {graph_key.upper()}")
        generate_markdown_report(evaluated_results, graph_key, run_dir)

        logger.info(
            f"Updating combined evaluation summary log for: {graph_key.upper()}"
        )
        # Pass the loaded results to the modified log function
        update_combined_log(graph_key, evaluated_results)
    else:
        logger.warning(
            f"No evaluated results were loaded for '{graph_key}', skipping report generation."
        )

    logger.info(f"--- Report Generation Complete for: {graph_key.upper()} ---")
