"""Product Summary Agent Graph Definition."""

import json
import os
from typing import Dict, List, Optional

import httpx
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from langgraph.graph import StateGraph
from loguru import logger

from scraper.bright_data.amazon import scrape_amazon_product
from src.common.llm_models import create_gemini
from src.product_summary.config import Configuration
from src.product_summary.state import InputState, State


# Structured prompt for product summaries
STRUCTURED_PROMPT = """
You are an AI assistant tasked with creating concise product summaries for average consumers based on the product mentioned in the user's request. Your goal is to search for and extract the most crucial information about the product to help someone quickly understand its main benefits and potential drawbacks, aiding their purchase decision.

Please search for information about the product mentioned and create a summary with the following structure:

1. **What it is & Who it's for**: Start with a very brief (1-2 sentences) description of the product and its primary purpose or ideal user.

2. **Key Benefits (What's Good)**: List the top 3-4 most significant advantages users experience. Focus on the results (e.g., "Noticeably improves water taste and removes chlorine smell," "Easy filter changes without tools"). Do not simply re-list features from the product description unless they directly translate to a key, unique benefit.

3. **Potential Downsides (Keep in Mind)**: List the top 3-4 most important drawbacks or common issues mentioned in reviews/sources. Be as specific as possible based on the available information (e.g., "Some users report difficulty contacting customer support," "Requires dedicated faucet installation").

4. **Bottom Line**: A short (1-2 sentence) concluding thought summarizing the main trade-off or suitability (e.g., "A good option for significantly better-tasting water if you prioritize mineral retention, but be mindful of potential leak issues reported by some users.").

Return the summary in markdown format and the summary only. No other text.
"""

# Remove the old generate_summary_stream function
# async def generate_summary_stream(...) -> AsyncGenerator[str, None]: ...


# Add scrape_product_node
async def scrape_product_node(
    state: State, config: RunnableConfig
) -> Dict[str, Optional[str]]:
    resp = await scrape_amazon_product(state.get("url"))
    logger.info(f"Scraped content: {resp}")
    return {"scraped_content": str(resp)}


# Refactor call_summary_node
async def call_summary_node(
    state: State, config: RunnableConfig
) -> Dict[str, BaseMessage | None]:
    """
    Node that calls the summary generation function using LangChain Gemini integration,
    now using scraped content from the state.

    Args:
        state: The current state containing messages and scraped_content.
        config: Configuration for the runnable.

    Returns:
        A dictionary with the 'summary_message' field containing the AI response or None.
    """
    logger.info("---GENERATE SUMMARY---")
    configuration = Configuration.from_runnable_config(config)
    logger.info(f"State received in call_summary_node: {state}")

    # Extract scraped content from the state
    scraped_content = state.get("scraped_content")

    if not scraped_content:
        logger.error("No scraped content found in state for summarization.")
        # If scraping failed, the error message might already be in state["messages"]
        # We could return here, or return a specific error message.
        # Let's return an error message to make it explicit.
        return {
            # Return None for the message if scraping failed
            "summary_message": AIMessage(
                content="Scraping failed, cannot generate summary."
            )
        }

    try:
        # Create the LLM with LangChain's Gemini integration
        llm = create_gemini(configuration.model)

        # Prepare messages for the LLM
        # Use SystemMessage for the prompt and HumanMessage for the input (scraped content)
        prepared_messages = [
            SystemMessage(content=STRUCTURED_PROMPT),
            # Provide the scraped content as the context for summarization
            HumanMessage(
                content=f"Here are some the product details:\n\n{scraped_content}. You should summarize the product based on the details provided. Think about what information are needed for user to make a purchase decision. if the information cannot be found, use search and fill those information."
            ),
        ]

        # Stream the LLM response
        summary_parts = []
        response = None  # Initialize response
        async for chunk in llm.astream(prepared_messages, config=config):
            # Check if chunk is AIMessage and has content
            if isinstance(chunk, AIMessage) and isinstance(chunk.content, str):
                summary_parts.append(chunk.content)
            response = (
                chunk  # Keep track of the last chunk for final AIMessage attributes
            )

        # Reconstruct the final AIMessage with aggregated content
        if response is not None:
            # Use attributes from the last chunk but with combined content
            final_content = "".join(summary_parts)
            response = AIMessage(
                content=final_content,
                id=response.id,
                response_metadata=response.response_metadata,
                tool_calls=response.tool_calls,
                usage_metadata=response.usage_metadata,
            )
        else:
            # Handle case where stream yields nothing
            logger.warning("LLM stream yielded no chunks.")
            response = AIMessage(content="")  # Create an empty message

        # Log the response for debugging
        logger.info(f"Generated response type: {type(response)}")

        if not response or not hasattr(response, "content") or not response.content:
            logger.error("Empty or invalid response received from LLM")
            return {
                # Return error message
                "summary_message": AIMessage(content="LLM returned empty response.")
            }

        # The response should already be an AIMessage
        # Ensure tool calls are handled if they appear unexpectedly, although the prompt asks for text.
        if response.tool_calls:
            logger.warning(f"Unexpected tool calls in response: {response.tool_calls}")
            # Decide how to handle tool calls if needed, for now, just return content
            return {"summary_message": AIMessage(content=response.content)}

        # Return the AIMessage response
        return {"summary_message": response}

    except Exception as e:
        logger.error(f"Error in call_summary_node: {e}", exc_info=True)
        # Send an error message if something goes wrong
        return {
            "summary_message": AIMessage(content=f"Error generating summary: {str(e)}")
        }


# Define the graph
builder = StateGraph(State, input=InputState, config_schema=Configuration)

# Add the nodes
builder.add_node("scrape", scrape_product_node)
builder.add_node("generate", call_summary_node)

# Set the entry point to the new scrape node
builder.add_edge("__start__", "scrape")

# Connect scrape node to generate node
builder.add_edge("scrape", "generate")

# Set the end point
builder.add_edge("generate", "__end__")

# Compile the graph
graph = builder.compile()
graph.name = "Product Summary Agent"

# Optional: Add memory (commented out, assumed setup elsewhere if needed)
# memory = SqliteSaver.from_conn_string(":memory:")
# graph = builder.compile(checkpointer=memory)
