def get_filtered_retriever(vector_db, subject=None):
    """Handles semantic search with optional metadata filtering."""
    search_kwargs = {}
    if subject and subject != "ALL":
        search_kwargs["Filter"] = {"subject": subject}
    return vector_db.as_retriever(search_kwargs=search_kwargs)