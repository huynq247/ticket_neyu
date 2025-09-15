# Checklist cho Ticket Service

## Thiết kế Cơ sở dữ liệu
- [x] Thiết kế schema cho collections tickets
- [x] Thiết kế schema cho comments và attachments
- [x] Thiết kế schema cho ticket history
- [x] Thiết lập indexes cho tối ưu truy vấn
- [x] Thiết lập cơ chế validation

## Phát triển API
- [x] Thiết lập project structure (FastAPI với MongoDB)
- [x] Xây dựng models và schemas
- [x] Phát triển API endpoint cho quản lý ticket (CRUD)
- [x] Phát triển API endpoint cho tìm kiếm và lọc ticket
- [x] Phát triển API endpoint cho comments
- [x] Phát triển API endpoint cho attachments
- [x] Phát triển API endpoint cho ticket history
- [x] Xây dựng logic phân công ticket tự động

## Tính năng chuyên biệt
- [x] Xây dựng cơ chế workflow cho trạng thái ticket
- [x] Xây dựng cơ chế phân loại và ưu tiên ticket
- [x] Xây dựng cơ chế gán nhãn (tagging)
- [x] Xây dựng cơ chế thời hạn và nhắc nhở
- [x] Xây dựng cơ chế đánh giá mức độ hài lòng
- [x] Xây dựng vai trò Dispatcher/Coordinator cho phân chia tickets
  - [x] Thiết kế quyền hạn đặc biệt cho vai trò này
  - [x] Xây dựng giao diện phân chia tickets
  - [x] Xây dựng cơ chế theo dõi phân phối workload

## Tích hợp
- [x] Tích hợp với User Service (để lấy thông tin người dùng)
- [x] Tích hợp với Notification Service (thông báo khi có cập nhật)
- [x] Tích hợp với File Service (đính kèm tệp)
- [x] Thiết lập event publishing khi ticket được cập nhật

## Testing
- [x] Unit tests cho models
- [x] Integration tests cho API endpoints
- [x] Performance tests với dữ liệu lớn
- [x] Test cơ chế phân công tự động

## Triển khai
- [x] Tạo Dockerfile
- [x] Cấu hình kết nối MongoDB
- [x] Thiết lập logging và monitoring
- [x] Cấu hình backup và recovery

## Documentation
- [x] API documentation
- [x] Database schema documentation
- [x] Ticket workflow documentation