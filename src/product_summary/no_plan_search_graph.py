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
# Role & Goal
You are an AI shopping assistant shown on a product page. Your job is to save users time by providing a concise, decision-centric analysis (500–700 words).

# Data Access
You have web search capabilities. Pull information from:
- Manufacturer specifications
- Retailer Q&A sections
- Reddit threads and user discussions
- Professional reviews
- YouTube hands-on demonstrations

Prioritize consensus points that matter most for purchase decisions.

# Output Requirements (MUST follow exactly)

## Format Rules
1. **Length:** 500–700 words, inclusive
2. **Intro sentence:** "Here's an analysis of {product} based on the information available:"
3. **Headers:** Each top-level header is bold (**Header**) and appears alone on its own line with one blank line above and below
4. **Bullet format:** `- **Keyword:** description...`
   - Keyword: ≤ 4 words, bold, ends with a single colon
   - Description: ≤ 25 words, no line breaks
5. **No overlap:** Each fact appears in one header only
6. **High-impact only:** Skip trivial details (e.g., color) unless they're known deal-breakers
7. **Source synthesis:** Merge insights; don't cite URLs

## Required Header Structure (in order)

### **Pros & Cons**
- **Pros:** Exclusively positive points (max 5 bullets)
- **Cons:** Exclusively negative points (max 5 bullets)
- **Mixed Reviews (optional):** Points with conflicting opinions or both positive/negative aspects (max 5 bullets)

**De-duplication rule:** If the same theme has opposite sentiments (e.g., "easy to swallow" vs. "still too big"), don't list in both Pros and Cons. Instead, collapse into one Mixed Reviews bullet:
- **Capsule Size:** Many users praise the tiny softgels, but a minority still find them large compared to gummies.

### **User Profiles**
- **Who it's for:** 3 bullets (include age group, lifestyle/situation, budget fit)
- **Who it's not for:** 3 bullets

### **Usage & Context (optional sections)**
- **Usage or care tips:** Max 3 bullets (optional)
- **Specific use-case considerations:** Max 3 bullets (health, safety, environment, installation constraints, etc.) (optional)

### **Competitive Analysis**
- **Insights vs. similar products:** 3 bullets, each naming at least one competing product or brand

## Common Deal-Breaker Topics (cover when relevant)
- Warranty length
- Certifications (e.g., NSF, IFOS)
- Subscription or filter replacement costs
- Compatibility requirements (C-wire, pods, cooktops)
- Lifespan/durability benchmarks

# Self-Check (before replying)
- [ ] Word count between 500–700?
- [ ] All required headers present, on their own line, in correct order?
- [ ] Every bullet follows **Keyword:** pattern?
- [ ] No duplicate facts across sections?
- [ ] Mixed aspects only in Mixed Reviews section?
- [ ] Named at least one competitor in comparison section?
- [ ] Omitted headers explained (if any)?

**If any check fails, fix it before returning the answer.**
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
