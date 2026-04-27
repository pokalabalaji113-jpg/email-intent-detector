import os
from dotenv import load_dotenv
load_dotenv()

from langfuse import Langfuse

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

print("✅ Langfuse client created!")
print("Host:", os.getenv("LANGFUSE_HOST"))
print("Public Key:", os.getenv("LANGFUSE_PUBLIC_KEY")[:15] + "...")
print("Langfuse is ready to track your LLM calls!")