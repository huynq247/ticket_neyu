# File Service API Endpoints

Dựa trên checklist của File Service, dưới đây là danh sách các API endpoint cần thiết và trạng thái hiện tại của chúng.

## Quản lý File (CRUD)

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/files` | GET | Lấy danh sách file với phân trang và lọc | Đã triển khai |
| `/api/v1/files/{file_id}` | GET | Lấy thông tin metadata của file | Đã triển khai |
| `/api/v1/files/{file_id}/content` | GET | Tải xuống nội dung file | Đã triển khai |
| `/api/v1/files` | POST | Upload file mới | Đã triển khai |
| `/api/v1/files/{file_id}` | PUT | Cập nhật metadata file | Đã triển khai |
| `/api/v1/files/{file_id}` | DELETE | Xóa file | Đã triển khai |

## Tìm kiếm và Lọc File

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/files/search` | GET | Tìm kiếm file theo tên, mô tả, tags | Đã triển khai |
| `/api/v1/files/by-owner/{user_id}` | GET | Lấy danh sách file của một người dùng cụ thể | Đã triển khai |
| `/api/v1/files/by-type/{file_type}` | GET | Lọc file theo loại | Đã triển khai |

## Phân quyền và Chia sẻ

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/files/{file_id}/permissions` | GET | Lấy thông tin phân quyền của file | Đã triển khai |
| `/api/v1/files/{file_id}/permissions` | POST | Thêm quyền truy cập cho người dùng/nhóm | Đã triển khai |
| `/api/v1/files/{file_id}/permissions/{permission_id}` | DELETE | Xóa quyền truy cập | Đã triển khai |
| `/api/v1/files/{file_id}/share` | POST | Tạo link chia sẻ file | Đã triển khai |
| `/api/v1/files/shared-with-me` | GET | Lấy danh sách file được chia sẻ với người dùng | Đã triển khai |

## Tích hợp với Ticket

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/files/by-ticket/{ticket_id}` | GET | Lấy danh sách file đính kèm với ticket | Đã triển khai |
| `/api/v1/files/attach-to-ticket` | POST | Đính kèm file với ticket | Đã triển khai |
| `/api/v1/files/detach-from-ticket/{ticket_id}/{file_id}` | DELETE | Gỡ bỏ file khỏi ticket | Đã triển khai |

## Tính năng Nâng cao

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/files/{file_id}/thumbnail` | GET | Lấy thumbnail của file | Cần triển khai |
| `/api/v1/files/multipart/initiate` | POST | Khởi tạo multipart upload | Cần triển khai |
| `/api/v1/files/multipart/upload-part` | PUT | Upload một phần của file | Cần triển khai |
| `/api/v1/files/multipart/complete` | POST | Hoàn thành multipart upload | Cần triển khai |
| `/api/v1/files/{file_id}/versions` | GET | Lấy danh sách các phiên bản của file | Cần triển khai |

## Quản lý Hệ thống

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/storage/usage` | GET | Lấy thông tin sử dụng bộ nhớ | Đã triển khai |
| `/api/v1/storage/quota` | GET | Lấy thông tin quota cho người dùng | Đã triển khai |
| `/api/v1/storage/backends` | GET | Lấy thông tin về các storage backend | Đã triển khai |
| `/api/v1/files/cleanup` | POST | Dọn dẹp các file tạm | Đã triển khai |

## Tích hợp và Hệ thống

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/` | GET | Health check | Đã triển khai |
| `/db-check` | GET | Kiểm tra kết nối database | Đã triển khai |
| `/storage-check` | GET | Kiểm tra kết nối storage backend | Đã triển khai |
| `/docs` | GET | Swagger API documentation | Đã triển khai |
| `/redoc` | GET | ReDoc API documentation | Đã triển khai |

## Ghi chú

- Các endpoint có trạng thái "Đã triển khai" đã được xác nhận hoạt động trong checklist.
- Các endpoint có trạng thái "Cần triển khai" cần được phát triển dựa trên checklist.
- Tất cả các API endpoint đều yêu cầu xác thực JWT trừ endpoint health check.
- Đối với các endpoint liên quan đến phân quyền và chia sẻ, có thể yêu cầu quyền owner hoặc admin.
- Service này có cơ chế fallback để lưu trữ file trên filesystem local khi không thể kết nối tới MongoDB.
- Các tính năng nâng cao như multipart upload và version control đang trong kế hoạch phát triển.