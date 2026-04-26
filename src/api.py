from fastapi import FastAPI, UploadFile, File, Query
import shutil, os
from .pdf_loader import load_textbook
from .chunker import get_chunks
from .embeddings import build_vector_db, get_existing_db
from .retrievers import get_filtered_retriever
from .Chain import create_tutor_chain

app = FastAPI()
vector_db = get_existing_db()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), subject: str = Query(...)):
    global vector_db
    path = f"data/pdfs/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    pages = load_textbook(path)
    chunks = get_chunks(pages, subject)
    vector_db = build_vector_db(chunks)
    return {"message": f"Successfully indexed {subject}"}

@app.get("/ask")
async def ask(query: str, subject: str = None):
    if not vector_db: return {"error": "DB not initialized."}
    
    retriever = get_filtered_retriever(vector_db, subject)
    source_docs = retriever.invoke(query)
    answer = create_tutor_chain(retriever).invoke(query)
    
    citations = [{"subject": d.metadata.get("subject"), "page": d.metadata.get("page"), 
                  "excerpt": d.page_content[:200] + "..."} for d in source_docs]
    
    return {"answer": answer, "citations": citations}