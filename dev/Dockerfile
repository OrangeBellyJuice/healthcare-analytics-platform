FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash"]
