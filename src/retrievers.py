def get_filtered_retriever(vector_db, subject=None, chapter=None):
    """
    Retrieval with optional filtering
    """

    search_kwargs = {"k": 5}
    filters = {}

    if subject and subject != "All":
        filters["subject"] = subject

    if chapter and chapter != "All":
        filters["chapter"] = chapter

    # ✅ FIX: Chroma supports ONLY simple dict filters
    if filters:
        search_kwargs["filter"] = filters

    return vector_db.as_retriever(search_kwargs=search_kwargs)