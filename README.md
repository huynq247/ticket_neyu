# Ticket Management System

Hệ thống quản lý ticket với kiến trúc microservices, được phát triển để tiếp nhận và quản lý các yêu cầu hỗ trợ từ người dùng.

## Kiến trúc

Dự án sử dụng kiến trúc microservices với các thành phần chính:

- **API Gateway**: Điểm vào duy nhất cho tất cả client
- **User Service**: Quản lý người dùng và xác thực (PostgreSQL)
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