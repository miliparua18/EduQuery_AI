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
You are an expert University Tutor for CSE students.
Use the following pieces of retrieved context to answer the question. 

RULES:
1. If the answer isn't in the context, say you don't know based on the textbooks.
2. If there occurs context ambiguity  then check if the context mentions 
   both Data Structures and Machine Learning trees and ask for clarification.
3. Always cite the page number.

Context: {context}
Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)
parser = StrOutputParser()

def create_tutor_chain(retriever):
    chain = (
        {"context":retriever, "question": lambda x: x} | prompt | model | parser
    )
    return chain

