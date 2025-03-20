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
from langchain.chains.question_answering import load_qa_chain
from langchain.schema import Document
from typing import List

app = FastAPI(title="Intelligent Policy & Compliance Assistant: A RAG-Based Knowledge System for Goldman Sachs")

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

data_folder = "data"  
faiss_index_path = "faiss_index"  

if not os.path.exists(data_folder):
    os.makedirs(data_folder)

if os.path.exists(faiss_index_path):
    print("✅ Loading existing FAISS index...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    faiss_index = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
    print("✅ FAISS index ready!")
else:
    print("⚠️ No FAISS index found! Rebuilding FAISS index...")

    # Load documents
    loader = DirectoryLoader(data_folder, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    # Generate embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    # Create and save FAISS index
    faiss_index = FAISS.from_documents(chunks, embeddings)
    faiss_index.save_local(faiss_index_path)

    print("✅ New FAISS index created!")

# Load documents and split into chunks 
loader = DirectoryLoader(data_folder, glob="*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# ✅ Initialize BM25 Retriever from chunks
if chunks:
    bm25_retriever = BM25Retriever.from_documents(chunks)
    print("✅ BM25 Retriever Ready!")
else:
    bm25_retriever = None
    print("⚠️ No documents found! BM25 retriever will be skipped.")

# ✅ Initialize dense retriever
retriever_dense = faiss_index.as_retriever(search_kwargs={"k": 10})

# ✅ Hybrid Retriever (Dense + BM25)
if bm25_retriever:
    hybrid_retriever = EnsembleRetriever(retrievers=[retriever_dense, bm25_retriever], weights=[0.5, 0.5])
else:
    hybrid_retriever = retriever_dense  # Use only FAISS if no BM25

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

# ✅ Load LLM
from langchain_groq import ChatGroq
llm = ChatGroq(api_key=GROQ_API_KEY, model='llama-3.3-70b-versatile')

# ✅ Define RAG Prompt
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
print("✅ RAG Support Bot PromptTemplate Ready!")

# ✅ Load QA Chain
qa_chain = load_qa_chain(llm, chain_type="stuff")

class RAGQuery(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Goldman Sachs Support Bot"}

@app.post("/predict")
def predict(query: RAGQuery):
    retrieved_docs = hybrid_retriever.get_relevant_documents(query.question)
    reranked_docs = rerank_documents(query.question, retrieved_docs)
    final_answer = qa_chain.run(input_documents=reranked_docs, question=query.question)
    return {"answer": final_answer}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5000)
