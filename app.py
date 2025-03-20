import streamlit as st
import requests
import time

st.set_page_config(page_title="Goldman Sachs RAG Compliance Assistant", page_icon="📜", layout="wide")
st.title("🤖 Goldman Sachs RAG-based Compliance Assistant")
st.write("Ask about compliance policies, ethical trading, and more!")

st.sidebar.title("📌 Project Details")
st.sidebar.markdown(
    """
    **🔹 Project:** Intelligent Policy & Compliance Assistant  
    **🔹 Technology:** FastAPI, FAISS, BM25, LangChain, Hugging Face  
    **🔹 Features:**  
    - Hybrid Retrieval (FAISS + BM25)  
    - Reranking for Accuracy ✅  
    - Fast Responses ⚡  
    - Ethical Trading Insights 📈  
    - Secure & Reliable 🔒  
    """
)

# ✅ Backend URL (Docker)
BACKEND_URL = "http://backend:5000/predict"

st.subheader("💬 Ask Your Question:")
user_input = st.text_input("Type your question here...")

if st.button("Get Answer 🚀"):
    if user_input:
        try:
            response = requests.post(BACKEND_URL, json={"question": user_input}, timeout=10)
            if response.status_code == 200:
                st.success("✅ Answer:")
                st.write(response.json().get("answer", "No response received."))
            else:
                st.error(f"⚠️ Backend Error ({response.status_code}): {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Could not connect to the backend. Please check if the backend service is running.")
        except requests.exceptions.Timeout:
            st.error("⚠️ Connection to the backend timed out.")
    else:
        st.warning("⚠️ Please enter a question!")

# Footer
st.markdown("---\n🏢 **Goldman Sachs Internal Compliance System** | Made with ❤️ & AI 🤖")
