from fastapi import FastAPI, UploadFile, File, Query
import shutil
from collections import Counter

from .pdf_loader import load_textbook
from .chunker import get_chunks
from .embeddings import build_vector_db, get_db
from .retrievers import get_filtered_retriever
from .Chain import create_tutor_chain
from .query_rewrite import rewrite_query
from utils.logger import setup_logger
from src.subject_router import detect_subject


logger = setup_logger(__name__)
app = FastAPI()

vector_db = get_db()
session_memory = {}

def get_session(session_id):
    if session_id not in session_memory:
        session_memory[session_id] = {}

    session = session_memory[session_id]

    session.setdefault("history", [])
    session.setdefault("pending_query", None)
    session.setdefault("subjects", None)

    return session


def get_chat_history(session_id):
    return get_session(session_id)["history"]


def update_chat_history(session_id, user_query, assistant_answer):
    session = get_session(session_id)

    session["history"].append({"role": "user", "content": user_query})
    session["history"].append({"role": "assistant", "content": assistant_answer})

    session["history"] = session["history"][-12:]


def build_contextual_query(chat_history, current_query):
    if not chat_history:
        return current_query

    last_user_messages = [
        msg["content"]
        for msg in reversed(chat_history)
        if msg["role"] == "user"
    ]

    if not last_user_messages:
        return current_query

    return f"{last_user_messages[0]} -> {current_query}"



def detect_ambiguity(source_docs, query):
    subjects = list(set(
        d.metadata.get("subject", "Unknown") for d in source_docs
    ))

    # remove Unknown noise if needed
    subjects = [s for s in subjects if s != "Unknown"]

    # STRICT RULE: more than one subject = ambiguous
    if len(subjects) > 1:
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
async def ask(
    query: str,
    session_id: str = "default",
    subject: str = None,
    chapter: str = None
):
    if not vector_db:
        return {"error": "Vector DB not initialized"}

    session = get_session(session_id)

   
    if session["subjects"]:
        matched_subject = None

        for sub in session["subjects"]:
            if sub.lower() in query.lower():
                matched_subject = sub
                break

        if matched_subject:
            subject = matched_subject
            query = session["pending_query"]

            session["pending_query"] = None
            session["subjects"] = None

    logger.info(f"Original: {query}")

    chat_history = get_chat_history(session_id)

    contextual_query = build_contextual_query(chat_history, query)

    if len(contextual_query.split()) < 12:
        improved_query = rewrite_query(contextual_query, chat_history)
    else:
        improved_query = contextual_query

    logger.info(f"Rewritten: {improved_query}")

    retriever = get_filtered_retriever(vector_db, subject, chapter)

    if subject is None or str(subject).strip().lower() == "all":

        predicted_subject = detect_subject(improved_query)
        logger.info(f"Detected subject: {predicted_subject}")

        if predicted_subject == "UNKNOWN":
            return {
                "original_query": query,
                "improved_query": improved_query,
                "answer": "Your query is ambiguous. Please specify a subject .",
                "citations": []
            }

        subject = predicted_subject

   
    source_docs = retriever.invoke(improved_query)
    # print(source_docs)
    # results = vector_db._collection.query(
    #         query_texts=[improved_query],
    #         n_results=5,
    #         include=["documents", "metadatas", "distances"]
    #     )

    # docs = results["documents"][0]
    # metas = results["metadatas"][0]
    # scores = results["distances"][0]
    # print("scores: ", scores)
    # for doc, meta, score in zip(docs, metas, scores):

    #     confidence = 1 - score

    #     print("Score: ", confidence)
    #     print("metadat:", meta)
    is_ambiguous, subjects = detect_ambiguity(source_docs, query)

    if is_ambiguous:
        session["pending_query"] = query
        session["subjects"] = subjects

        return {
            "original_query": query,
            "improved_query": improved_query,
            "answer": f"Your query relates to multiple subjects: {', '.join(subjects)}. Please specify one subject.",
            "citations": []
        }

    
    chain = create_tutor_chain(retriever)

    try:
        raw_answer = chain.invoke({
            "question": improved_query,
            "chat_history": chat_history
        }).strip()
    except Exception as e:
        print("Chain error:", e)
        raw_answer = "NOT_FOUND: Unable to generate answer right now."

    
    citations = []

    if raw_answer.startswith("FOUND:"):
        answer = raw_answer.replace("FOUND:", "").strip()

        final_docs = retriever.invoke(improved_query)
        citations = []

        for d in final_docs:
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

    update_chat_history(session_id, query, answer)

    return {
        "original_query": query,
        "improved_query": improved_query,
        "answer": answer,
        "citations": citations
    }



