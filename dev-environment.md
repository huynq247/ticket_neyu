# Môi trường Phát triển

Hướng dẫn thiết lập và chạy môi trường phát triển cho dự án Ticket Management System.

## Yêu cầu

- Docker
- Docker Compose

## Cài đặt

1. Cài đặt Docker và Docker Compose:
   - [Docker](https://docs.docker.com/get-docker/)
   - [Docker Compose](https://docs.docker.com/compose/install/)

## Chạy môi trường phát triển

1. Khởi động các dịch vụ cơ bản:

```bash
docker-compose up -d
```

2. Khởi động các công cụ phát triển:

```bash
docker-compose -f docker-compose.dev.yml up -d
```

## Truy cập các công cụ

- **MongoDB UI (Mongo Express)**: http://localhost:8081
- **PostgreSQL UI (pgAdmin)**: http://localhost:8082
  - Email: admin@example.com
  - Password: password
- **Redis UI (Redis Commander)**: http://localhost:8083

## Dừng môi trường

1. Dừng các công cụ phát triển:

```bash
docker-compose -f docker-compose.dev.yml down
```

2. Dừng các dịch vụ cơ bản:

```bash
docker-compose down
```

## Xóa dữ liệu

Để xóa hoàn toàn dữ liệu và khởi động lại:

```bash
docker-compose down -v
```

**Lưu ý**: Lệnh này sẽ xóa tất cả volumes và dữ liệu trong các containers.