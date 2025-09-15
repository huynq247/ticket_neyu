# Ticket Management System

Hệ thống quản lý ticket với kiến trúc microservices, được phát triển để tiếp nhận và quản lý các yêu cầu hỗ trợ từ người dùng.

## Kiến trúc

Dự án sử dụng kiến trúc microservices với các thành phần chính:

- **API Gateway**: Điểm vào duy nhất cho tất cả client
- **User Service**: Quản lý người dùng và xác thực (PostgreSQL)
- **Ticket Service**: Quản lý ticket và danh mục (MongoDB)
- **Notification Service**: Gửi thông báo qua email, SMS (đang phát triển)
- **File Service**: Quản lý tệp đính kèm (đang phát triển)
- **Report Service**: Tạo báo cáo và thống kê (đang phát triển)

## Cài đặt và Chạy

### Cách 1: Sử dụng môi trường ảo Python (cho phát triển cục bộ)

1. **Thiết lập môi trường ảo**:
   ```
   .\setup_venv.bat
   ```

2. **Khởi động các service**:
   ```
   .\start_with_venv.bat
   ```
   
   Hoặc sử dụng PowerShell để khởi động các service riêng biệt:
   ```powershell
   .\run_venv.ps1 user     # Khởi động User Service
   .\run_venv.ps1 ticket   # Khởi động Ticket Service
   .\run_venv.ps1 gateway  # Khởi động API Gateway
   .\run_venv.ps1 start    # Khởi động tất cả các service
   .\run_venv.ps1 stop     # Dừng tất cả các service
   ```

3. **Truy cập các service**:
   - User Service API docs: http://localhost:8000/docs
   - Ticket Service API docs: http://localhost:8001/docs
   - API Gateway: http://localhost:3000

### Cách 2: Sử dụng Docker (cho triển khai và môi trường production)

1. **Khởi động với Docker Compose**:
   ```
   .\manage.ps1 start
   ```

2. **Dừng các service**:
   ```
   .\manage.ps1 stop
   ```

3. **Xem logs**:
   ```
   .\manage.ps1 logs           # Xem logs tất cả các service
   .\manage.ps1 logs user      # Xem logs User Service
   .\manage.ps1 logs ticket    # Xem logs Ticket Service
   .\manage.ps1 logs gateway   # Xem logs API Gateway
   ```

## Chạy test tích hợp

Để kiểm tra xem các service có hoạt động đúng và tích hợp với nhau tốt không:

```
.\run_tests.bat
```
- **Ticket Service**: Quản lý tickets (MongoDB)
- **File Service**: Quản lý tệp đính kèm
- **Notification Service**: Xử lý thông báo qua email và Telegram
- **Report Service**: Báo cáo và thống kê
- **Analytics Service**: Phân tích dữ liệu nâng cao
- **Telegram Bot**: Tích hợp với Telegram để quản lý tickets

## Công nghệ

- **Backend**: Python (FastAPI/Flask)
- **Frontend**: ReactJS
- **Databases**: MongoDB (tickets), PostgreSQL (users)
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Cài đặt

Hướng dẫn cài đặt và chạy dự án sẽ được cập nhật sau.

## Tài liệu

- [Git Branching Strategy](./git-strategy.md)
- [Checklists](./checklists/README.md)
- [Kiến trúc](./architecture_diagram.md)