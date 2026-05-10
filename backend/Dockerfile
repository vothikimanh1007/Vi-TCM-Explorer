# Dockerfile for Hugging Face Spaces
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies required for giotto-tda C++ compilation
RUN apt-get update && apt-get install -y build-essential gcc g++ && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Hugging Face Spaces routes port 7860
EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
