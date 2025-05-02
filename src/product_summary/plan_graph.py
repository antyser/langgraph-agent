import asyncio
import os
import time
from common.llm_models import create_gemini, create_openai
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from google.ai.generativelanguage_v1beta.types import Tool as GenAITool
from langgraph.graph import StateGraph
from typing import List, Dict, Any, Literal
from src.product_summary.schemas import SearchQueries
import logging
from pydantic import BaseModel, ConfigDict, Field as PydanticField

logger = logging.getLogger(__name__)

PLANNING_PROMPT = """
You are an expert product researcher. Given a product name or description, generate 3-5 specific search queries that will help gather the most important information for a consumer summary (e.g., main features, pros, cons, who it's for, common complaints, ingredients, etc.).
Return only the list of queries. Make sure the queries are not overlapping.
"""

SEARCH_PROMPT = """
Use the Search tool to answer the following query about the product. Return the most relevant facts and details.
"""

SUMMARY_PROMPT = """You are an expert research summarizer that synthesizes information follow the original instructions.
    # Response Guidelines:
- Provide detailed, structured responses clearly divided into logical sections and subsections.
- Explicitly cite all sources, including the title and direct URL.
- Prioritize accuracy, thoroughness, and relevance; completeness is more important than brevity.
- Clearly distinguish between confirmed facts, well-supported conclusions, informed predictions, and speculative statements. Explicitly label speculative or emerging insights as such.
- Anticipate and proactively address potential follow-up questions or related relevant context that enhances overall comprehension.
- Incorporate relevant recent advancements, unconventional perspectives, or alternative viewpoints, explicitly marking these as emerging or speculative when applicable."""

class SimpleState(BaseModel):
    """Represents the Pydantic state for the simple product summary agent graph."""
    model_config = ConfigDict(extra='ignore') # Or 'allow' if nodes might add temp fields

    product: str
    search_engine: Literal["google", "openai"] = "google" # Default search engine
    search_queries: List[str] = PydanticField(default_factory=list)
    search_results: List[str] = PydanticField(default_factory=list)
    summary: str = ""

async def planning_node(state: SimpleState, config: Any) -> Dict[str, Any]:
    """
    Planning node that generates search queries using structured output, 
    selecting the LLM based on the state's search_engine.

    Args:
        state: The current state containing the product.
        config: The configuration for the node.

    Returns:
        A dictionary with the generated search queries list.
    """
    product = state.product
    search_engine = state.search_engine # No need for .get() with default

    # Select LLM based on search_engine
    if search_engine == "google":
        llm = create_gemini()
    elif search_engine == "openai":
        llm = create_openai()
    else:
        raise ValueError(f"Unsupported search engine in planning_node: {search_engine}")

    # Configure LLM for structured output using the Pydantic schema
    structured_llm = llm.with_structured_output(SearchQueries)

    messages = [
        HumanMessage(content=PLANNING_PROMPT),
        HumanMessage(content=f"Product: {product}")
    ]

    response: SearchQueries = await structured_llm.ainvoke(messages)

    queries = response.queries

    return {"search_queries": queries}

async def _search_single_query(
    llm: ChatGoogleGenerativeAI | ChatOpenAI,
    query: str,
    search_engine: Literal["google", "openai"]
) -> str:
    """
    Helper function to perform a single search query using the specified engine.

    Args:
        llm: The LLM instance (Gemini or OpenAI).
        query: The search query string.
        search_engine: The search engine to use ("google" or "openai").

    Returns:
        The search result as a string.
    """
    messages = [
        HumanMessage(content=SEARCH_PROMPT),
        HumanMessage(content=query)
    ]
    if search_engine == "google" and isinstance(llm, ChatGoogleGenerativeAI):
        resp = await llm.ainvoke(messages, tools=[GenAITool(google_search={})])
    elif search_engine == "openai" and isinstance(llm, ChatOpenAI):
        resp = await llm.ainvoke(messages, tools=[{"type": "web_search_preview"}])
    else:
        # Handle mismatch or unsupported engine
        raise ValueError(f"Unsupported search engine '{search_engine}' or LLM type mismatch.")

    # Ensure the return value is always a string to prevent TypeError downstream
    if isinstance(resp.content, list):
        # If it's a list (e.g., search snippets), join them into a single string
        # Adjust the joiner (e.g., "\n") if needed based on expected list content
        logger.debug(f"OpenAI search returned list, joining: {resp.content}")
        return "\n".join(map(str, resp.content))
    elif resp.content is None:
        logger.warning(f"Search query '{query}' returned None content.")
        return "" # Return empty string for None
    else:
        # Otherwise, assume it's string-like and cast just in case
        return str(resp.content)

async def search_node(state: SimpleState, config: Any) -> Dict[str, Any]:
    """
    Search node that runs all search queries in parallel using the specified search engine.

    Args:
        state: The current state containing search queries and search_engine choice.
        config: The configuration for the node.

    Returns:
        A dictionary with the list of search results.
    """
    queries = state.search_queries
    search_engine = state.search_engine

    if search_engine == "google":
        llm = create_gemini()
    elif search_engine == "openai":
        llm = create_openai()
    else:
        raise ValueError(f"Unsupported search engine: {search_engine}")

    results = await asyncio.gather(*[_search_single_query(llm, q, search_engine) for q in queries])
    return {"search_results": list(results)}

async def summary_node(state: SimpleState, config: Any) -> Dict[str, Any]:
    """
    Summary node that generates a product summary from search results, 
    selecting the LLM based on the state's search_engine.

    Args:
        state: The current state containing search results and search_engine.
        config: The configuration for the node.

    Returns:
        A dictionary with the generated summary and summary_latency.
    """
    search_results_list = state.search_results
    search_engine = state.search_engine

    # Join the list of strings
    search_results_str = "\n\n".join(search_results_list)

    # Select LLM based on search_engine
    if search_engine == "google":
        llm = create_gemini()
    elif search_engine == "openai":
        llm = create_openai()
    else:
        raise ValueError(f"Unsupported search engine in summary_node: {search_engine}")

    messages = [
        HumanMessage(content=SUMMARY_PROMPT),
        HumanMessage(content=search_results_str)
    ]
    resp = await llm.ainvoke(messages)

    # Ensure summary content is a string before returning
    summary_content = resp.content
    if isinstance(summary_content, list):
        logger.debug("Summary node returned list, joining: %s", summary_content)
        summary_str = "\n".join(map(str, summary_content))
    elif summary_content is None:
        logger.warning("Summary node returned None content.")
        summary_str = "" # Return empty string for None
    else:
        summary_str = str(summary_content)

    return {"summary": summary_str}


builder = StateGraph(SimpleState)
builder.add_node("plan", planning_node)
builder.add_node("search", search_node)
builder.add_node("summarize", summary_node)
builder.add_edge("__start__", "plan")
builder.add_edge("plan", "search")
builder.add_edge("search", "summarize")
builder.add_edge("summarize", "__end__")
graph = builder.compile()