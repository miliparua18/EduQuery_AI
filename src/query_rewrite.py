from langchain_huggingface import HuggingFaceEndpoint
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_huggingface import HuggingFaceEndpoint
import os
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    temperature=0.3,
    max_new_tokens=80
)

def rewrite_query(query: str) -> str:
    """
    Convert short query → detailed retrieval query
    """

    prompt = f"""
You are a query rewriting assistant.

Convert the user question into a clear and detailed search query for a textbook assistant.

Rules:
- Keep meaning same
- Do not add explanation
- Make it suitable for semantic search

User Query: {query}

Rewritten Query:
"""

    try:
        response = llm.invoke(prompt)
        return response.strip()

    except Exception as e:
        print("Rewrite failed:", e)
        return query