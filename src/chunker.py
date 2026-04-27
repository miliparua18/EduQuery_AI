import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def get_chunks(pages, subject_name):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = []
    current_chapter = "Introduction"

    for p in pages:
        text = p["text"]
        page_num = p["metadata"]["page"]

        chapter_pattern = r'(?i)(?:Chapter|CHAPTER|Chap)\s+(\d+|[IVXLC]+)(?:\s+—\s+|\s*[:.\-]?\s*)(.*)'
        match = re.search(chapter_pattern, text)
        
        if match:
            chapter_num = match.group(1)
            chapter_title = match.group(2).strip()
            current_chapter = f"Chapter {chapter_num}: {chapter_title}" if chapter_title else f"Chapter {chapter_num}"

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