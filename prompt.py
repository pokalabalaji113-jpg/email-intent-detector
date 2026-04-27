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

FALLBACK_PROMPT = """You are an expert professional email analyst AI.
Your job is to carefully read an email and extract structured information from it.

Analyze the following email:

Email Content:
\"\"\"
{email_text}
\"\"\"

Instructions:
- Identify the main intent/purpose of this email.
- Determine how urgent this email is (Low / Medium / High / Critical).
- Write a brief 1-2 sentence summary.
- Suggest the best action the recipient should take.
- Identify the tone/sentiment of the email.

{format_instructions}

IMPORTANT:
- Return ONLY valid JSON output.
- Do NOT add any explanation before or after the JSON.
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