# Notification Service API Endpoints

Dựa trên checklist của Notification Service, dưới đây là danh sách các API endpoint cần thiết và trạng thái hiện tại của chúng.

## Gửi và Quản lý Thông báo

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/notifications/send` | POST | Gửi thông báo mới | Đã triển khai |
| `/api/v1/notifications` | GET | Lấy danh sách thông báo với phân trang và lọc | Đã triển khai |
| `/api/v1/notifications/{notification_id}` | GET | Lấy thông tin chi tiết của một thông báo | Đã triển khai |
| `/api/v1/notifications/{notification_id}` | DELETE | Xóa thông báo | Đã triển khai |
| `/api/v1/notifications/batch` | POST | Gửi nhiều thông báo cùng lúc | Cần triển khai |

## Quản lý Template

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/templates` | GET | Lấy danh sách template | Đã triển khai |
| `/api/v1/templates/{template_id}` | GET | Lấy thông tin chi tiết của một template | Đã triển khai |
| `/api/v1/templates` | POST | Tạo template mới | Đã triển khai |
| `/api/v1/templates/{template_id}` | PUT | Cập nhật template | Đã triển khai |
| `/api/v1/templates/{template_id}` | DELETE | Xóa template | Đã triển khai |
| `/api/v1/templates/{template_id}/render` | POST | Hiển thị preview của template với dữ liệu mẫu | Đã triển khai |

## Lập lịch Thông báo

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/schedules` | GET | Lấy danh sách thông báo được lập lịch | Đã triển khai |
| `/api/v1/schedules` | POST | Lập lịch thông báo mới | Đã triển khai |
| `/api/v1/schedules/{schedule_id}` | GET | Lấy thông tin chi tiết lịch thông báo | Đã triển khai |
| `/api/v1/schedules/{schedule_id}` | PUT | Cập nhật lịch thông báo | Đã triển khai |
| `/api/v1/schedules/{schedule_id}` | DELETE | Hủy lịch thông báo | Đã triển khai |
| `/api/v1/schedules/{schedule_id}/pause` | POST | Tạm dừng lịch thông báo | Đã triển khai |
| `/api/v1/schedules/{schedule_id}/resume` | POST | Tiếp tục lịch thông báo | Đã triển khai |

## Trạng thái và Theo dõi

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/notifications/{notification_id}/status` | GET | Kiểm tra trạng thái thông báo | Đã triển khai |
| `/api/v1/notifications/stats` | GET | Thống kê thông báo (gửi thành công/thất bại) | Đã triển khai |
| `/api/v1/notifications/user/{user_id}` | GET | Lấy danh sách thông báo của người dùng | Đã triển khai |
| `/api/v1/notifications/user/{user_id}/unread` | GET | Lấy số lượng thông báo chưa đọc | Đã triển khai |
| `/api/v1/notifications/{notification_id}/mark-read` | PUT | Đánh dấu thông báo đã đọc | Đã triển khai |
| `/api/v1/notifications/mark-all-read` | PUT | Đánh dấu tất cả thông báo đã đọc | Đã triển khai |

## Kênh Thông báo

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/channels` | GET | Lấy danh sách kênh thông báo có sẵn | Đã triển khai |
| `/api/v1/channels/email/settings` | GET | Lấy cấu hình email | Đã triển khai |
| `/api/v1/channels/email/settings` | PUT | Cập nhật cấu hình email | Đã triển khai |
| `/api/v1/channels/telegram/settings` | GET | Lấy cấu hình Telegram | Đã triển khai |
| `/api/v1/channels/telegram/settings` | PUT | Cập nhật cấu hình Telegram | Đã triển khai |
| `/api/v1/channels/test` | POST | Kiểm tra kênh thông báo | Đã triển khai |

## Tích hợp và Webhook

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/webhooks` | GET | Lấy danh sách webhook | Đã triển khai |
| `/api/v1/webhooks` | POST | Tạo webhook mới | Đã triển khai |
| `/api/v1/webhooks/{webhook_id}` | DELETE | Xóa webhook | Đã triển khai |
| `/api/v1/events` | POST | Endpoint nhận sự kiện từ services khác | Đã triển khai |

## Tích hợp và Hệ thống

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/` | GET | Health check | Đã triển khai |
| `/db-check` | GET | Kiểm tra kết nối database | Đã triển khai |
| `/queue-check` | GET | Kiểm tra kết nối message queue | Đã triển khai |
| `/docs` | GET | Swagger API documentation | Đã triển khai |
| `/redoc` | GET | ReDoc API documentation | Đã triển khai |

## Ghi chú

- Các endpoint có trạng thái "Đã triển khai" đã được xác nhận hoạt động trong checklist.
- Các endpoint có trạng thái "Cần triển khai" cần được phát triển dựa trên checklist.
- Tất cả các API endpoint đều yêu cầu xác thực JWT trừ endpoint health check.
- Service này có thể chạy ở chế độ giới hạn nếu không thể kết nối tới Telegram hoặc SMTP server.
- Hệ thống sử dụng Celery và Redis để xử lý hàng đợi thông báo.
- Template sử dụng cú pháp Jinja2 để render nội dung thông báo.