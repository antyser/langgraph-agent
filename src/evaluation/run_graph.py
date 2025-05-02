"""Handles the execution of configured LangGraph graphs for evaluation."""

import asyncio
import json
import sys
from loguru import logger
import time
from typing import Any, Dict, List, Optional
from pathlib import Path

from langgraph.graph.graph import CompiledGraph

from src.evaluation.common_defs import RawResult, GraphConfiguration, RAW_FILENAME
from src.common.callbacks import NodeLatencyCallback

logger.remove() # Remove default handler
logger.add(sys.stderr, level="TRACE") # Add handler with TRACE level

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
    # graph_type is removed

    name = product_info.get("name", product_info.get("url", "Unknown Product"))
    # url = product_info.get("url") # No longer needed for scrape logic

    logger.info(f"Running [{graph_key}]: {name}")
    latency_callback.reset()

    # --- Determine Input State (Simplified) ---
    input_state = initial_state.copy()

    # Check if graph requires 'product' in its input schema
    graph_input_schema = getattr(graph_obj, 'input_schema', None)
    required_inputs = set(graph_input_schema.schema().get('required', [])) if graph_input_schema else set()
    input_properties = graph_input_schema.schema().get('properties', {}) if graph_input_schema else {}

    if "product" in required_inputs or "product" in input_properties:
         input_state["product"] = name
    elif required_inputs: # Check if any input is required but 'product' is not
         logger.warning(f"Graph {graph_key} requires inputs ({required_inputs}) but does not explicitly take 'product'. Relying only on initial_state: {initial_state}")
         # Proceed, assuming initial_state is sufficient

    # --- Execute Graph ---
    start_time = time.perf_counter()
    node_latencies: Dict[str, float] = {}
    summary = "Graph execution did not complete successfully or yielded no final output."
    error_str: Optional[str] = None
    graph_output: Optional[Dict[str, Any]] = None

    try:
        final_event_data = None
        last_event_output = None # Variable to store the data from the last relevant event
        async for event in graph_obj.astream(input_state, config={"callbacks": [latency_callback]}):
            logger.trace(f"Stream event for {graph_key} - {name}: {event}") # Log all events
            # Check if the event dictionary is not empty and store its value part
            # The key is the node name (e.g., 'direct_search', 'plan', 'summarize')
            # The value is the output dictionary from that node
            if isinstance(event, dict) and event:
                # Get the first (and likely only) value from the event dict
                # This assumes the structure {node_name: output_dict}
                node_output = next(iter(event.values()), None)
                if node_output is not None:
                    last_event_output = node_output

        # After the loop, assign the data from the last captured event
        if last_event_output:
            final_event_data = last_event_output
            logger.debug(f"Captured final event data for {graph_key} - {name}: {final_event_data}")

        # Get latencies after the stream finishes (or errors out)
        node_latencies = latency_callback.get_last_run_report()

        # Assign graph_output if we got a final state
        if final_event_data:
            graph_output = final_event_data
            # --- Extract Summary (Simplified) ---
            if "summary" in graph_output and graph_output["summary"] is not None:
                summary = str(graph_output["summary"])
            elif "search_results" in graph_output and graph_output["search_results"] is not None:
                # Use search_results as fallback (for direct_search graph)
                summary = str(graph_output["search_results"])
                logger.debug(f"Using 'search_results' as summary for {graph_key} - {name}")
            else:
                summary = f"Summary/search_results not found in final output keys: {list(graph_output.keys())}. Output: {str(graph_output)[:200]}..."
                logger.warning(summary)
        else:
            # Stream finished but we didn't capture a final state with output
            summary = "Graph stream finished, but no final output state captured."
            logger.warning(summary)

    except Exception as e:
        logger.error(f"Error streaming {graph_key} for product {name}: {e}", exc_info=True)
        error_str = str(e)
        # Get latencies up to the error, even if stream fails
        node_latencies = latency_callback.get_last_run_report()
        summary = f"Error during execution: {error_str}"

    end_time = time.perf_counter()
    total_latency_ms = (end_time - start_time) * 1000
    logger.info(f"Finished [{graph_key}] {name} in {total_latency_ms:.2f}ms")

    # --- Prepare Raw Result (Simplified) ---
    # Get TTFT from the callback after the run
    ttft_ms = latency_callback.get_ttft_ms()

    raw_result = RawResult(
        graph_key=graph_key,
        # graph_type=graph_type, # Removed
        product=product_info,
        summary=summary, # Ensure summary is always a string
        latency_ms=total_latency_ms,
        ttft_ms=ttft_ms, # Add TTFT here
        node_latencies=node_latencies,
        error=error_str
    )

    return raw_result

# Function signature remains the same
async def execute_single_graph_run(
    graph_key: str,
    graph_config: GraphConfiguration,
    products_to_evaluate: List[Dict[str, Any]],
    run_dir: Path
):
    """Executes a graph run for a single configuration and saves raw results to the run_dir."""
    logger.info(f"--- Starting Graph Run for: {graph_key.upper()} --- Output Dir: {run_dir}")
    latency_callback = NodeLatencyCallback()

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
    return current_raw_results 