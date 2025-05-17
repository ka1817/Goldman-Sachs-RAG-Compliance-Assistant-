## A Retrieval-Augmented Generation (RAG) system designed to assist with intelligent policy and compliance queries at Goldman Sachs.

---

## 📜 Problem Statement

Goldman Sachs manages an extensive collection of policy documents, including compliance guidelines, ethical codes, and governance frameworks. Manually searching through these documents is inefficient and prone to human error.

### Challenges:

* Difficulty in retrieving relevant policies promptly.
* Compliance risks due to misinterpretation or outdated information.
* Reduced operational efficiency due to manual searches.

---

## 🚀 Solution

An AI-powered Compliance Assistant that:

* ✅ Retrieves policy sections using **hybrid search (BM25 + FAISS)**
* ✅ Generates compliance-safe responses using **LLMs**
* ✅ Automates CI/CD using **GitHub Actions** to build and push Docker images to Docker Hub
* ✅ Deployed on **AWS EC2** for scalability and availability

---

## 🔧 Key Features

* **Hybrid Retrieval:** BM25 (keyword-based) + FAISS (vector search)
* **LLM Integration:** Uses **LLAMA 3-70B** for response generation
* **Re-ranking:** Enhanced accuracy using **Cross-Encoder (ms-marco-MiniLM-L-2-v2)**
* **Secure & Scalable:** Backend with **FastAPI**, frontend via **Streamlit**, containerized with **Docker**
* **Real-Time Responses:** Instant answers for compliance and governance queries

---

## 🛠️ Technologies Used

| Component     | Technology                          |
| ------------- | ----------------------------------- |
| Retrieval     | FAISS, BM25                         |
| LLM Framework | LangChain, HuggingFace, LLAMA-3-70B |
| Re-ranking    | CrossEncoder (MiniLM-L-2-v2)        |
| Backend       | FastAPI                             |
| Frontend      | Streamlit                           |
| Deployment    | Docker, Docker Compose              |
| CI/CD         | GitHub Actions + Docker Hub         |

---

## 📂 Project Structure

```
.
├── .github/workflows       # GitHub Actions workflows
├── Research                # Research documents/scripts
├── __pycache__            # Python cache
├── data                   # Compliance PDFs
├── faiss_index            # FAISS vector index
├── .dockerignore          # Docker ignore config
├── .gitignore             # Git ignore config
├── Readme.md              # Project documentation
├── app.py                 # FastAPI backend
├── backend.Dockerfile     # Backend Dockerfile
├── docker-compose.yml     # Docker Compose file
├── frontend.Dockerfile    # Frontend Dockerfile
├── main.py                # Entry point / coordinator
├── requirements.txt       # Python dependencies
```

---

## ⚙️ Deployment (Using Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/ka1817/Goldman-Sachs-RAG-Compliance-Assistant-.git
cd Goldman-Sachs-RAG-Compliance-Assistant-
```

### 2. Set Environment Variables

Create a `.env` file in the root directory:

```dotenv
GROQ_API_KEY="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"
DOCKER_USERNAME="pranavreddy123"
```

### 3. Run Docker Compose

```bash
docker-compose up -d
```

This will:

* ▶️ Start the **backend** (FastAPI) on port **5000**
* ▶️ Start the **frontend** (Streamlit) on port **8501**

---

## 🌌 Deployment on AWS EC2

### Prerequisites

* AWS EC2 Instance (Ubuntu)
* Docker and Docker Compose installed

### Steps:

1. **SSH into EC2**

```bash
ssh -i "your-key.pem" ubuntu@your-ec2-public-ip
```

2. **Clone the Repository**

```bash
git clone https://github.com/ka1817/Goldman-Sachs-RAG-Compliance-Assistant-.git
cd Goldman-Sachs-RAG-Compliance-Assistant-
```

3. **Set Environment Variables**

```bash
echo "GROQ_API_KEY=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" >> .env
echo "DOCKER_USERNAME=pranavreddy123" >> .env
```

4. **Start Services**

```bash
docker-compose up -d
```

5. **Access App**

* Backend: `http://your-ec2-public-ip:5000`
* Frontend: `http://your-ec2-public-ip:8501`

---

## 📩 Contact

**Developer:** Katta Sai Pranav Reddy
**Email:** [kattapranavreddy@gmail.com](mailto:kattapranavreddy@gmail.com)

---

## 🔗 GitHub Repository

[https://github.com/ka1817/Goldman-Sachs-RAG-Compliance-Assistant-](https://github.com/ka1817/Goldman-Sachs-RAG-Compliance-Assistant-)

