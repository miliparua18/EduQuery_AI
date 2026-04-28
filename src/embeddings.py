import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from src.model import get_huggingface_model

load_dotenv()

CHROMA_DB_DIR = "./chroma_db"


#def get_embeddings():
    #return HuggingFaceEmbeddings(
        #model = "sentence-transformers/all-MiniLM-L6-v2"
    #)



def get_db():
    return Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=get_huggingface_model()
    )


def build_vector_db(docs):
    db = Chroma.from_documents(
        documents=docs,
        embedding=get_huggingface_model(),
        persist_directory=CHROMA_DB_DIR
    )
    return db