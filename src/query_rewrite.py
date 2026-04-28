from langchain_google_genai import ChatGoogleGenerativeAI
from src.model import get_gemini_model
from dotenv import load_dotenv
import os

load_dotenv()

#llm = ChatGoogleGenerativeAI(
    #model="gemini-3-flash-preview",
    #google_api_key=os.getenv("GOOGLE_API_KEY"),
    #temperature=0.3
#)

llm = get_gemini_model()




def rewrite_query(query: str) -> str:
    """
    Convert short query into a better semantic-search query.
    """

    prompt = f"""
You are a query rewriting assistant.

Convert the user question into a clear and detailed search query
for a textbook assistant.

Rules:
- Keep the meaning the same
- Do not add explanations
- Make it suitable for semantic search

User Query: {query}

Rewritten Query:
"""

    try:
        response = llm.invoke(prompt)
        return response.content.strip()

    except Exception as e:
        print("Rewrite failed:", e)
        return query