"""Handles the execution of configured LangGraph graphs for evaluation."""

import asyncio
import json
from loguru import logger
import time
from typing import Any, Dict, List, Optional, Literal
from pathlib import Path

from langgraph.graph.graph import CompiledGraph
from langchain_core.messages import BaseMessage

from src.evaluation.common_defs import RawResult, GraphConfiguration, RAW_FILENAME
from src.common.callbacks import NodeLatencyCallback


async def run_graph_for_product(
    product_info: Dict[str, Any],
    graph_key: str,
    graph_config: GraphConfiguration,
    latency_callback: NodeLatencyCallback
) -> RawResult:
    """
    Runs a configured graph for a single product and returns raw results.

    Args:
        product_info: Dictionary containing product details.
        graph_key: Identifier for the graph configuration.
        graph_config: Dictionary with graph object and initial state.
        latency_callback: Callback handler for latencies.

    Returns:
        A RawResult dictionary.
    """
    graph_obj: CompiledGraph = graph_config['graph']
    initial_state: Dict[str, Any] = graph_config.get('initial_state', {})
    # Determine graph type from config or key for input handling
    if 'plan' in graph_key:
        graph_type: Literal["plan_google", "plan_openai", "scrape", "unknown"] = graph_key # e.g. "plan_google"
    elif 'scrape' in graph_key:
        graph_type = 'scrape'
    else:
        graph_type = 'unknown'

    name = product_info.get("name", product_info.get("url", "Unknown Product"))
    url = product_info.get("url")

    logger.info(f"Running [{graph_key}]: {name}")
    latency_callback.reset()

    # --- Determine Input State ---
    input_state = initial_state.copy()
    if graph_type.startswith("plan"):
        if "product" not in graph_obj.input_schema.schema().get('properties', {}):
            logger.error(f"Graph {graph_key} requires 'product' input but not found. Skipping.")
            graph_type = "unknown"
        else:
            input_state["product"] = name
    elif graph_type == "scrape":
        if "url" not in graph_obj.input_schema.schema().get('properties', {}):
            logger.error(f"Graph {graph_key} requires 'url' input but not found. Skipping.")
            graph_type = "unknown"
        elif not url:
            logger.error(f"Graph {graph_key} requires 'url' but none provided for {name}. Skipping.")
            graph_type = "unknown"
        else:
            input_state["url"] = url
    else:
        logger.warning(f"Cannot determine input requirements for graph type '{graph_type}' from key {graph_key}. Skipping.")
        graph_type = "unknown"

    # --- Execute Graph ---
    start_time = time.perf_counter()
    node_latencies: Dict[str, float] = {}
    summary = "Execution skipped or failed."
    error_str: Optional[str] = None
    graph_output: Optional[Dict[str, Any]] = None

    if graph_type != "unknown":
        try:
            graph_output = await graph_obj.ainvoke(
                input_state,
                config={"callbacks": [latency_callback]}
            )
            node_latencies = latency_callback.get_last_run_report()

            # --- Extract Summary ---
            if graph_type.startswith("plan"):
                summary = graph_output.get("summary", "No summary generated in output.")
            elif graph_type == "scrape":
                messages: List[BaseMessage] = graph_output.get("messages", [])
                if messages and hasattr(messages[-1], 'content') and isinstance(messages[-1].content, str):
                    summary = messages[-1].content
                else:
                    summary = "Summary not found in scrape graph messages."
            else:
                 summary = f"Graph ran but summary extraction method unknown. Output: {str(graph_output)[:200]}..."

        except Exception as e:
            logger.error(f"Error invoking {graph_key} for product {name}: {e}", exc_info=True)
            error_str = str(e)
            node_latencies = latency_callback.get_last_run_report()
            summary = f"Error during execution: {error_str}"
    else:
        error_str = "Execution skipped due to invalid input state or graph type."

    end_time = time.perf_counter()
    total_latency_ms = (end_time - start_time) * 1000
    logger.info(f"Finished [{graph_key}] {name} in {total_latency_ms:.2f}ms")

    # --- Prepare Raw Result ---
    raw_result = RawResult(
        graph_key=graph_key,
        graph_type=graph_type,
        product=product_info,
        summary=summary,
        latency_ms=total_latency_ms,
        node_latencies=node_latencies,
        error=error_str
    )

    return raw_result

# Rename function and change signature to handle one key
async def execute_single_graph_run(
    graph_key: str,
    graph_config: GraphConfiguration,
    products_to_evaluate: List[Dict[str, Any]],
    run_dir: Path
):
    """Executes a graph run for a single configuration and saves raw results to the run_dir."""
    logger.info(f"--- Starting Graph Run for: {graph_key.upper()} --- Output Dir: {run_dir}")
    latency_callback = NodeLatencyCallback()
    # run_dir is created by the caller
    # RAW_RESULTS_DIR.mkdir(parents=True, exist_ok=True) # Ensure dir exists

    # No loop needed here anymore
    header = f" Running Graph: {graph_key.upper()} "
    separator = '=' * 15
    logger.info(f"\n{separator}{header}{separator}\n")

    current_raw_results: List[RawResult] = []
    for product in products_to_evaluate:
        result = await run_graph_for_product(product, graph_key, graph_config, latency_callback)
        current_raw_results.append(result)
        # await asyncio.sleep(0.05) # Optional delay

    # Save raw results to the specified run directory
    raw_output_path = run_dir / RAW_FILENAME # Use standard filename
    try:
        # Convert Pydantic models to dicts for saving
        raw_dicts = [res.model_dump() for res in current_raw_results]
        with open(raw_output_path, "w", encoding="utf-8") as f:
            json.dump(raw_dicts, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"Raw results for '{graph_key}' saved to {raw_output_path}")
    except (IOError, TypeError) as e:
        logger.error(f"Failed to save raw JSON results for '{graph_key}': {e}")

    logger.info(f"--- Graph Run Complete for: {graph_key.upper()} ---")
    # Return the results if needed by the caller, though run.py doesn't use it directly
    return current_raw_results 