# def get_filtered_retriever(vector_db, subject=None, chapter=None):
#     filters = {}

#     if subject and subject != "All":
#         filters["subject"] = subject

#     if chapter and chapter != "All":
#         filters["chapter"] = chapter

#     return vector_db.as_retriever(
#         search_kwargs={
#             "k": 5,
#             "filter": filters if filters else None
#         }
#     )



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