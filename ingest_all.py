import os
from src.pdf_loader import load_textbook
from src.chunker import get_chunks
from src.embeddings import build_vector_db

def normalize_subject(subject):
    mapping = {
        "ml": "Machine Learning",
        "machine learning": "Machine Learning",
        "dbms": "DBMS",
        "ds": "Data Structures",
        "data structures": "Data Structures"
    }
    return mapping.get(subject.lower(), subject)

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
            print(f"Loading {data['subject']}...")

            pages = load_textbook(path)
            chunks = get_chunks(pages, data["subject"])

            
            for c in chunks:
                if not c.metadata:
                    c.metadata = {}
                c.metadata["subject"] = data["subject"]

            all_chunks.extend(chunks)

        else:
            print(f"File not found: {path}")

    if all_chunks:
        db = build_vector_db(all_chunks)
        print("Vector Database Ready!")

        return db


if __name__ == "__main__":
    run_ingestion()


