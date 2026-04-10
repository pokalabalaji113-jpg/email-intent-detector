# main.py
# -----------------------------------------------
# Core logic of the Email Intent & Urgency Detector.
# Connects: Prompt → LLM → Parser → Structured Output
# -----------------------------------------------

from prompt import get_prompt_and_parser
from model import get_llm
from email_parser import EmailAnalysis


def analyze_email(email_text: str) -> EmailAnalysis:
    """
    Analyzes an email and returns structured analysis.

    Args:
        email_text (str): The raw email content to analyze.

    Returns:
        EmailAnalysis: A Pydantic object with intent, urgency,
                       summary, suggested_action, and sentiment.

    Raises:
        ValueError: If email_text is empty.
        Exception: If LLM call or parsing fails.
    """

    # Input validation
    if not email_text or not email_text.strip():
        raise ValueError("⚠️ Email text cannot be empty. Please provide valid email content.")

    # Step 1: Get prompt template and output parser
    prompt, parser = get_prompt_and_parser()

    # Step 2: Get the LLM
    llm = get_llm()

    # Step 3: Build the chain using LCEL (LangChain Expression Language)
    # Flow: prompt → llm → parser
    chain = prompt | llm | parser

    # Step 4: Invoke the chain with the email text
    result = chain.invoke({"email_text": email_text})

    return result


# -----------------------------------------------
# Quick test when running: python main.py
# -----------------------------------------------
if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("   📧 Email Intent & Urgency Detector — Test Run")
    print("=" * 60)

    # Test Email 1: Critical/Urgent
    email_1 = """
    Hi Team,

    I've been waiting for the project deliverables for over 3 weeks now.
    Our client presentation is tomorrow morning at 9 AM sharp.
    If I don't receive the files by tonight, the entire deal might fall through.
    This is costing the company thousands of dollars.

    Please respond IMMEDIATELY.

    - David (Project Manager)
    """

    # Test Email 2: Low urgency
    email_2 = """
    Hey Sarah,

    Hope you're having a great week! Just wanted to check in on the Q3 
    report we talked about. Whenever you get a chance, could you send 
    it over? No rush at all — next week works perfectly fine.

    Thanks so much!
    - Mike
    """

    test_emails = [
        ("CRITICAL EMAIL TEST", email_1),
        ("LOW URGENCY EMAIL TEST", email_2),
    ]

    for label, email in test_emails:
        print(f"\n{'─' * 60}")
        print(f"🧪 {label}")
        print(f"{'─' * 60}")
        print(f"📩 Input:\n{email.strip()}\n")

        try:
            result = analyze_email(email)

            print("📊 ANALYSIS RESULT:")
            print(f"  🎯 Intent          : {result.intent}")
            print(f"  ⚡ Urgency Level   : {result.urgency}")
            print(f"  📝 Summary         : {result.summary}")
            print(f"  ✅ Suggested Action: {result.suggested_action}")
            print(f"  😊 Sentiment       : {result.sentiment}")

        except Exception as e:
            print(f"  ❌ Error: {str(e)}")

    print(f"\n{'=' * 60}\n")