# Sử dụng Python slim để image nhẹ, build nhanh
FROM python:3.10-slim

WORKDIR /app

# Copy requirement và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ thư mục app
COPY app/ ./app/

EXPOSE 8000

# Lệnh khởi chạy server (Lưu ý đường dẫn module chuẩn app.main:app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]