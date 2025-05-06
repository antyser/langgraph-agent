"""Handles the execution of configured LangGraph graphs for evaluation."""

import asyncio
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from langgraph.graph.graph import CompiledGraph
from loguru import logger

from src.common.callbacks import NodeLatencyCallback
from src.evaluation.common_defs import RAW_FILENAME, GraphConfiguration, RawResult


async def run_graph_for_product(
    product_info: Dict[str, Any],
    graph_key: str,
    graph_config: GraphConfiguration,
    latency_callback: NodeLatencyCallback,
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
    graph_obj: CompiledGraph = graph_config["graph"]
    initial_state: Dict[str, Any] = graph_config.get("initial_state", {})
    # graph_type is removed

    name = product_info.get("name", product_info.get("url", "Unknown Product"))
    url = product_info.get("url")  # Get URL from product info

    logger.info(f"Running [{graph_key}]: {name}")
    latency_callback.reset()

    # --- Prepare Initial State for the Unified State Model ---
    # The graph itself will use the State Pydantic model for validation.
    # We pass a dictionary that can populate it.
    initial_graph_input_dict = {
        "product": name,
        "url": url,
        # Add other fields from graph_config's initial_state if they exist in the unified State model
        # e.g., search_engine
    }
    if "search_engine" in initial_state:
        initial_graph_input_dict["search_engine"] = initial_state["search_engine"]
    # Any other fields from initial_state that are part of the unified State model can be added here.

    # --- Execute Graph ---
    start_time = time.perf_counter()
    node_latencies: Dict[str, float] = {}
    summary = (
        "Graph execution did not complete successfully or yielded no final output."
    )
    error_str: Optional[str] = None
    graph_output: Optional[Dict[str, Any]] = None

    try:
        final_event_data = None
        last_event_output = (
            None  # Variable to store the data from the last relevant event
        )
        async for event in graph_obj.astream_events(
            initial_graph_input_dict, config={"callbacks": [latency_callback]}
        ):
            logger.trace(f"Stream event for {graph_key} - {name}: {event}")

            # Check for the final graph end event
            if event.get("event") == "on_chain_end":
                event_data = event.get("data", {})
                if isinstance(event_data.get("output"), dict):
                    last_event_output = event_data["output"]
                    # Found the final output, no need to process further events for state
                    # break # Optional: break if we only care about the final state

        # After the loop, assign the data from the last captured relevant event
        if last_event_output:
            final_event_data = last_event_output
            logger.debug(
                f"Captured final event data for {graph_key} - {name}: {final_event_data}"
            )

        # Get latencies after the stream finishes (or errors out)
        node_latencies = latency_callback.get_last_run_report()

        # Assign graph_output if we got a final state
        if final_event_data:
            graph_output = final_event_data
            # --- Extract Summary (Simplified) ---
            # All graphs should now place their final string output in the 'output' field of the State
            if isinstance(graph_output.get("output"), str):
                summary = graph_output["output"]
            elif graph_output.get("output") is None:
                summary = "Graph output field was None."
                logger.warning(
                    f"Graph {graph_key} final state 'output' field is None for {name}. State: {graph_output}"
                )
            else:
                summary = f"Graph 'output' field not found or not a string. Keys: {list(graph_output.keys())}. Output: {str(graph_output.get('output'))[:200]}..."
                logger.warning(summary)
        else:
            # Stream finished but we didn't capture a final state with output
            summary = "Graph stream finished, but no final output state captured."
            logger.warning(summary)

    except Exception as e:
        # Use loguru's exception method to automatically include the traceback
        logger.exception(f"Error streaming {graph_key} for product {name}")

        error_str = str(e)
        # Get latencies up to the error, even if stream fails
        # Add try-except around this call too, in case the callback state is the issue
        try:
            node_latencies = latency_callback.get_last_run_report()
        except Exception as callback_err:
            logger.error(
                f"Error retrieving latencies from callback after main exception: {callback_err}"
            )
            node_latencies = {}  # Set default if retrieving fails

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
        summary=summary,  # Ensure summary is always a string
        latency_ms=total_latency_ms,
        ttft_ms=ttft_ms,  # Add TTFT here
        node_latencies=node_latencies,
        error=error_str,
    )

    return raw_result


# Function signature remains the same
async def execute_single_graph_run(
    graph_key: str,
    graph_config: GraphConfiguration,
    products_to_evaluate: List[Dict[str, Any]],
    run_dir: Path,
):
    """Executes a graph run for a single configuration and saves raw results to the run_dir."""
    logger.info(
        f"--- Starting Graph Run for: {graph_key.upper()} --- Output Dir: {run_dir}"
    )
    latency_callback = NodeLatencyCallback()

    header = f" Running Graph: {graph_key.upper()} "
    separator = "=" * 15
    logger.info(f"\n{separator}{header}{separator}\n")

    current_raw_results: List[RawResult] = []
    for product in products_to_evaluate:
        result = await run_graph_for_product(
            product, graph_key, graph_config, latency_callback
        )
        current_raw_results.append(result)
        # await asyncio.sleep(0.05) # Optional delay

    # Save raw results to the specified run directory
    raw_output_path = run_dir / RAW_FILENAME  # Use standard filename
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
