from fastapi import FastAPI, UploadFile, File, Query
import shutil
from collections import Counter

from .pdf_loader import load_textbook
from .chunker import get_chunks
from .embeddings import build_vector_db, get_db
from .retrievers import get_filtered_retriever
from .Chain import create_tutor_chain
from .query_rewrite import rewrite_query

app = FastAPI()

vector_db = get_db()


def detect_ambiguity(source_docs, query, threshold=0.6):
    subjects = list(set(d.metadata.get("subject", "Unknown") for d in source_docs))

    if len(query.split()) <= 3 and len(subjects) > 1:
        return True, subjects

    
    subject_counts = Counter(
        d.metadata.get("subject", "Unknown") for d in source_docs
    )

    if len(subject_counts) <= 1:
        return False, subjects

    total = sum(subject_counts.values())
    dominant_ratio = max(subject_counts.values()) / total

    if dominant_ratio < threshold:
        return True, subjects

    return False, subjects


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), subject: str = Query(...)):
    global vector_db

    path = f"data/pdf/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = load_textbook(path)
    chunks = get_chunks(pages, subject)

    if vector_db:
        vector_db.add_documents(chunks)
    else:
        vector_db = build_vector_db(chunks)

    return {"message": f"Successfully indexed {subject}"}


@app.get("/ask")
async def ask(query: str, subject: str = None, chapter: str = None):

    if not vector_db:
        return {"error": "Vector DB not initialized"}

    print("Original:", query)

    if len(query.split()) < 6:
        improved_query = rewrite_query(query)
    else:
        improved_query = query

    print("Rewritten:", improved_query)

    retriever = get_filtered_retriever(vector_db, subject, chapter)

    if subject is None or str(subject).strip().lower() == "all":
        temp_retriever = vector_db.as_retriever(search_kwargs={"k": 10})
        source_docs = temp_retriever.invoke(improved_query)
    else:
        source_docs = retriever.invoke(improved_query)

    if subject is None or str(subject).strip().lower() == "all":
        is_ambiguous, subjects = detect_ambiguity(source_docs, query)

        if is_ambiguous:
            return {
                "original_query": query,
                "improved_query": improved_query,
                "answer": f"Your query relates to multiple subjects: {', '.join(subjects)}. Please select a subject for a more accurate answer.",
                "citations": []
            }

    chain = create_tutor_chain(retriever)

    try:
        raw_answer = chain.invoke(improved_query).strip()
    except Exception as e:
        print("Chain error:", e)
        raw_answer = "NOT_FOUND: Unable to generate answer right now."

    citations = []

    if raw_answer.startswith("FOUND:"):
        answer = raw_answer.replace("FOUND:", "").strip()

        for d in source_docs:
            citations.append({
                "Subject": d.metadata.get("subject"),
                "Chapter": d.metadata.get("chapter"),
                "Page": d.metadata.get("page"),
                "Excerpt": d.page_content[:200].strip() + "..."
            })
    elif raw_answer.startswith("NOT_FOUND:"):
        answer = raw_answer.replace("NOT_FOUND:", "").strip()

    else:
        answer = raw_answer
        citations = []

    return {
        "original_query": query,
        "improved_query": improved_query,
        "answer": answer,
        "citations": citations
    }
    



