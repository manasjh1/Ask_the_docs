# Use lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# --- OPTIMIZATION START ---
# 1. Install CPU-only PyTorch (This saves ~2.5 GB)
# We do this BEFORE requirements.txt so pip finds it and doesn't download the big one.
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 2. Install the rest of the dependencies
# Note: If requirements.txt has 'torch', pip will see we already installed it and skip it.
RUN pip install --no-cache-dir -r requirements.txt
# --- OPTIMIZATION END ---

# Copy the rest of the application
COPY . .

# Set PYTHONPATH
ENV PYTHONPATH=/app