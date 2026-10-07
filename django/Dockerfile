FROM python:3.12-slim

# Dependances de compilation pour mysqlclient (extension C)
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc pkg-config default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
