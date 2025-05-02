import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


GEMINI_2_0_FLASH = "gemini-2.0-flash"
GEMINI_2_5_FLASH_PREVIEW = "gemini-2.5-flash-preview-04-17"
GEMINI_2_5_PRO_PREVIEW = "gemini-2.5-pro-preview-03-25"
GPT_4_1 = "gpt-4.1-2025-04-14"


def create_gemini(model_name: str = GEMINI_2_5_FLASH_PREVIEW) -> ChatGoogleGenerativeAI:
    """
    Create a LangChain ChatGoogleGenerativeAI instance configured for product summary.

    Args:
        model_name: Name of the Gemini model to use.

    Returns:
        A ChatGoogleGenerativeAI instance.
    """
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.8,
        google_api_key=os.environ.get("GEMINI_API_KEY"),
    )


def create_openai(model_name: str = GPT_4_1) -> ChatOpenAI:
    """
    Create a LangChain ChatOpenAI instance.

    Assumes OPENAI_API_KEY environment variable is set.

    Args:
        model_name: Name of the OpenAI model to use (e.g., "gpt-4o", "gpt-3.5-turbo").

    Returns:
        A ChatOpenAI instance.
    """
    return ChatOpenAI(
        model=model_name,
        temperature=0.8,
        use_responses_api=True,
        api_key=os.environ.get("OPENAI_API_KEY"),
    )