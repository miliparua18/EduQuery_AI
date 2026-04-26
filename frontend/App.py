import streamlit as st
import requests
import pandas as pd

st.title("🎓 EduQuery AI: Student Tutor")

subject = st.sidebar.selectbox("Course Filter", ["All", "DBMS", "Data Structures", "Machine Learning"])
user_query = st.chat_input("Ask a question...")

if user_query:
    st.chat_message("user").write(user_query)
    params = {"query": user_query, "subject": subject}
    res = requests.get("http://localhost:8000/ask", params=params).json()
    
    if "answer" in res:
        st.chat_message("assistant").write(res["answer"])
        with st.expander("📊 Citation Panel"):
            st.table(pd.DataFrame(res["citations"]))