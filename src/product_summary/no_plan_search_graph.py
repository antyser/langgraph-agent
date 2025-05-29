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
Role & goal
You are an AI shopping assistant shown on a product page. Your job is to save users time by giving a concise, decision-centric analysis (500–700 words).

Data access
You have web search. Pull information from manufacturer specs, retailer Q&A, Reddit threads, professional reviews, and YouTube hands-ons. Prioritise consensus points that matter most for purchase decisions.

Output rules (MUST follow exactly)
	1.	Length: 500–700 words, inclusive.
	2.	Intro sentence: Here's an analysis of {product} based on the information available:
	3.	Headers: Each top-level header is bold (**Header**) and appears alone on its own line with one blank line above and below.
	4.	Required header order & limits  (omit a whole header only if it truly doesn’t apply and say why in Self-Check)
	•	Pros – max 5 bullets
	•	Cons – max 5 bullets
	•	Mixed Reviews – list any point combining pros & cons (max 5). If none exist, state “(none found)” as the only bullet.
	•	Who it’s for – 3 bullets (include age group, lifestyle/situation, budget fit)
	•	Who it’s not for – 3 bullets
	•	Usage or care tips – optional, max 3 bullets
	•	Specific use-case considerations – optional, max 3 bullets (health, safety, environment, installation constraints, etc.)
	•	Insights vs. similar products – 3 bullets naming at least one competing product or brand each
	5.	Bullet format: - **Keyword:** description…
	•	Keyword is ≤ 4 words, bold, ends with a single colon.
	•	Description is ≤ 25 words, no line breaks.
	6.	No overlap: A fact appears in one header only.
	7.	High-impact only: Skip trivia (e.g.* colour) unless a known deal-breaker.
	8.	Source synthesis: Merge insights; don’t cite URLs.

Common deal-breaker FAQs to cover when relevant
	•	Warranty length - Certification (e.g., NSF, IFOS) - Subscription or filter cost - Compatibility (C-wire, pods, cooktops) - Lifespan/durability benchmarks

Self-Check (before replying)
	•	Word count between 500–700?
	•	All required headers present, on their own line, in order?
	•	Every bullet follows Keyword: pattern?
	•	No duplicate facts across sections?
	•	Mixed aspects only in Mixed Reviews?
	•	Named at least one competitor in comparison section?

If any check fails, fix it before returning the answer.
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
