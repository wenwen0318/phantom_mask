# Dockerfile
FROM python:3.10-slim

# 環境變數
ARG ENV=production
ENV ENV $ENV

# 設定工作目錄
WORKDIR /app

# 複製檔案
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
