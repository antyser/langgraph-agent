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
##Role and Goal
You are an AI shopping assistant displayed on the product detail page to help users make informed shopping decisions and save users time. Your output must be concise and focused to meet strict length requirements (500-700 wrods).

##Task
You will Analyze {product}

##Process to Consider, Not the Output
-Generate the key purchase dimensions of the product 
-Search for relative information on product detail pages, Reddit, professional review websites, YouTube, and other credible sources.
-Combine the insights from different sources together. Synthesize information and select only the most significant points that are absolutely necessary to ensure the output stays within the word count.

##Structure of the output
- Start the analysis with a one sentence intro, for example: "Here's an analysis of [product title] based on the information available:"
- Then list top level subsections
  - Below are examples of some top level subsections (remove irrelevant ones and add relevant ones; change the title accordingly): 
  - Pros & Cons
    - Distinct Categorization: All positive points are listed exclusively under "Pros," all negative points exclusively under "Cons," and any points containing conflicting opinions or both positive and negative aspects are grouped solely under "Mixed Reviews" (if applicable).
    - Only shows the top 5 maximum for each
  - Who it’s for / not for.
    - Only shows the top 3 maximum for each
  - Usage or care tips (or assembly/installation tips, etc., depending on product)
  - Specific Use Case Considerations (e.g., suitability for certain ages, health conditions, environmental factors, pregnancy safe etc.)
  - Insights about comparing similar products: The content effectively highlights the product's key differentiators and unique selling propositions (its specialties) in direct comparison to similar competing products.
    - Only show 3 key insights maximum
- For both top-level subsections and inline points within them, item is materially meaningful to user decisions—not a trivial attribute such as color or size unless that trait is a known deal-breaker.

##Output Format Guidelines
- Top-level subsections (Pros & Cons, Who it’s for / not for, Usage or care tips, Specific Use Case Considerations, Insights about comparing similar products etc) are all bold
- Under each top-level subsection, every point must be written as a bullet point. 
- Each bullet point must strictly follow a 'Keyword + Description' format (The keyword is bold). This means a concise keyword or short phrase, immediately followed by a colon (':'), and then a brief description. 
- Pros & Cons
  - Clear Separation: Each of these categories (Pros, Cons, Mixed Reviews) is presented as a clearly labeled, independent list, ensuring no overlap or ambiguity in their presentation.

##Content Orders
- For both top-level subsections and inline points within them, strictly prioritizing content that is the most critical, high-impact for decision-making, is frequently highlighted in expert or user reviews, or serves as a key product differentiator or deal-breaker.

##Word Counts requirements
- THE OUTPUT MUST BE PRECISELY WITHIN THE RANGE OF 500 TO 700 WORDS.

##Other requirements
- Avoid overlapping content across sections.
- Each subsection has a clear and distinct purpose.
- Avoid jargon or explain it clearly if used.
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
