# Build stage
FROM python:3.9-slim AS builder

WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết cho TensorFlow và Pillow
RUN apt-get update && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 && rm -rf /var/lib/apt/lists/*

# Chỉ copy requirements để tận dụng cache layer
COPY requirements.txt .

# Cài đặt các dependencies cần thiết
RUN pip install --no-cache-dir numpy==1.23.5 && \
    pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.9-slim

WORKDIR /app

# Copy các dependencies và executable scripts từ builder
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy các file cần thiết
COPY main.py .
COPY model/ model/

# Tạo thư mục static và copy index.html vào đó
RUN mkdir -p static
COPY static/index.html static/

# Set permissions
RUN chmod -R 755 /app

EXPOSE 8000

# Chỉ định worker process
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000", "--workers", "4"]