# email_parser.py
from pydantic import BaseModel, Field
from typing import Literal


class EmailAnalysis(BaseModel):
    intent: str = Field(
        description="The main intent or purpose of the email. Examples: Complaint, Invoice Request, Meeting Request, Follow-up, etc."
    )
    urgency: Literal["Low", "Medium", "High", "Critical"] = Field(
        description="Urgency level. Low=no deadline, Medium=within a week, High=within 1-2 days, Critical=immediate."
    )
    summary: str = Field(
        description="A brief 1-2 sentence summary of what the email is about."
    )
    suggested_action: str = Field(
        description="The recommended action the recipient should take."
    )
    sentiment: Literal["Positive", "Neutral", "Negative", "Frustrated", "Angry", "Polite"] = Field(
        description="The overall tone or emotional sentiment of the email."
    )