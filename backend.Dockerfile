# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt requirements.txt
COPY main.py main.py
COPY data/ data/
COPY faiss_index/ faiss_index/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 5000

# Run FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
