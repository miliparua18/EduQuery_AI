from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def get_gemini_model():
    return ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3
    )


def get_huggingface_model():
    return HuggingFaceEmbeddings(
        model = "sentence-transformers/all-MiniLM-L6-v2"
    )