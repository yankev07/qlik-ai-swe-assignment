FROM python:3.10-slim

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip


RUN pip install --no-cache-dir torch==2.2.2 \
    openai==0.28.0 \
    pydantic==2.9.2 \
    python-dotenv==1.0.1 \
    transformers==4.45.2 \
    flask-cors==5.0.0 \
    numpy==1.24.4 \
    "fastapi[all]"

RUN pip install pytest pytest-cov

COPY . .

EXPOSE 8000
ENV PORT 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
