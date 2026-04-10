# prompt.py
# -----------------------------------------------
# Builds the Prompt Template that will be sent to the LLM.
# Uses LangChain PromptTemplate + PydanticOutputParser.
# -----------------------------------------------

from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from email_parser import EmailAnalysis


def get_prompt_and_parser():
    """
    Creates and returns:
    - prompt: The PromptTemplate to send to LLM
    - parser: The PydanticOutputParser to parse LLM response

    Returns:
        tuple: (prompt, parser)
    """

    # Step 1: Create the output parser based on our Pydantic model
    parser = PydanticOutputParser(pydantic_object=EmailAnalysis)

    # Step 2: Create the prompt template
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