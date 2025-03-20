import streamlit as st
import requests

# Streamlit Page Setup
st.set_page_config(page_title="Goldman Sachs RAG Compliance Assistant", page_icon="📜", layout="wide")
st.title("🤖 Goldman Sachs RAG-based Compliance Assistant")
st.write("Ask about compliance policies, ethical trading, and more!")

# Sidebar Details
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

# Set backend URL dynamically
BACKEND_URL = "http://backend:5000/predict"  # Works in Docker
LOCAL_BACKEND_URL = "http://localhost:5000/predict"  # Works locally

# User Input
st.subheader("💬 Ask Your Question:")
user_input = st.text_input("Type your question here...")

if st.button("Get Answer 🚀"):
    if user_input:
        try:
            response = requests.post(BACKEND_URL, json={"question": user_input}, timeout=10)
            if response.status_code != 200:
                raise Exception(f"Error {response.status_code}: {response.text}")
            st.success("✅ Answer:")
            st.write(response.json().get("answer", "No response received."))
        except Exception:
            # If backend is not available in Docker, try localhost
            try:
                response = requests.post(LOCAL_BACKEND_URL, json={"question": user_input}, timeout=10)
                if response.status_code == 200:
                    st.success("✅ Answer:")
                    st.write(response.json().get("answer", "No response received."))
                else:
                    st.error("⚠️ Backend error. Try again later.")
            except Exception:
                st.error("⚠️ Could not connect to backend.")
    else:
        st.warning("⚠️ Please enter a question!")

# Footer
st.markdown("---\n🏢 **Goldman Sachs Internal Compliance System** | Made with ❤️ & AI 🤖")
