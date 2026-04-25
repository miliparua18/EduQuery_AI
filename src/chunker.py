from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def get_chunks(pages, subject_name):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    docs = []
    for p in pages:
        chunks = splitter.split_text(p["text"])
        for c in chunks:
            docs.append(Document(
            page_content = c,
             metadata ={
                 "subject": subject_name,
                 "page" : p["metadat"]["page"]
                }
            ))
    return docs