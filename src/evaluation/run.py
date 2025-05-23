"""Main orchestrator script for the evaluation pipeline."""

import argparse
import asyncio

# Remove standard logging import
# import logging
import os
import uuid  # For generating unique IDs
from datetime import datetime
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv

# Import loguru logger
from loguru import logger

# Remove standard logging configuration
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# Load .env before other imports that might need env vars
load_dotenv()

# Use absolute import for evaluation data
from evaluation_data import COVERAGE_TO_EVALUATE

# Use absolute imports for evaluation components
from src.evaluation.common_defs import (
    DATA_DIR,
    EVAL_FILENAME,
    RAW_FILENAME,
    GraphConfiguration,
)
from src.evaluation.generate_report import execute_single_report_generation
from src.evaluation.run_evaluation import execute_single_evaluation

# Use absolute imports for execution functions
from src.evaluation.run_graph import execute_single_graph_run
from src.product_summary.graph import graph as scrape_graph

# Use absolute import for the new direct search graph
from src.product_summary.no_plan_search_graph import graph as direct_search_graph

# Use absolute imports for graph definitions and product data
# Adjust these imports based on your actual project structure
from src.product_summary.plan_graph import graph as plan_graph

# Define Graph Configurations
# Keys should be unique identifiers
ALL_GRAPH_CONFIGURATIONS: Dict[str, GraphConfiguration] = {
    "plan_google": {"graph": plan_graph, "initial_state": {"search_engine": "google"}},
    "plan_openai": {"graph": plan_graph, "initial_state": {"search_engine": "openai"}},
    "direct_google": {
        "graph": direct_search_graph,
        "initial_state": {"search_engine": "google"},
    },
    "direct_openai": {
        "graph": direct_search_graph,
        "initial_state": {"search_engine": "openai"},
    },
    "scrape_summary": {
        "graph": scrape_graph,
        # No initial state needed here, the graph takes URL from product info
        "initial_state": {},
    },
    # Add more configurations here
}


async def main():
    """Parses arguments and runs the selected evaluation stages."""

    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(
        description="Run evaluation pipeline for product summary graphs."
    )
    parser.add_argument(
        "--run-graphs",
        action="store_true",
        help="Execute graph runs and save raw results.",
    )
    parser.add_argument(
        "--run-evaluation",
        action="store_true",
        help="Load raw results, perform LLM evaluation, save evaluated results.",
    )
    parser.add_argument(
        "--generate-report",
        action="store_true",
        help="Load evaluated results, generate Markdown reports and update combined log.",
    )
    parser.add_argument(
        "--graph-key",
        type=str,
        default=None,
        # Update choices after adding scrape_summary back
        choices=list(ALL_GRAPH_CONFIGURATIONS.keys()),
        metavar="KEY",
        help=f"Specify ONE graph configuration to process. Choices: {list(ALL_GRAPH_CONFIGURATIONS.keys())}. If omitted, uses the first defined key.",
    )
    parser.add_argument(
        "--skip-existing-raw",
        action="store_true",
        help="If --run-graphs is set, skip running graphs for which raw results JSON already exists.",
    )
    # Add argument for specifying run ID / folder name
    parser.add_argument(
        "--run-id",
        type=str,
        default=None,
        help="Specify a run ID. If provided, reuses existing folder and intermediate results within that folder. Otherwise, creates a new run folder.",
    )

    args = parser.parse_args()

    # Determine which actions to run
    run_graphs_flag = args.run_graphs
    run_evaluation_flag = args.run_evaluation
    generate_report_flag = args.generate_report

    # Default to running all stages if no specific action is requested
    if not run_graphs_flag and not run_evaluation_flag and not generate_report_flag:
        logger.info(
            "No specific action requested, defaulting to run all stages: graphs, evaluation, report."
        )
        run_graphs_flag = True
        run_evaluation_flag = True
        generate_report_flag = True
    # If only generate_report is requested, we implicitly need evaluation results
    # If only run_evaluation is requested, we implicitly need graph results (handled by stage checks)

    # Determine the single graph key to run
    if args.graph_key:
        selected_graph_key = args.graph_key
    else:
        if len(ALL_GRAPH_CONFIGURATIONS) == 1:
            selected_graph_key = list(ALL_GRAPH_CONFIGURATIONS.keys())[0]
            logger.info(
                f"No graph key specified, defaulting to the only available key: {selected_graph_key}"
            )
        else:
            parser.error(
                "Multiple graph configurations exist. Please specify ONE using --graph-key."
            )
            return  # Should exit due to parser.error, but adding return for clarity

    logger.info(f"Processing graph configuration: {selected_graph_key}")
    graph_config_to_run = ALL_GRAPH_CONFIGURATIONS.get(selected_graph_key)

    if not graph_config_to_run:
        # This case should be prevented by argparse choices, but check anyway
        logger.error(
            f"Configuration for graph key '{selected_graph_key}' not found. Exiting."
        )
        return

    # --- Determine Run Directory --- #
    if args.run_id:
        # Use provided run ID
        run_id = args.run_id
        run_dir = DATA_DIR / run_id
        logger.info(f"Using specified run ID: {run_id} (Directory: {run_dir})")
        # Create directory if it doesn't exist when reusing ID
        run_dir.mkdir(parents=True, exist_ok=True)
    else:
        # Generate a new run ID (e.g., timestamp + graph_key + uuid)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        short_uuid = str(uuid.uuid4())[:6]
        run_id = f"{timestamp}_{selected_graph_key}_{short_uuid}"
        run_dir = DATA_DIR / run_id
        logger.info(f"Generating new run ID: {run_id} (Directory: {run_dir})")
        # Create the new directory
        run_dir.mkdir(
            parents=True, exist_ok=False
        )  # exist_ok=False to avoid overwriting

    # --- Execute Stages --- #
    raw_file_path = run_dir / RAW_FILENAME
    eval_file_path = run_dir / EVAL_FILENAME

    if run_graphs_flag:
        # If --run-id was specified and raw results exist, skip running graph stage implicitly
        if args.run_id and raw_file_path.exists():
            logger.info(
                f"Raw results file found in specified run folder ({run_dir}). Skipping graph run stage."
            )
        else:
            # If no run-id or raw file doesn't exist in the specified run folder, run graph
            await execute_single_graph_run(
                selected_graph_key, graph_config_to_run, COVERAGE_TO_EVALUATE, run_dir
            )

    if run_evaluation_flag:
        # Check if input (raw results) exists in the run folder
        if not raw_file_path.exists():
            logger.error(
                f"Raw results file ({raw_file_path}) not found. Cannot run evaluation. Please run the graph stage first."
            )
        # Check if output (eval results) already exists in the run folder
        elif args.run_id and eval_file_path.exists():
            logger.info(
                f"Evaluated results file found in specified run folder ({run_dir}). Skipping evaluation stage."
            )
        else:
            # Input exists, and output doesn't (or no run-id reuse specified)
            await execute_single_evaluation(selected_graph_key, run_dir)

    if generate_report_flag:
        # Check if input (evaluated results) exists in the run folder
        if not eval_file_path.exists():
            logger.error(
                f"Evaluated results file ({eval_file_path}) not found. Cannot generate report. Please run the evaluation stage first."
            )
        else:
            # Input exists, generate report
            execute_single_report_generation(selected_graph_key, run_dir)

    logger.info("Evaluation pipeline finished.")


if __name__ == "__main__":
    import sys

    # Configure loguru basic settings (optional, defaults are often sufficient)
    # Example: logger.add("file_{time}.log", level="INFO") # To add file logging
    # The default logs INFO and above to stderr.
    # Set TRACE level for debugging stream events if needed
    logger.remove()
    logger.add(sys.stderr, level="TRACE")  # Or set to INFO for normal operation
    asyncio.run(main())
