# SLM Hosting Service - Challenge 1

## 📌 Giới thiệu
Dự án triển khai một hệ thống API Wrapper cho Small Language Model (SLM), tích hợp khả năng phân loại ý định (Intent Mapping) và giám sát hiệu năng (Latency Logging). Hệ thống được đóng gói bằng Docker và bảo vệ bởi tầng Proxy Nginx.

## 🏗 Kiến trúc hệ thống (Flow Data)
Hệ thống tuân thủ mô hình 3 lớp (3-tier architecture):
1. **Client**: Gửi request qua cổng 80.
2. **Nginx (Proxy)**: Tiếp nhận request, thực hiện **Rate Limit (10r/s)** để chống spam, sau đó điều hướng tới API Wrapper.
3. **API Wrapper (FastAPI)**: 
   - Tiếp nhận câu hỏi tiếng Việt.
   - Phân loại Intent (Cảm xúc/Hành động).
   - Gọi Model Server qua giao thức OpenAI Compatible.
   - Ghi log Latency và Intent định dạng Structured Log.
4. **Model Server (Ollama/vLLM)**: Thực hiện suy luận (Inference) bằng model Qwen2.5-1.5B.

## 🚀 Tính năng nổi bật
- **Intent Mapping**: Tự động nhận diện ý định người dùng (Vui vẻ, thắc mắc, yêu cầu...).
- **Performance Monitoring**: Log chi tiết thời gian xử lý của từng request.
- **Infrastructure as Code**: Triển khai toàn bộ qua Docker Compose.
- **Rate Limiting**: Bảo vệ tài nguyên GPU/CPU ở tầng Gateway.

## 🛠 Công nghệ sử dụng
- **Backend**: Python 3.10, FastAPI.
- **AI/LLM**: Ollama, vLLM (Qwen2.5-1.5B).
- **Hạ tầng**: Nginx, Docker, Docker Compose.