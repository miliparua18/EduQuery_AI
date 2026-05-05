import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="EduQuery AI", layout="wide")
st.title("🎓 EduQuery AI: Student Textbook Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

subject_map = {
    "All": None,
    "ML": "Machine Learning",
    "DSA": "Data Structures",
    "DBMS": "DBMS"
}

subject = st.sidebar.selectbox("Filter Subject", ["All", "DBMS", "DSA", "ML"])
mapped_subject = subject_map.get(subject, subject)

if st.sidebar.button("Clear History"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if "citations" in message and message["citations"]:
            with st.expander("📊 Source Citations"):
                st.dataframe(pd.DataFrame(message["citations"]), width="stretch")

user_query = st.chat_input("Ask Questions...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("user"):
        st.write(user_query)

    with st.spinner("Analyzing textbooks..."):
        params = {
            "query": user_query,
            "subject": mapped_subject
        }

        response = requests.get("http://127.0.0.1:8000/ask", params=params).json()

        answer = response.get("answer", "No answer found.")
        citations = response.get("citations", [])

        with st.chat_message("assistant"):
            st.write(answer)

            if citations:
                with st.expander("📊 Source Citations"):
                    st.dataframe(pd.DataFrame(citations), width="stretch")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "citations": citations
        })