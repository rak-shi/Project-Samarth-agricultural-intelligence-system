import streamlit as st
from query_engine import answer_question

st.title("🌾 Project Samarth — Intelligent Q&A System")
st.write("Ask questions about India's agricultural economy and climate patterns.")
question = st.text_input("Enter your question:")

if st.button("Get Answer"):
    with st.spinner("Fetching data..."):
        answer = answer_question(question)
        st.success(answer)
