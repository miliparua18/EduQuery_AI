from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.model import get_gemini_model
import os

load_dotenv()

model = get_gemini_model()

template = """
You are an expert University Tutor.

Use ONLY the provided context.

Context:
{context}

Question:
{question}

RULES:
1. If the answer is clearly supported by the context, begin your response with:
FOUND:

2. If the topic is not covered, unrelated, or insufficiently supported by the context, begin your response with:
NOT_FOUND:

3. Do not invent details.
4. Keep explanations educational, structured, and concise.
5. Stay grounded strictly in the provided context.
6. If multiple subjects are mixed, ask for clarification.
7. Follow the exact format strictly.

Examples:

FOUND:
A tree is a hierarchical data structure consisting of nodes connected by edges. It is widely used in computer science for representing relationships.

NOT_FOUND:
This topic is not covered in the selected textbook.

Now answer strictly in this format.
"""

prompt = ChatPromptTemplate.from_template(template)
parser = StrOutputParser()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs[:3])


def create_tutor_chain(retriever):
    chain = (
        {
            "context": retriever | format_docs,
            "question": lambda x: x
        }
        | prompt
        | model
        | parser
    )
    return chain