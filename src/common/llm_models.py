import os
from langchain_google_genai import ChatGoogleGenerativeAI


GEMINI_2_0_FLASH = "gemini-2.0-flash"
GEMINI_2_5_FLASH_PREVIEW = "gemini-2.5-flash-preview-04-17"
GEMINI_2_5_PRO_PREVIEW = "gemini-2.5-pro-preview-03-25"


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