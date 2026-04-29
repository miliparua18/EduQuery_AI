EduQuery AI: Student Textbook Assistant

1. Overview

EduQuery AI is an intelligent textbook assistant that allows students to ask questions from multiple subjects like DBMS, Data Structures, and Machine Learning.
It uses Retrieval-Augmented Generation (RAG) to provide accurate, context-based answers along with source citations.


-----------------------------------------------------------------------------------------------------------------------

2. Features
 Multi-subject support (DBMS, DSA, ML)
 Semantic search using vector database
 Smart text chunking with metadata (subject, chapter, page)
 AI-generated answers using Gemini
 Ambiguity detection across subjects
 Source citations for every answer
 Chat-based UI using Streamlit


 ------------------------------------------------------------------------------------------------------------------------


 3. Project Architecture
Ingestion Phase (Build Knowledge Base)

PDF → Text Extraction → Chunking → Embeddings → Chroma DB

 Query Phase (Answer Generation)

User Query → Query Rewrite → Retriever → LLM → Answer + Citations

---------------------------------------------------------------------------------------------------------------------

4. Workflow
i.   Upload textbooks (PDFs)
ii.  System extracts and processes content
iii. Text is split into chunks with metadata
iv.  Chunks are converted into embeddings
v.   Stored in Chroma vector database
vi.  User asks a question
vii. System retrieves relevant chunks
viii. Gemini generates answer based on context
ix.   Response is shown with citations

----------------------------------------------------------------------------------------------------------------------

5. Project Structure
src/
│── pdf_loader.py        # Extract text from PDFs
│── chunker.py           # Split text into chunks
│── embeddings.py        # Create vector database
│── retrievers.py        # Filtered search
│── Chain.py             # LLM pipeline
│── query_rewrite.py     # Improve user query
│── api.py               # FastAPI backend

streamlit_app.py         # Frontend UI
ingest_all.py            # Data ingestion script


---------------------------------------------------------------------------------------------------------------------


6. Tech Stack
Frontend: Streamlit
Backend: FastAPI
LLM: Google Gemini
Embeddings: HuggingFace
Vector DB: ChromaDB
Language: Python

---------------------------------------------------------------------------------------------------------------------

7. How to Run
i. Install dependencies
pip install -r requirements.txt
ii. Run ingestion
python ingest_all.py
iii. Start backend
uvicorn src.api:app --reload
iv. Run frontend
streamlit run streamlit_app.py

---------------------------------------------------------------------------------------------------------------------

8. Example Output

Query: What is a SQL?
Answer: Explanation from textbook
Citations: Subject, Chapter, Page number


---------------------------------------------------------------------------------------------------------------------


👨‍💻 Author Name:

        MILI PARUA

