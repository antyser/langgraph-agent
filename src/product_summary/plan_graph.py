import asyncio
import os
import time
from common.llm_models import create_gemini
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from google.ai.generativelanguage_v1beta.types import Tool as GenAITool
from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any

PLANNING_PROMPT = """
You are an expert product researcher. Given a product name or description, generate 3-5 specific search queries that will help gather the most important information for a consumer summary (e.g., main features, pros, cons, who it's for, common complaints, ingredients, etc.).
Return only the list of queries. Make sure the queries are not overlapping.
"""

SEARCH_PROMPT = """
Use the Google Search tool to answer the following query about the product. Return the most relevant facts and details.
"""

SUMMARY_PROMPT = """You are an expert research summarizer that synthesizes information follow the original instructions.
    # Response Guidelines:
- Provide detailed, structured responses clearly divided into logical sections and subsections.
- Explicitly cite all sources, including the title and direct URL.
- Prioritize accuracy, thoroughness, and relevance; completeness is more important than brevity.
- Clearly distinguish between confirmed facts, well-supported conclusions, informed predictions, and speculative statements. Explicitly label speculative or emerging insights as such.
- Anticipate and proactively address potential follow-up questions or related relevant context that enhances overall comprehension.
- Incorporate relevant recent advancements, unconventional perspectives, or alternative viewpoints, explicitly marking these as emerging or speculative when applicable."""

class SimpleState(TypedDict):
    """Represents the state for the simple product summary agent graph."""
    product: str
    search_queries: List[str]
    search_results: List[str]
    summary: str

def _parse_queries_from_response(response_content: str) -> List[str]:
    """Parse the queries from the LLM response, handling bullet points or numbered lists."""
    lines = [line.strip("- ").strip() for line in response_content.strip().split("\n") if line.strip()]
    return [line for line in lines if line]

async def planning_node(state: Dict[str, Any], config: Any) -> Dict[str, Any]:
    """
    Planning node that generates search queries for a given product and logs latency.

    Args:
        state: The current state containing the product.
        config: The configuration for the node.

    Returns:
        A dictionary with the generated search queries and plan_latency.
    """
    product = state["product"]
    llm = create_gemini()
    messages = [
        HumanMessage(content=PLANNING_PROMPT),
        HumanMessage(content=f"Product: {product}")
    ]
    response = await llm.ainvoke(messages)
    queries = _parse_queries_from_response(response.content)
    return {"search_queries": queries}

async def _search_single_query(llm: ChatGoogleGenerativeAI, query: str) -> str:
    """
    Helper function to perform a single search query using Gemini and Google Search tool.

    Args:
        llm: The Gemini LLM instance.
        query: The search query string.

    Returns:
        The search result as a string.
    """
    messages = [
        HumanMessage(content=SEARCH_PROMPT),
        HumanMessage(content=query)
    ]
    resp = await llm.ainvoke(messages, tools=[GenAITool(google_search={})])
    return resp.content

async def search_node(state: Dict[str, Any], config: Any) -> Dict[str, Any]:
    """
    Search node that runs all search queries in parallel using Gemini and Google Search tool, and logs latency.

    Args:
        state: The current state containing search queries.
        config: The configuration for the node.

    Returns:
        A dictionary with the list of search results and search_latency.
    """
    queries = state["search_queries"]
    llm = create_gemini()
    results = await asyncio.gather(*[_search_single_query(llm, q) for q in queries])
    return {"search_results": list(results)}

async def summary_node(state: Dict[str, Any], config: Any) -> Dict[str, Any]:
    """
    Summary node that generates a product summary from search results and logs latency.

    Args:
        state: The current state containing search results.
        config: The configuration for the node.

    Returns:
        A dictionary with the generated summary and summary_latency.
    """
    search_results = "\n\n".join(state["search_results"])
    llm = create_gemini()
    messages = [
        HumanMessage(content=SUMMARY_PROMPT),
        HumanMessage(content=search_results)
    ]
    resp = await llm.ainvoke(messages)
    return {"summary": resp.content}


builder = StateGraph(SimpleState)
builder.add_node("plan", planning_node)
builder.add_node("search", search_node)
builder.add_node("summarize", summary_node)
builder.add_edge("__start__", "plan")
builder.add_edge("plan", "search")
builder.add_edge("search", "summarize")
builder.add_edge("summarize", "__end__")
graph = builder.compile()