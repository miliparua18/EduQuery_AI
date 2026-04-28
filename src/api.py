from fastapi import FastAPI, UploadFile, File, Query
import shutil

from .pdf_loader import load_textbook
from .chunker import get_chunks
from .embeddings import build_vector_db, get_db
from .retrievers import get_filtered_retriever
from .Chain import create_tutor_chain
from .query_rewrite import rewrite_query

app = FastAPI()

vector_db = get_db()


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

    source_docs = retriever.invoke(improved_query)

    chain = create_tutor_chain(retriever)

    try:
        answer = chain.invoke(improved_query)
    except Exception as e:
        print("Chain error:", e)
        answer = "Unable to generate answer right now."

    citations = []
    for d in source_docs:
        citations.append({
            "Subject": d.metadata.get("subject"),
            "Chapter": d.metadata.get("chapter"),
            "Page": d.metadata.get("page"),
            "Excerpt": d.page_content[:200].strip() + "..."
        })

    return {
        "original_query": query,
        "improved_query": improved_query,
        "answer": answer,
        "citations": citations
    }