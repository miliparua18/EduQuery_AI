import os
from src.pdf_loader import load_textbook
from src.chunker import get_chunks
from src.embeddings import built_vector_db

def run_ingestion():
    datasets = [
        {"file": "DBMS_Textbook.pdf", "subject": "DBMS"},
        {"file": "DataStructures_Textbook.pdf", "subject": "Data Structures"},
        {"file": "MachineLearning_Textbook.pdf", "subject": "Machine Learning"}
    ]
    
    all_chunks = []
    os.makedirs("data/pdf", exist_ok=True)

    for data in datasets:
        path = os.path.join("data", "pdf", data["file"])
        if os.path.exists(path):
            print(f" Loading {data['subject']}...")
            pages = load_textbook(path)
            all_chunks.extend(get_chunks(pages, data["subject"]))
        else:
            print(f" File not found: {path}")

    if all_chunks:
        built_vector_db(all_chunks)
        print(" Vector Database Ready!")

if __name__ == "__main__":
    run_ingestion()