import asyncio
import logging
from typing import Any, Dict, List, Literal

from google.ai.generativelanguage_v1beta.types import Tool as GenAITool
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

from common.llm_models import create_gemini, create_openai
from src.evaluation.common_defs import State

logger = logging.getLogger(__name__)

SEARCH_PROMPT_TEMPLATE = """
**Role and Goal**
You are an AI shopping assistant displayed on the product detail page to help users make informed shopping decisions and save users time

**Task**
You will Analyze {product}

**Research Steps to consider**
-Generate the key purchase dimensions of the product 
-Search for relative information on product detail pages, Reddit, professional review websites, YouTube, and other credible sources.
-Combine the insights from different sources together.

**possible subsections**
Below are examples of some subsections (remove irrelevant ones and add relevant ones; change the subtitle accordingly): 
- Pros & Cons
  - separate the "Pros" and "Cons" into distinct lists
  - Avoid minor or obvious pros/cons.
  - If opinions conflict, group them as “Mixed Reviews.”
- Who it’s for / not for.
- Usage or care tips (or assembly/installation tips, etc., depending on product)
- Specific Use Case Considerations (e.g., suitability for certain ages, health conditions, environmental factors, pregnancy safe etc.)
- Insights about comparing similar products: analyze the product's specialty compared with similar products
- Show the hard work AI has done, like summarize how many youtube, reddit, articles etc AI have read to generate the content in the beginning of the analysis

**Output Format Guidelines**
- List the most important points first — order matters.
- Use concise bullet points and highlight keywords. For every bullet point, use key word+description format
- For every subtitle, highlight the words. 
- Avoid overlapping content across sections.
- Each subsection has a clear and distinct purpose.
- Avoid jargon or explain it clearly if used.
- Limit the word count to 500-700
"""


async def direct_search_node(state: State, config: Any) -> Dict[str, Any]:
    """
    Performs a direct search for the product using the specified search engine.

    Args:
        state: The current state containing the product name and search engine choice.
        config: The configuration for the node.

    Returns:
        A dictionary containing the search result.
    """
    product_name = state.product
    search_engine = state.search_engine

    # Select LLM based on search_engine
    if search_engine == "google":
        llm: ChatGoogleGenerativeAI = create_gemini()
    elif search_engine == "openai":
        llm: ChatOpenAI = create_openai()
    else:
        logger.error(
            f"Unsupported search engine in direct_search_node: {search_engine}"
        )
        raise ValueError(f"Unsupported search engine: {search_engine}")

    # Prepare the search message
    search_query = SEARCH_PROMPT_TEMPLATE.format(product=product_name)
    messages = [HumanMessage(content=search_query)]

    # Execute the search
    try:
        if search_engine == "google":
            # Assuming create_gemini returns ChatGoogleGenerativeAI
            resp = await llm.ainvoke(messages, tools=[GenAITool(google_search={})])
        elif search_engine == "openai":
            # Assuming create_openai returns ChatOpenAI
            resp = await llm.ainvoke(messages, tools=[{"type": "web_search_preview"}])
        else:
            # This case is technically handled above, but added for safety
            raise ValueError(f"Unsupported search engine: {search_engine}")

        result_str = str(resp.content)

    except Exception as e:
        logger.exception(
            f"Error during direct search for '{product_name}' using {search_engine}: {e}"
        )
        # Re-raise the exception after logging
        raise

    # Output the final search result to the standardized 'output' field
    return {"output": result_str}


# Define the graph
builder = StateGraph(State)  # Use the unified State
builder.add_node("direct_search", direct_search_node)
builder.add_edge("__start__", "direct_search")
builder.add_edge("direct_search", "__end__")
# Compile the graph, explicitly setting the output schema to be the full state
graph = builder.compile()
