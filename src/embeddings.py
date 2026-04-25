from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os


def get_embeddings_model():
    return HuggingFaceEmbeddings(model = "sentence-transformers/all-MiniLM-L6-v2")


def built_vector_db(docs):
    return Chroma.from_documents(
        documents= docs,
        embedding=get_embeddings_model(),
        persist_directory="./chroma_db"
    )

def get_existing_db():
    if os.path.exists("./chroma_db"):
        return Chroma(
            persist_directory="./chroma_db",
            embedding_function=get_embeddings_model()
        )
    return None