def get_filtered_retriever(vector_db, subject=None, chapter=None):
    """
    Configures retrieval:
    - k=5: Returns top 5 relevant chunks
    - filter: Limits search to specific subject/chapter
    """
    search_kwargs = {"k": 5}
    filters = {}

    if subject and subject != "All":
        filters["subject"] = subject
    
    if chapter and chapter != "All":
        filters["chapter"] = chapter

    if len(filters) > 1:
        search_kwargs["filter"] = {"$and": [{k: v} for k, v in filters.items()]}
    elif len(filters) == 1:
        search_kwargs["filter"] = filters

    return vector_db.as_retriever(search_kwargs=search_kwargs)