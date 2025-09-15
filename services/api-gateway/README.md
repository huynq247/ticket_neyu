# API Gateway

Service này đóng vai trò là cổng vào duy nhất cho tất cả các client, chịu trách nhiệm định tuyến các yêu cầu đến các microservices tương ứng.

## Chức năng chính

- Định tuyến các yêu cầu đến các microservices phù hợp
- Xử lý xác thực và phân quyền
- Cân bằng tải
- Giám sát và logging
- Rate limiting và throttling

## Công nghệ

- Node.js
- Express
- http-proxy-middleware
- JWT Authentication

## Cài đặt và Chạy

### Cài đặt dependencies

```bash
npm install
```

### Thiết lập biến môi trường

Sao chép file `.env.example` thành `.env` và chỉnh sửa các giá trị:

```bash
cp .env.example .env
```

### Chạy ứng dụng

Chạy trong môi trường development:

```bash
npm run dev
```

Chạy trong môi trường production:

```bash
npm start
```

## Cấu hình Routing

API Gateway sẽ định tuyến các yêu cầu đến các microservices dựa trên URL paths:

- `/api/auth/*` -> User Service (không yêu cầu xác thực)
- `/api/user/*` -> User Service
- `/api/ticket/*` -> Ticket Service
- `/api/file/*` -> File Service
- `/api/notification/*` -> Notification Service

## Kiểm tra trạng thái

API Gateway cung cấp endpoint để kiểm tra trạng thái của các services:

```
GET /api/status
```

## Bảo mật

API Gateway xử lý xác thực thông qua JWT (JSON Web Tokens) để bảo vệ các endpoints.