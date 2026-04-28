import fitz

def load_textbook(file_path):
    pages = []
    with fitz.open(file_path) as doc:
        for i, page in enumerate(doc):
            text = page.get_text().strip()
            if text:
                pages.append({
                    "text": text,
                    "metadata": {"page": i + 1}
                })
    return pages
        
