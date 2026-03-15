# 📚 RUNBOOK: Hệ thống SLM Hosting (vLLM/Ollama + FastAPI + Nginx)

Tài liệu này ghi chú lại quá trình triển khai, vận hành hệ thống SLM (Small Language Model) trên môi trường Production thu nhỏ, đồng thời làm rõ cách dự án này đã vượt qua các sai lầm phổ biến khi deploy AI model.

---

## 🛡️ 1. BẢNG TỔNG HỢP: KHẮC PHỤC SAI LẦM PHỔ BIẾN

Trong quá trình triển khai, dự án đã chủ động áp dụng các Best Practices để tránh 8 sai lầm thường gặp khi host LLM/SLM.

| Lỗi | Mô tả rủi ro | Giải pháp đã áp dụng trong dự án | Trạng thái |
| :--- | :--- | :--- | :---: |
| **#1** | Download model thẳng trong Dockerfile | Đã cấu hình `volumes: ollama_data` và sử dụng lệnh `ollama pull` lúc khởi động container (entrypoint) thay vì tải lúc build image. Model được lưu ở host, không tải lại nhiều lần. | ✅ |
| **#2** | Expose port model thẳng ra ngoài | Port `11434` của Ollama chỉ dùng nội bộ. Traffic từ ngoài bắt buộc phải đi qua Nginx (Port 80) -> API Wrapper (Port 8000) -> Ollama. Đã thiết lập Nginx Rate Limit (10r/s) để chặn spam. | ✅ |
| **#3** | Không set `--max-model-len` | Do sử dụng CPU/Ollama thay vì vLLM, Ollama tự động quản lý Context Length (hiện đang chạy với `default_num_ctx=4096`). | ✅ |
| **#4** | Không dùng Quantization | Hệ thống sử dụng model `qwen2.5:1.5b` (mặc định đã được lượng tử hóa 4-bit) thông qua Ollama, giúp model siêu nhẹ, chạy mượt trên CPU. | ✅ |
| **#5** | Healthcheck vô dụng | Đã cấu hình lệnh `healthcheck` (`ollama list`) trong `docker-compose.yml`. Nginx và API chỉ được khởi động (`depends_on: service_healthy`) khi model đã sẵn sàng phục vụ. | ✅ |
| **#6** | Sync endpoint làm chết API | API Wrapper sử dụng `async def` và `httpx.AsyncClient`. Quá trình gọi model hoàn toàn là non-blocking (không khóa luồng), giúp FastAPI xử lý hàng trăm request cùng lúc mà không bị treo. | ✅ |
| **#7** | Không giới hạn VRAM (GPU) | Dự án chạy trên CPU thông qua Ollama nên không bị dính lỗi tràn VRAM (90%) mặc định của vLLM. | ✅ |
| **#8** | Không timeout & max_tokens | Đã thiết lập `timeout=30.0` trong `httpx.AsyncClient` và truyền `"max_tokens": 10` vào payload gửi xuống model để ép model dừng sinh chữ sớm, tránh nghẽn hàng đợi. | ✅ |

---

## 📸 2. MINH CHỨNG THỰC TẾ (PROOF)

Dưới đây là các hình ảnh chứng minh hệ thống hoạt động ổn định và các cơ chế bảo vệ đã được kích hoạt.

### 2.1. Request Thành Công (Happy Path)
Hệ thống xử lý phân loại cảm xúc (Intent) thông qua API Wrapper. Model nhận diện chính xác và trả về hành động tương ứng.

*Lệnh test:*
```bash
curl -X POST http://localhost/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{"message": "hôm nay tôi được điểm 10"}'