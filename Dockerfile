FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libfreetype6-dev \
    libjpeg-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libraqm-dev \
    zlib1g-dev \
    pkg-config \
    curl \
    cron \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /server

COPY ./server/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./server /server

# Make entrypoint.sh executable
RUN chmod +x /server/entrypoint.sh

# Convert scripts to Unix format just in case
RUN dos2unix /server/*.sh