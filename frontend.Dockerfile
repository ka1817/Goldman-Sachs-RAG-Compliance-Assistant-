# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy only requirements first for faster caching
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the Streamlit default port
EXPOSE 8501

# Run Streamlit app with CORS & XSRF fixes
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
