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

    # --- Determine Input State (Simplified) ---
    input_state = initial_state.copy()

    # Check if graph requires 'product' in its input schema
    graph_input_schema = getattr(graph_obj, "input_schema", None)
    required_inputs = (
        set(graph_input_schema.schema().get("required", []))
        if graph_input_schema
        else set()
    )
    input_properties = (
        graph_input_schema.schema().get("properties", {}) if graph_input_schema else {}
    )

    # Determine input based on schema (add url if needed)
    if "product" in required_inputs or "product" in input_properties:
        input_state["product"] = name
    # Specifically check for 'url' for graphs like scrape_summary
    if "url" in required_inputs or "url" in input_properties:
        if url:
            input_state["url"] = url
        else:
            # Handle missing URL if required by the graph
            logger.error(
                f"Graph {graph_key} requires 'url' but none provided for {name}. Cannot execute."
            )
            # Create a failed RawResult immediately
            return RawResult(
                graph_key=graph_key,
                product=product_info,
                summary="Execution skipped: Missing required URL input.",
                latency_ms=0,
                ttft_ms=None,
                node_latencies={},
                error="Missing required URL input.",
            )
    # Check if *other* required inputs are missing (excluding product/url handled above)
    elif required_inputs - set(input_state.keys()):
        logger.warning(
            f"Graph {graph_key} requires inputs ({required_inputs - set(input_state.keys())}) not provided by product name, URL, or initial_state. Relying on current state: {input_state}"
        )
        # Proceed, assuming initial_state + product/url is sufficient

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
            input_state, config={"callbacks": [latency_callback]}
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
            # Check for the new summary_message field
            if (
                "summary_message" in graph_output
                and graph_output["summary_message"] is not None
            ):
                # Extract content assuming it's a BaseMessage with a .content attribute
                summary_msg_obj = graph_output["summary_message"]
                if hasattr(summary_msg_obj, "content") and isinstance(
                    summary_msg_obj.content, str
                ):
                    summary = summary_msg_obj.content
                else:
                    # Handle unexpected format
                    summary = f"Summary message object format unexpected: {type(summary_msg_obj)}"
                    logger.warning(summary)
            # Fallback to previous fields if summary_message is not present or empty
            elif "summary" in graph_output and graph_output["summary"] is not None:
                summary = str(graph_output["summary"])
                logger.debug(f"Using legacy 'summary' field for {graph_key} - {name}")
            elif (
                "search_results" in graph_output
                and graph_output["search_results"] is not None
            ):
                # Use search_results as fallback (for direct_search graph)
                summary = str(graph_output["search_results"])
                logger.debug(f"Using 'search_results' field for {graph_key} - {name}")
            else:
                summary = f"Expected summary field (summary_message, summary, search_results) not found in final output keys: {list(graph_output.keys())}. Output: {str(graph_output)[:200]}..."
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
