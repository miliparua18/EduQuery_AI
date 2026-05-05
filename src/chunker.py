import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def get_chunks(pages, subject_name):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=200
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




# def get_chunks(pages, subject_name):
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=100
#     )

#     docs = []

#     chapter_pattern = r'(?i)(?:chapter)\s+(\d+)\s*[:\-]?\s*(.*)'

#     concept_pattern = r'(?i)\b(decision tree|binary tree|dbms|sql|normalization)\b'

#     for p in pages:
#         text = p["text"]
#         page_num = p["metadata"]["page"]

#         current_chapter = "Introduction"

#         match = re.search(chapter_pattern, text)
#         if match:
#             current_chapter = f"Chapter {match.group(1)}: {match.group(2).strip()}"

#         chunks = splitter.split_text(text)

#         for c in chunks:

#             # 🔥 detect concept inside chunk
#             concept_match = re.findall(concept_pattern, c.lower())

#             concept = concept_match[0] if concept_match else "general"

#             docs.append(Document(
#                 page_content=c,
#                 metadata={
#                     "subject": subject_name,
#                     "chapter": current_chapter,
#                     "concept": concept,   # ⭐ IMPORTANT ADDITION
#                     "page": page_num
#                 }
#             ))

#     return docs