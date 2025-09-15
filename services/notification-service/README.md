# Notification Service

Microservice cho việc gửi và quản lý thông báo trong hệ thống Ticket Management.

## Tính năng

- Gửi thông báo qua nhiều kênh (Email, Telegram)
- Quản lý templates thông báo
- Lập lịch gửi thông báo
- Theo dõi trạng thái gửi thông báo
- Xử lý hàng đợi thông báo với Celery và Redis

## Cài đặt

### Sử dụng Docker

```bash
docker build -t notification-service .
docker run -d -p 8003:8003 --name notification-service notification-service
```

### Sử dụng Local Environment

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

### Khởi động Celery Worker

```bash
celery -A app.core.celery_app worker --loglevel=info
```

## API Endpoints

- `POST /api/v1/notifications`: Gửi thông báo
- `GET /api/v1/notifications/{notification_id}`: Kiểm tra trạng thái thông báo
- `GET /api/v1/notifications/templates`: Danh sách templates
- `POST /api/v1/notifications/templates`: Tạo template mới

## Kết nối với services khác

Notification Service tích hợp với:
- User Service: Lấy thông tin liên hệ người dùng
- Ticket Service: Nhận sự kiện cập nhật ticket