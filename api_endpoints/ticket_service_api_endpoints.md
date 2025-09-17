# Ticket Service API Endpoints

Dựa trên checklist của Ticket Service, dưới đây là danh sách các API endpoint cần thiết và trạng thái hiện tại của chúng.

## Quản lý Ticket (CRUD)

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/tickets` | GET | Lấy danh sách ticket với phân trang và lọc | Đã triển khai |
| `/api/v1/tickets/{ticket_id}` | GET | Lấy thông tin chi tiết của một ticket | Đã triển khai |
| `/api/v1/tickets` | POST | Tạo ticket mới | Đã triển khai |
| `/api/v1/tickets/{ticket_id}` | PUT | Cập nhật thông tin ticket | Đã triển khai |
| `/api/v1/tickets/{ticket_id}` | DELETE | Xóa ticket | Đã triển khai |

## Tìm kiếm và Lọc Ticket

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/tickets/search` | GET | Tìm kiếm ticket theo từ khóa | Đã triển khai |
| `/api/v1/tickets/filter` | GET | Lọc ticket theo nhiều tiêu chí | Đã triển khai |
| `/api/v1/tickets/my-tickets` | GET | Lấy danh sách ticket của người dùng hiện tại | Đã triển khai |
| `/api/v1/tickets/assigned` | GET | Lấy danh sách ticket được gán cho người dùng hiện tại | Đã triển khai |
| `/api/v1/tickets/by-status/{status}` | GET | Lấy danh sách ticket theo trạng thái | Đã triển khai |
| `/api/v1/tickets/by-priority/{priority}` | GET | Lấy danh sách ticket theo mức độ ưu tiên | Đã triển khai |
| `/api/v1/tickets/by-department/{department_id}` | GET | Lấy danh sách ticket theo phòng ban | Đã triển khai |

## Quản lý Comment

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/tickets/{ticket_id}/comments` | GET | Lấy danh sách comments của một ticket | Đã triển khai |
| `/api/v1/tickets/{ticket_id}/comments` | POST | Thêm comment mới vào ticket | Đã triển khai |
| `/api/v1/tickets/{ticket_id}/comments/{comment_id}` | PUT | Cập nhật comment | Đã triển khai |
| `/api/v1/tickets/{ticket_id}/comments/{comment_id}` | DELETE | Xóa comment | Đã triển khai |

## Quản lý Attachment

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/tickets/{ticket_id}/attachments` | GET | Lấy danh sách attachments của một ticket | Đã triển khai |
| `/api/v1/tickets/{ticket_id}/attachments` | POST | Thêm attachment mới vào ticket | Đã triển khai |
| `/api/v1/tickets/{ticket_id}/attachments/{attachment_id}` | GET | Tải xuống attachment | Đã triển khai |
| `/api/v1/tickets/{ticket_id}/attachments/{attachment_id}` | DELETE | Xóa attachment | Đã triển khai |

## Ticket History

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/tickets/{ticket_id}/history` | GET | Lấy lịch sử thay đổi của ticket | Đã triển khai |

## Workflow và Trạng thái

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/tickets/{ticket_id}/status` | PUT | Cập nhật trạng thái ticket | Đã triển khai |
| `/api/v1/tickets/{ticket_id}/assign` | PUT | Gán ticket cho người xử lý | Đã triển khai |
| `/api/v1/tickets/{ticket_id}/priority` | PUT | Cập nhật mức độ ưu tiên | Đã triển khai |
| `/api/v1/tickets/{ticket_id}/tags` | PUT | Cập nhật nhãn cho ticket | Đã triển khai |
| `/api/v1/tickets/{ticket_id}/deadline` | PUT | Cập nhật thời hạn ticket | Đã triển khai |
| `/api/v1/tickets/{ticket_id}/satisfaction` | POST | Đánh giá mức độ hài lòng | Đã triển khai |

## Dispatcher/Coordinator

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/dispatcher/tickets` | GET | Lấy danh sách ticket cần phân công | Đã triển khai |
| `/api/v1/dispatcher/assign` | POST | Phân công ticket cho nhân viên | Đã triển khai |
| `/api/v1/dispatcher/workload` | GET | Xem tình trạng phân phối công việc | Đã triển khai |
| `/api/v1/dispatcher/departments/{department_id}/tickets` | GET | Xem ticket của phòng ban | Đã triển khai |

## Báo cáo và Thống kê

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/tickets/stats/by-status` | GET | Thống kê ticket theo trạng thái | Đã triển khai |
| `/api/v1/tickets/stats/by-priority` | GET | Thống kê ticket theo mức độ ưu tiên | Đã triển khai |
| `/api/v1/tickets/stats/by-department` | GET | Thống kê ticket theo phòng ban | Đã triển khai |
| `/api/v1/tickets/stats/resolution-time` | GET | Thống kê thời gian giải quyết ticket | Đã triển khai |

## Tích hợp và Hệ thống

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/` | GET | Health check | Đã triển khai |
| `/db-check` | GET | Kiểm tra kết nối database | Đã triển khai |
| `/docs` | GET | Swagger API documentation | Đã triển khai |
| `/redoc` | GET | ReDoc API documentation | Đã triển khai |

## Ghi chú

- Các endpoint có trạng thái "Đã triển khai" đã được xác nhận hoạt động trong checklist.
- Tất cả các API endpoint đều yêu cầu xác thực JWT trừ endpoint health check.
- Đối với một số endpoint, có thể yêu cầu quyền admin, dispatcher hoặc quyền phù hợp theo vai trò.
- Các endpoint liên quan đến attachments phối hợp với File Service.
- Các cập nhật trạng thái ticket sẽ tự động gửi thông báo qua Notification Service.