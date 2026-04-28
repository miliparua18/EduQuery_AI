import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def get_chunks(pages, subject_name):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    docs = []
    current_chapter = "Introduction"

    chapter_pattern = r'(?i)(?:chapter)\s+(\d+)\s*[:\-]?\s*(.*)'

    for p in pages:
        text = p["text"]
        page_num = p["metadata"]["page"]

        match = re.search(chapter_pattern, text)
        if match:
            current_chapter = f"Chapter {match.group(1)}: {match.group(2).strip()}"

        chunks = splitter.split_text(text)

        for c in chunks:
            docs.append(Document(
                page_content=c,
                metadata={
                    "subject": subject_name,
                    "chapter": current_chapter,
                    "page": page_num
                }
            ))

    return docs