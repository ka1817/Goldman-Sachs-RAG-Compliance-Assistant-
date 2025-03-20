# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY requirements.txt .
COPY main.py .
COPY faiss_index/ faiss_index/
COPY data/ data/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure faiss_index directory exists
RUN mkdir -p /app/faiss_index

# Expose API port
EXPOSE 5000

# Run FastAPI server after ensuring FAISS index is built
CMD ["sh", "-c", "python3 main.py && uvicorn main:app --host 0.0.0.0 --port 5000"]
