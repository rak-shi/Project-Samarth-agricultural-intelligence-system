import streamlit as st
from query_engine import answer_question
st.sidebar.title("About Project Samarth")
st.sidebar.markdown(
    """
    **A Smart Q&A System over Indian Government Open Data**

    - 💡 **Purpose:** Bridge the gap between diverse government datasets and actionable, traceable insights.
    - 🔗 **Live Data:** All answers are fetched live from [data.gov.in](https://data.gov.in) official APIs.
    - 🧠 **How it works:** Enter questions in natural language – your answer is computed in real-time and always cites the original source (dataset name + resource ID).
    - 🏛️ **Key Data Sources:**
        - Crop statistics: Ministry of Agriculture & Farmers Welfare
        - Rainfall stats: India Meteorological Department (IMD) & Jal Shakti
    - 🔒 **Data Sovereignty:** Runs locally and never shares your queries or results with third parties.
    - 🏷️ **Traceability:** Every output includes a government dataset citation for policy or research needs.
    
    ---
    _Built for rapid, robust, and secure insight extraction for policymakers and researchers._
    """
)


st.title("🌾 Project Samarth — Intelligent Q&A System")
st.write("Ask complex questions about India's agricultural economy and climate patterns. (Source: data.gov.in)")

question = st.text_input("Enter your question:")

if st.button("Get Answer"):
    with st.spinner("Fetching real-time data..."):
        answer = answer_question(question)
        st.success(answer)
