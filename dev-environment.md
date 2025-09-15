# Môi trường Phát triển

Hướng dẫn thiết lập và chạy môi trường phát triển cho dự án Ticket Management System.

## Yêu cầu

- Docker
- Docker Compose
- MongoDB (có thể sử dụng external hoặc container)
- PostgreSQL (có thể sử dụng external hoặc container)

## Cài đặt

1. Cài đặt Docker và Docker Compose:
   - [Docker](https://docs.docker.com/get-docker/)
   - [Docker Compose](https://docs.docker.com/compose/install/)

2. Cấu hình kết nối Database:
   - Sao chép file mẫu: `cp config/database.env.example config/database.env`
   - Chỉnh sửa `config/database.env` với thông tin kết nối thực tế

## Sử dụng Database Bên Ngoài (External)

Nếu bạn muốn sử dụng database có sẵn (không dùng container):

1. Cấu hình thông tin kết nối trong file `config/database.env`:
   ```
   # MongoDB Configuration
   MONGODB_URI=mongodb://your-mongodb-host:27017/your-database
   MONGODB_USER=your-username
   MONGODB_PASSWORD=your-password
   MONGODB_DATABASE=your-database
   MONGODB_AUTH_SOURCE=admin

   # PostgreSQL Configuration
   POSTGRES_URI=postgresql://your-postgres-host:5432/your-database
   POSTGRES_USER=your-username
   POSTGRES_PASSWORD=your-password
   POSTGRES_DATABASE=your-database
   ```

2. Nếu cần, bạn có thể thiết lập biến môi trường cho dev tools:
   ```bash
   export MONGODB_HOST=your-mongodb-host
   export MONGODB_PORT=27017
   export MONGODB_USER=your-username
   export MONGODB_PASSWORD=your-password
   export MONGODB_AUTH_SOURCE=admin
   ```

## Sử dụng Database trong Container

Nếu bạn muốn sử dụng database trong container:

1. Uncomment phần cấu hình MongoDB và PostgreSQL trong file `docker-compose.yml`
2. Cập nhật file `config/database.env` để kết nối với các container:
   ```
   # MongoDB Configuration
   MONGODB_URI=mongodb://mongodb:27017/ticket_system
   MONGODB_USER=admin
   MONGODB_PASSWORD=password
   MONGODB_DATABASE=ticket_system
   MONGODB_AUTH_SOURCE=admin

   # PostgreSQL Configuration
   POSTGRES_URI=postgresql://postgres:5432/users
   POSTGRES_USER=admin
   POSTGRES_PASSWORD=password
   POSTGRES_DATABASE=users
   ```

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

## Kiểm tra kết nối Database

Để kiểm tra kết nối đến các database:

```bash
python config/database.py
```

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