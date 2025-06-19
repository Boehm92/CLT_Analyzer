FROM nvidia/cuda:12.8.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libglib2.0-0 \
    libgl1-mesa-glx \
    python3 \
    python3-pip \
    python3-dev \
    git \
    curl \
    ca-certificates \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --upgrade pip setuptools wheel

# Install build tools for Python extensions
RUN pip install cython pybind11

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python packages and nightly PyTorch with CUDA 12.8
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install torch==2.7.0+cu128 --index-url https://download.pytorch.org/whl/cu128 && \
    pip install torch_geometric && \
    pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.7.0+cu128.html

# Copy your application code
COPY scripts/ /app/scripts/
ENV PYTHONPATH=/app/scripts

# Run main script
CMD ["python", "scripts/__main__.py"]
