# prompt.py
# -----------------------------------------------
# Prompt template with Langfuse integration.
# Falls back to local prompt if Langfuse unavailable.
# -----------------------------------------------
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from email_parser import EmailAnalysis

load_dotenv()

parser = PydanticOutputParser(pydantic_object=EmailAnalysis)

# -----------------------------------------------
# ANNOTATION NOTE:
# The original prompt had these drawbacks:
#
# DRAWBACK 1 — No urgency definitions:
#   "Low / Medium / High / Critical" were listed
#   without any explanation of what each means.
#   The model was guessing the boundaries,
#   causing inconsistent urgency labeling.
#   FIX: Added concrete time-based definitions.
#
# DRAWBACK 2 — Vague sentiment instruction:
#   "Identify the tone/sentiment" gave no guidance
#   on valid values. The model used "Polite" which
#   is NOT a standard sentiment (Positive/Negative/Neutral).
#   But the enum in EmailAnalysis DID include "Polite".
#   The prompt should explicitly list the allowed values
#   so the model does not invent new ones.
#   FIX: Listed all allowed sentiment enum values.
#
# DRAWBACK 3 — No "key_entities" field in prompt:
#   The prompt never asked for names, dates, amounts,
#   or deadlines — yet these are critical signals for
#   urgency and action. The model was summarizing
#   without surfacing structured entities.
#   FIX: Added Key Entities extraction step.
#
# DRAWBACK 4 — Weak JSON-only enforcement:
#   "Return ONLY valid JSON output" was not strong
#   enough — some smaller models still prepend text
#   or wrap output in ```json``` blocks.
#   FIX: Explicit rule added to ban markdown fences
#   and set null for unknown fields.
#
# DRAWBACK 5 — Comments inside prompt template:
#   The original had inline comments like
#   "# Main goal of the email" inside the prompt
#   string. These are Python comments, so they do
#   NOT appear in the actual prompt sent to the model.
#   They were misleading to developers reading the code.
#   FIX: Moved all documentation to this annotation block.
# -----------------------------------------------

FALLBACK_PROMPT = """You are an expert professional email analyst AI.
Your task is to carefully read the following email and extract structured information.

Email Content:
\"\"\"
{email_text}
\"\"\"

Perform the following analysis:

1. **Intent**: Identify the primary purpose or goal of this email.
   Choose the most specific label. Examples:
   Complaint, Invoice Request, Meeting Request, Follow-up, Project Update,
   Legal Threat, Newsletter, Announcement, Resignation, Appreciation,
   Leave Request, Budget Approval Request, Warning Letter, Vendor Proposal,
   Refund Request, Security Alert, Payment Confirmation,
   Promotion Announcement, System Maintenance Notice, Escalation

2. **Urgency**: Rate urgency using ONLY one of these four levels:
   - Low      → No deadline. FYI emails, newsletters, appreciation, announcements.
   - Medium   → Response needed within 3-7 days. Leave requests, proposals, updates.
   - High     → Response needed within 24-48 hours. Complaints, resignations,
                refund requests, budget approvals with upcoming deadlines.
   - Critical → IMMEDIATE action required within hours. Data breach,
                production down, legal threat, CEO escalation,
                angry customer threatening action, security incident.

3. **Summary**: Write a concise 1-2 sentence summary of the email.

4. **Suggested Action**: Recommend the single best next step for the recipient.

5. **Sentiment**: Identify the overall tone using ONLY one of these values:
   - Positive   → Happy, grateful, celebratory tone
   - Polite     → Professional, neutral, courteous tone
   - Neutral    → Purely informational, no emotion
   - Frustrated → Repeated issues, waiting too long, mild dissatisfaction
   - Negative   → Disappointed, critical, unhappy tone
   - Angry      → Threatening, aggressive, hostile tone

6. **Key Entities**: Extract ALL of the following if present:
   - Person names, dates, deadlines, monetary amounts, IDs, company names
   Return as a list of strings. Example: ["Kavya Reddy", "May 15th 2026", "INV-2291"]
   If truly none present, set to null.

{format_instructions}

IMPORTANT RULES:
- Return ONLY valid JSON. No preamble, no explanation, no markdown.
- Do NOT wrap output in ```json``` or any code block.
- All fields except key_entities are REQUIRED. Always provide a value.
- Follow the format instructions exactly.
"""


def get_prompt_and_parser():
    """
    Returns prompt template and parser.
    Tries to load prompt from Langfuse first.
    Falls back to local FALLBACK_PROMPT if unavailable.
    """
    try:
        from langfuse import Langfuse
        langfuse = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST")
        )
        lf_prompt = langfuse.get_prompt("email_intent_detector")
        template = lf_prompt.prompt
        print("✅ Loaded prompt from Langfuse")
    except Exception as e:
        template = FALLBACK_PROMPT
        print(f"⚠️ Using fallback prompt: {e}")

    prompt = PromptTemplate(
        template=template,
        input_variables=["email_text"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )
    return prompt, parser
