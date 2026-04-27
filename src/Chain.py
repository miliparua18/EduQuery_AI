from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

model = ChatHuggingFace(llm = llm)

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
3. If the context contains information from two DIFFERENT subjects (e.g., DSA and ML) for the same term, 
   do not mix them. Instead, explain that the term exists in both and ask the user to clarify.
4. If the context only covers one subject, provide a detailed grounded answer.
5. If the context does not contain the answer, politely state you don't have that info.


Answer:"""

prompt = ChatPromptTemplate.from_template(template)
parser = StrOutputParser()

def create_tutor_chain(retriever):
    chain = (
        {"context":retriever, "question": lambda x: x} | prompt | model | parser
    )
    return chain

