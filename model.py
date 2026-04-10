# model.py
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "❌ GROQ_API_KEY not found! "
            "Please add it to your .env file."
        )

    llm = ChatGroq(
        model="llama-3.1-8b-instant",   # ✅ FIXED — active model
        groq_api_key=api_key,
        temperature=0.1,
    )

    return llm