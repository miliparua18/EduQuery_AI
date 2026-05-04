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









