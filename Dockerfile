FROM python:3.9-slim

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 創建並複製靜態文件
COPY static/ /app/static/
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 