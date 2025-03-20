## Intelligent Policy & Compliance Assistant: A RAG-Based Knowledge System for Goldman Sachs 

📜 Goldman Sachs RAG-Based Compliance Assistant
A Retrieval-Augmented Generation (RAG) system for intelligent policy and compliance assistance at Goldman Sachs.

🔹 Problem Statement
Goldman Sachs manages extensive policy documents, including compliance guidelines, ethical codes, and governance frameworks. Manually searching these documents is time-consuming and inefficient.

Challenge:

Employees struggle to quickly retrieve relevant policies.
Compliance risks arise due to misinterpretation or outdated information.
Manual search methods reduce operational efficiency.

Solution:
We built a RAG-based AI assistant that:
✅ Retrieves relevant policy sections using advanced search (BM25 + FAISS).
✅ Generates accurate, compliance-friendly responses using LLMs.
✅ Ensures transparency by citing source documents.

🚀 Key Features

Hybrid Retrieval: Combines FAISS (dense embeddings) and BM25 (keyword-based) for optimal document search.
LLM Integration: Uses LLAMA 3-70B for response generation.
Reranking: Implements Cross-Encoder re-ranking for improved accuracy.
Secure & Scalable: Deployed via FastAPI + Docker + Streamlit UI.
Real-Time Querying: Instant responses for compliance and governance questions.



🛠️ Technologies Used
Retrieval System: FAISS (vector search), BM25 (keyword retrieval)
LLM Processing: LangChain + Hugging Face + LLAMA-3-70B
Reranking: CrossEncoder (ms-marco-MiniLM-L-2-v2)
Backend: FastAPI
Frontend: Streamlit
Deployment: Docker + Compose


💡 How It Works?
1️⃣ User enters a question (e.g., "What is Goldman Sachs’ policy on conflicts of interest?").
2️⃣ System retrieves relevant document sections from compliance PDFs using FAISS + BM25.
3️⃣ Documents are re-ranked using a Cross-Encoder model.
4️⃣ LLM generates an answer based only on retrieved context.
5️⃣ User receives a clear, source-backed response.

📖 Supported Queries

✅ Compliance & Ethics – Insider trading, bribery, conflict of interest.
✅ Corporate Governance – Proxy voting, board responsibilities.
✅ Political Policies – Lobbying, campaign contributions.
✅ Employee Conduct – Workplace ethics, reporting violations.


🔐 Security & Compliance

✅ No Hallucinations: AI only generates responses from retrieved document excerpts.
✅ Source Citations: Every response includes references to official Goldman Sachs policies.
✅ Data Privacy: The system does not store user queries or responses.



⚙️ Deployment Using Docker (Recommended)
You can quickly set up the application using pre-built Docker images.

1️⃣ Clone the Repository

Copy code
git clone https://github.com/ka1817/Goldman-Sachs-RAG-Compliance-Assistant-.git
cd Goldman-Sachs-RAG-Compliance-Assistant-

2️⃣ Set Environment Variables
Create a .env file in the root directory and add the following:

Copy code
GROQ_API_KEY="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"
DOCKER_USERNAME="pranavreddy123"

3️⃣ Run Docker Compose

Copy code
docker-compose up -d
This will:
✅ Start the backend (FastAPI) on port 5000
✅ Start the frontend (Streamlit UI) on port 8501


📩 Contact 
👨‍💻 Developer: Katta Sai Pranav Reddy | kattapranavreddy@gmail.com