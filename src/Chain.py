from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from src.model import get_gemini_model
from Prompts.Chain_prompt import HUMAN_PROMPT, SYSTEM_PROMPT
import os

load_dotenv()

model = get_gemini_model()

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", HUMAN_PROMPT)
])
parser = StrOutputParser()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs[:3])

def format_history(history):
    if not history:
        return "No previous conversation."

    return "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in history
    )

def create_tutor_chain(retriever):
    chain = (
        {
            "context": lambda x: format_docs(retriever.invoke(x["question"])),
            "question": lambda x: x["question"],
            "chat_history": lambda x: format_history(x["chat_history"])
        }
        | prompt
        | model
        | parser
    )
    return chain









# template = """
# You are an expert University Tutor.

# Use ONLY the provided context.

# Context:
# {context}

# Question:
# {question}

# RULES:
# 1. If the answer is clearly supported by the context, begin your response with:
# FOUND:

# 2. If the topic is not covered, unrelated, or insufficiently supported by the context, begin your response with:
# NOT_FOUND:

# 3. Do not invent details.
# 4. Keep explanations educational, structured, and concise.
# 5. Stay grounded strictly in the provided context.
# 6. If multiple subjects are mixed, ask for clarification.
# 7. Follow the exact format strictly.

# Examples:

# FOUND:
# A Tree is a hierarchical data structure consisting of nodes connected by edges. It is widely used in computer science for representing relationships.

# NOT_FOUND:
# This topic is not covered in the selected textbook.

# Now answer strictly in this format.
# """

# prompt = ChatPromptTemplate.from_template(template)
# parser = StrOutputParser()


# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs[:3])


# def create_tutor_chain(retriever):
#     chain = (
#         {
#             "context": retriever | format_docs,
#             "question": lambda x: x
#         }
#         | prompt
#         | model
#         | parser
#     )
#     return chain


# template = """
# You are an expert University Tutor.

# Use ONLY the provided context and conversation history.

# Conversation History:
# {chat_history}

# Context:
# {context}

# Question:
# {question}

# RULES:
# 1. If the answer is clearly supported by the context, begin your response with:
# FOUND:

# 2. If the topic is not covered, unrelated, or insufficiently supported by the context, begin your response with:
# NOT_FOUND:

# 3. Do not invent details.
# 4. Keep explanations educational, structured, and concise.
# 5. Stay grounded strictly in the provided context.
# 6. If multiple subjects are mixed, ask for clarification.
# 7. Follow the exact format strictly.

# Examples:

# FOUND:
# A tree is a hierarchical data structure consisting of nodes connected by edges. It is widely used in computer science for representing relationships.

# NOT_FOUND:
# This topic is not covered in the selected textbook.

# Now answer strictly in this format.