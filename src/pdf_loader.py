import fitz


def load_textbook(file_path):
    docs = fitz.open(file_path)
    pages = []
    for i , page in enumerate(docs):
        pages.append({
            "text" : page.get_text(),
            "metadata" : {"page": i+1}
        })
        
