from typing import Annotated, List, Optional, Sequence, TypedDict

from langchain_core.messages import BaseMessage


class State(TypedDict):
    """Represents the state of the Product Summary agent graph."""

    messages: Annotated[Sequence[BaseMessage], lambda x, y: x + y]
    url: Optional[str]
    scraped_content: Optional[str]
    summary_message: Optional[BaseMessage]


# This is used for input injection in the graph
class InputState(TypedDict):
    """Input schema for the Product Summary agent graph."""

    url: str
