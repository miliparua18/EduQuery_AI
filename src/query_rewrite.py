from src.model import get_gemini_model
from dotenv import load_dotenv
from Prompts.query_rewrite_prompt import SYSTEM_PROMPT, HUMAN_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import os

load_dotenv()


llm = get_gemini_model()


def rewrite_query(query: str, history=None) -> str:
    context = ""

    # 🔹 Add history if exists
    if history:
        for h in history[-3:]:
            context += f"User: {h['user']}\nAssistant: {h['bot']}\n"

    context += f"User Query: {query}"

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=HUMAN_PROMPT.format(
            context=context,
            query=query
        ))
    ]

    try:
        response = llm.invoke(messages)
        return response.text.strip()

        # content = response.content

        # if isinstance(content, list):
        #     content = " ".join(
        #         item.get("text", str(item)) if isinstance(item, dict) else str(item)
        #         for item in content
        #     )

        # rewritten = str(content).strip()
        # rewritten = rewritten.split("\n")[0].replace('"', "")

        # return rewritten

    except Exception as e:
        print("Rewrite failed:", e)
        return query
    






    # def rewrite_query(query: str, history=None) -> str:
#     """
#     Convert short query into a better semantic-search query.
#     """
#     context = ""
#     if history:
#         for h in history[-3:]:
#             context += f"User: {h['user']}\nAssistant: {h['bot']}\n"

#     context += f"User Query: {query}"


#     prompt = f"""
# You are a query rewriting assistant.

# Convert the user question into a clear and detailed search query
# for a textbook assistant.

# Rules:
# - Keep the meaning the same
# - Do not add explanations
# - Make it suitable for semantic search

# Conversation:
# {context}

# Rewritten Query:
# """

#     try:
#         response = llm.invoke(prompt)
#         return response.text.strip()
#     except Exception as e:
#         print("Rewrite failed:", e)
#         return query
    