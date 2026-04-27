from fastapi import FastAPI, UploadFile, File, Query
import shutil, os
from .pdf_loader import load_textbook
from .chunker import get_chunks
from .embeddings import built_vector_db, get_existing_db
from .retrievers import get_filtered_retriever
from .Chain import create_tutor_chain

app = FastAPI()
vector_db = get_existing_db()

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
        vector_db = built_vector_db(chunks)
    return {"message": f"Successfully indexed {subject}"}

@app.get("/ask")
async def ask(query: str, subject: str = None, chapter: str = None):
    if not vector_db:
        return {"error": "Vector database not initialized."}

    retriever = get_filtered_retriever(vector_db, subject, chapter)

    source_docs = retriever.invoke(query)

    chain = create_tutor_chain(retriever)
    answer = chain.invoke(query)

    citations = []
    for d in source_docs:
        citations.append({
            "Subject": d.metadata.get("subject"),
            "Chapter": d.metadata.get("chapter"),
            "Page": d.metadata.get("page"),
            "Excerpt": d.page_content[:200].strip() + "..." 
        })

    return {
        "answer": answer,
        "citations": citations
    }
