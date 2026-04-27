# main.py
# -----------------------------------------------
# Core logic — connects Prompt → LLM → Parser
# with Langfuse tracing support.
# -----------------------------------------------

import time
from prompt import get_prompt_and_parser
from model import get_llm, get_langfuse_handler
from email_parser import EmailAnalysis


def analyze_email(email_text: str) -> EmailAnalysis:
    """
    Analyzes an email and returns structured analysis.
    All LLM calls are traced via Langfuse.

    Args:
        email_text (str): Raw email content to analyze.

    Returns:
        EmailAnalysis: Pydantic model with all analysis fields.

    Raises:
        ValueError: If email is empty.
        Exception: If LLM call or parsing fails.
    """

    # Input validation
    if not email_text or not email_text.strip():
        raise ValueError("⚠️ Email text cannot be empty.")

    # Setup
    prompt, parser = get_prompt_and_parser()
    llm = get_llm()
    handler = get_langfuse_handler()

    # Build chain
    chain = prompt | llm | parser

    # Invoke chain with Langfuse tracing if available
    if handler:
        result = chain.invoke(
            {"email_text": email_text},
            config={"callbacks": [handler]}
        )
    else:
        result = chain.invoke({"email_text": email_text})

    return result


def analyze_with_retry(email_text: str, retries: int = 3, wait: int = 5) -> EmailAnalysis:
    """
    Retries analyze_email on failure.
    Useful for handling temporary LLM overload errors.

    Args:
        email_text (str): Raw email content.
        retries (int): Number of retry attempts.
        wait (int): Seconds to wait between retries.

    Returns:
        EmailAnalysis: Final structured result.
    """
    for attempt in range(retries):
        try:
            return analyze_email(email_text)
        except Exception as e:
            err = str(e)
            if "503" in err or "overloaded" in err.lower() or "unavailable" in err.lower():
                if attempt < retries - 1:
                    print(f"⏳ LLM overloaded. Retrying in {wait}s... (attempt {attempt+1})")
                    time.sleep(wait)
                else:
                    raise Exception(
                        "LLM is overloaded right now. "
                        "Please wait a minute and try again."
                    )
            else:
                raise


# ── Quick test ─────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*60)
    print("   📧 Email Intent & Urgency Detector — Test Run")
    print("="*60)

    test_email = """
    Hi Team,
    I've been waiting for the project deliverables for over 3 weeks.
    Our client presentation is tomorrow morning at 9 AM sharp.
    If I don't receive the files tonight, the entire deal may fall through.
    Please respond IMMEDIATELY.
    - David (Project Manager)
    """

    try:
        result = analyze_with_retry(test_email)
        print(f"  🎯 Intent          : {result.intent}")
        print(f"  ⚡ Urgency Level   : {result.urgency}")
        print(f"  📝 Summary         : {result.summary}")
        print(f"  ✅ Suggested Action: {result.suggested_action}")
        print(f"  😊 Sentiment       : {result.sentiment}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    print("="*60)