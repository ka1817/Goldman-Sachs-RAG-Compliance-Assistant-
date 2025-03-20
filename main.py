from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from sentence_transformers import CrossEncoder
from langchain.chains import RetrievalQA
from langchain.schema import Document
from typing import List

app = FastAPI(title="Intelligent Policy & Compliance Assistant")

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Define paths
data_folder = "data"
faiss_index_folder = "faiss_index"
faiss_index_path = os.path.join(faiss_index_folder, "index.faiss")

# Ensure necessary directories exist
os.makedirs(data_folder, exist_ok=True)
os.makedirs(faiss_index_folder, exist_ok=True)

# Load embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Load or create FAISS index
if os.path.exists(faiss_index_path):
    print("✅ Loading existing FAISS index...")
    faiss_index = FAISS.load_local(faiss_index_folder, embeddings, allow_dangerous_deserialization=True)
else:
    print("⚠️ No FAISS index found! Rebuilding FAISS index...")

    # Load documents
    loader = DirectoryLoader(data_folder, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    if documents:
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        # Create and save FAISS index
        faiss_index = FAISS.from_documents(chunks, embeddings)
        faiss_index.save_local(faiss_index_folder)

        print("✅ New FAISS index created!")
    else:
        print("⚠️ No documents found. FAISS index not created!")

# Load documents and split into chunks 
loader = DirectoryLoader(data_folder, glob="*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# ✅ Initialize BM25 Retriever from chunks
bm25_retriever = BM25Retriever.from_documents(chunks) if chunks else None

# ✅ Initialize dense retriever
retriever_dense = faiss_index.as_retriever(search_kwargs={"k": 10})

# ✅ Hybrid Retriever (Dense + BM25)
hybrid_retriever = EnsembleRetriever(retrievers=[retriever_dense, bm25_retriever], weights=[0.5, 0.5]) if bm25_retriever else retriever_dense

# ✅ Initialize reranker model
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-2-v2")

def rerank_documents(query: str, retrieved_docs: List[Document]) -> List[Document]:
    """Re-rank retrieved documents using a Cross-Encoder."""
    if not retrieved_docs:
        return []

    docs_texts = [doc.page_content for doc in retrieved_docs]
    scores = reranker.predict([(query, doc) for doc in docs_texts])
    sorted_docs = [doc for _, doc in sorted(zip(scores, retrieved_docs), key=lambda x: x[0], reverse=True)]
    return sorted_docs

# Load LLM
from langchain_groq import ChatGroq
llm = ChatGroq(api_key=GROQ_API_KEY, model='llama-3.3-70b-versatile')

rag_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful AI support assistant for Goldman Sachs, providing accurate and reliable information 
    based only on the retrieved document excerpts below. Always ensure compliance, transparency, and professionalism. 
    Do not make up answers. If the answer is not found in the provided context, state that clearly.

    ---
    Context:
    {context}
    ---

    User Query: {question}

    Guidelines:
    1. Use only the context provided. Do NOT generate unsupported information.
    2. Be concise and professional in your response.
    3. If the answer is unclear or unavailable in the context, respond with:
       "I'm sorry, but I couldn't find relevant information in the retrieved documents."
    4. Maintain a neutral and compliant tone, as this is an official support system.

    Answer:
    """
)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=hybrid_retriever, chain_type="stuff", return_source_documents=True)

class RAGQuery(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Goldman Sachs Support Bot"}

@app.post("/predict")
def predict(query: RAGQuery):
    retrieved_docs = hybrid_retriever.invoke(query.question)
    reranked_docs = rerank_documents(query.question, retrieved_docs)
    result = qa_chain.invoke({"query": query.question, "context": reranked_docs})
    return {"answer": result['result']}

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=5000)
