# email_parser.py
# -----------------------------------------------
# Defines the structured output schema using Pydantic.
# The LLM will always return data in this exact format.
# -----------------------------------------------

from pydantic import BaseModel, Field
from typing import Literal


class EmailAnalysis(BaseModel):
    """
    Structured output model for Email Analysis.
    Every field is strictly typed to ensure clean output.
    """

    intent: str = Field(
        description=(
            "The main intent or purpose of the email. "
            "Examples: Complaint, Invoice Request, Meeting Request, "
            "Follow-up, Information Request, Appreciation, etc."
        )
    )

    urgency: Literal["Low", "Medium", "High", "Critical"] = Field(
        description=(
            "The urgency level of the email. "
            "Low = no deadline, Medium = within a week, "
            "High = within 1-2 days, Critical = immediate action needed."
        )
    )

    summary: str = Field(
        description=(
            "A brief 1-2 sentence summary of what the email is about."
        )
    )

    suggested_action: str = Field(
        description=(
            "The recommended action the recipient should take. "
            "Examples: Reply with invoice, Schedule a meeting, "
            "Escalate to manager, No action needed, etc."
        )
    )

    sentiment: Literal["Positive", "Neutral", "Negative", "Frustrated", "Angry", "Polite"] = Field(
        description="The overall tone or emotional sentiment of the email."
    )