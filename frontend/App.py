import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="EduQuery AI", layout="wide")
st.title("🎓 EduQuery AI: Student Textbook Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.header("Settings")
subject = st.sidebar.selectbox("Filter Subject", ["All", "DBMS", "DSA", "ML"])

if st.sidebar.button("Clear History"):
    st.session_state.messages = []
    st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "citations" in message:
            with st.expander("📊 Source Citations (Auto-Detected)"):
                st.dataframe(pd.DataFrame(message["citations"]), width="stretch", hide_index=True)

user_query = st.chat_input("Ask about a concept...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)
    
    with st.spinner("Analyzing textbooks..."):
        params = {"query": user_query, "subject": subject}
        try:
            response = requests.get("http://127.0.0.1:8000/ask", params=params).json()
            
            if "answer" in response:
                answer = response["answer"]
                citations = response["citations"]
                
                with st.chat_message("assistant"):
                    st.write(answer)
                    if citations:
                        with st.expander("📊 Source Citations (Auto-Detected)"):
                            st.dataframe(pd.DataFrame(citations), width="stretch", hide_index=True)
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer, 
                    "citations": citations
                })
        except Exception as e:
            st.error(f"Error: {e}")