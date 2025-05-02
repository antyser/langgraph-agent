"""Custom LangChain Callback Handlers."""

from langchain_core.callbacks import AsyncCallbackHandler
from typing import Dict, Any, List, Optional
import time
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class NodeLatencyCallback(AsyncCallbackHandler):
    """Async callback handler for tracking node execution latency and TTFT in LangGraph for the last run."""

    def __init__(self) -> None:
        """Initialize the callback handler."""
        super().__init__()
        self._reset_run_tracking()

    def _reset_run_tracking(self) -> None:
        """Reset tracking dictionaries for a new graph run."""
        self.start_times: Dict[str, float] = {}
        self.run_id_to_node_name: Dict[str, str] = {} # Map run_id to node name
        # Store {node_name: latency} for the current/last run
        self.last_run_latencies: Dict[str, float] = {} 
        # TTFT tracking
        self.graph_start_time: Optional[float] = None
        self.first_token_time: Optional[float] = None

    async def on_chain_start(
        self,
        serialized: Dict[str, Any] | None,
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: List[str] | None = None,
        metadata: Dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Record start time and map run_id to node name."""
        run_id_str = str(run_id)
        current_time = time.monotonic()

        # If it's the overall graph start (no parent_run_id within the context of this specific run)
        # Heuristic: The first on_chain_start event for the graph itself might lack a parent_run_id 
        # or have a specific tag/metadata indicating it's the top-level start.
        # A simpler approach: record the first call to on_chain_start as graph_start_time.
        if self.graph_start_time is None:
            self.graph_start_time = current_time
            # Reset TTFT time for the new graph run
            self.first_token_time = None
            logger.debug(f"Graph start time recorded: {self.graph_start_time:.4f}")

        try:
            # Use _get_node_name primarily to identify the node
            node_name = self._get_node_name(run_id, tags, metadata, serialized, **kwargs)
            # logger.debug(f"on_chain_start: run_id={run_id_str}, node_name={node_name}, tags={tags}, metadata={metadata}")
            if node_name:
                self.start_times[run_id_str] = time.monotonic()
                self.run_id_to_node_name[run_id_str] = node_name # Store mapping
        except Exception as e:
             logger.warning(f"Error in NodeLatencyCallback.on_chain_start callback: {e}", exc_info=True)

    async def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: List[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Calculate and record latency using the run_id to find the node name."""
        run_id_str = str(run_id)
        if run_id_str not in self.start_times:
            # logger.debug(f"on_chain_end: Skipping run_id={run_id_str} (no start time)")
            return 

        try:
            # Look up the node name using the run_id stored during on_chain_start
            node_name = self.run_id_to_node_name.get(run_id_str)
            # logger.debug(f"on_chain_end: run_id={run_id_str}, found_node_name={node_name}")

            if node_name:
                latency = time.monotonic() - self.start_times[run_id_str]
                self.last_run_latencies[node_name] = latency
                # logger.info(f"Recorded latency for {node_name} ({run_id_str}): {latency:.4f}s")
            
            # Clean up start time and run_id mapping
            del self.start_times[run_id_str]
            if run_id_str in self.run_id_to_node_name:
                 del self.run_id_to_node_name[run_id_str]

        except Exception as e:
             logger.warning(f"Error in NodeLatencyCallback.on_chain_end callback: {e}", exc_info=True)
             # Ensure cleanup happens even on error
             if run_id_str in self.start_times:
                 del self.start_times[run_id_str]
             if run_id_str in self.run_id_to_node_name:
                 del self.run_id_to_node_name[run_id_str]

    async def on_llm_new_token(
        self,
        token: str,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> None:
        """Record the time when the first token is received."""
        # Check if this is the first token received for the current graph run
        if self.first_token_time is None:
            self.first_token_time = time.monotonic()
            logger.debug(f"First token time recorded: {self.first_token_time:.4f} (run_id: {run_id})")

    # _get_node_name now mainly used by on_chain_start to identify the node initially
    def _get_node_name(self, run_id: UUID, tags: List[str] | None, metadata: Dict[str, Any] | None, serialized: Dict[str, Any] | None, **kwargs: Any) -> str | None:
        """Helper to determine the LangGraph node name, safely handling None inputs."""
        # Priority 1: LangGraph metadata (most reliable)
        if metadata and "langgraph_node" in metadata:
            # Ensure it's not the overall graph entry point's metadata if it exists
            if metadata["langgraph_node"] not in ["__start__", "__end__"]:
                 return metadata["langgraph_node"]
        
        # Priority 2: Check tags for explicit node names if metadata fails
        if isinstance(tags, list):
             for tag in tags:
                 if tag.startswith("langgraph_node:"):
                     node_name = tag.split(":", 1)[1]
                     if node_name not in ["__start__", "__end__"]:
                         return node_name
        
        # Fallback: Check serialized name (less reliable for end events)
        potential_name_from_kwargs = kwargs.get("name")
        potential_name_from_serialized = serialized.get("name") if isinstance(serialized, dict) else None 
        potential_name = potential_name_from_kwargs or potential_name_from_serialized
        
        # Check if it looks like a langgraph node based on tags and isn't internal
        is_langgraph_node = isinstance(tags, list) and any("langgraph" in tag for tag in tags)
        if potential_name and is_langgraph_node and potential_name not in ["RunnableSequence", "__start__", "__end__"]:
            return potential_name

        # logger.debug(f"_get_node_name could not identify node for run_id={run_id}, tags={tags}, metadata={metadata}, name={potential_name}")
        return None

    def get_last_run_report(self) -> Dict[str, float]:
        """Return a dictionary of node latencies from the last run."""
        # Filter out potential main graph entry if tracked
        return {k: v for k, v in self.last_run_latencies.items() if k not in ['__start__', '__end__']}

    def print_last_run_report(self) -> None:
        """Print a formatted latency report for the last run to the primary logger."""
        report = self.get_last_run_report()
        if report:
            log_message = "\n--- Node Latency Report (Last Run) ---\n"
            total_latency = 0.0
            for node, latency in sorted(report.items()): # Sort for consistent order
                log_message += f"- {node}: {latency:.4f}s\n"
                total_latency += latency
            log_message += f"Total (Sum of Nodes): {total_latency:.4f}s\n" 
            log_message += "--------------------------------------"
            logger.info(log_message)
        else:
            logger.info("No specific node latency data collected for the last run.")

    def reset(self) -> None:
         """Reset the callback handler state for a new evaluation run."""
         self._reset_run_tracking()

    def get_ttft_ms(self) -> Optional[float]:
        """Calculate and return the Time To First Token in milliseconds."""
        if self.graph_start_time is not None and self.first_token_time is not None:
            ttft_s = self.first_token_time - self.graph_start_time
            # Ensure TTFT is not negative (shouldn't happen with monotonic clock)
            if ttft_s >= 0:
                return ttft_s * 1000
            else:
                 logger.warning(f"Calculated negative TTFT ({ttft_s:.4f}s). Returning None. Start: {self.graph_start_time}, First Token: {self.first_token_time}")
                 return None
        return None 