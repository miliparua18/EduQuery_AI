from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from src.model import get_gemini_model
from dotenv import load_dotenv
import os

load_dotenv()

# Gemini LLM
#model = ChatGoogleGenerativeAI(
    #model="gemini-3-flash-preview",
    #google_api_key=os.getenv("GOOGLE_API_KEY"),
    #temperature=0.3
#)


model = get_gemini_model()


template = """
You are an expert University Tutor.
Review the provided context carefully.

Context: {context}
Question: {question}

INSTRUCTIONS:
1. If the question is foundational (UG level), provide a clear, structured explanation
   with definitions and simple examples.
2. If the question is specialized or theoretical (PG level), provide a rigorous
   technical analysis, mentioning complexity, trade-offs, or mathematical logic
   found in the text.
3. If the context contains information from two DIFFERENT subjects for the same term,
   do not mix them. Instead, explain that the term exists in both and ask the user to clarify.
4. If the context only covers one subject, provide a detailed grounded answer.
5. If the context does not contain the answer, politely state you don't have that info.

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)
parser = StrOutputParser()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


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