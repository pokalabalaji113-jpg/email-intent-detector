# prompt.py
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from email_parser import EmailAnalysis

def get_prompt_and_parser():
    parser = PydanticOutputParser(pydantic_object=EmailAnalysis)

    prompt = PromptTemplate(
        template="""You are an expert professional email analyst AI.
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
""",
        input_variables=["email_text"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    return prompt, parser