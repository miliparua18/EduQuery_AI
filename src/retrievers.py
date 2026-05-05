def get_filtered_retriever(vector_db, subject, chapter):
    filters = {}

    if subject and subject.lower() != "all":
        filters["subject"] = subject

    if chapter:
        filters["chapter"] = chapter

    if filters:
        return vector_db.as_retriever(
            search_kwargs={
                "k": 5,
                "filter": filters
            }
        )
    else:
        return vector_db.as_retriever(
            search_kwargs={
                "k": 5
            }
        )





# from langchain_classic.retrievers.multi_query import MultiQueryRetriever
# # from src.model import get_gemini_model



# # llm = get_gemini_model()

# def get_filtered_retriever(vector_db, subject, chapter, llm=None):
#     filters = {}

#     if subject:
#         filters["subject"] = subject

#     if chapter:
#         filters["chapter"] = chapter

#     # 🔹 Build search kwargs safely
#     search_kwargs = {"k": 5}
#     if filters:
#         search_kwargs["filter"] = filters

#     # 🔹 Create base retriever FIRST
#     base_retriever = vector_db.as_retriever(
#         search_type="mmr",   # or "similarity"
#         search_kwargs=search_kwargs
#     )

        

#     return base_retriever
    
       