# Report Service API Endpoints

Dựa trên checklist của Report Service, dưới đây là danh sách các API endpoint cần thiết và trạng thái hiện tại của chúng.

## Tạo và Quản lý Báo cáo

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/reports` | GET | Lấy danh sách báo cáo đã lưu | Đã triển khai |
| `/api/v1/reports/{report_id}` | GET | Lấy thông tin chi tiết của một báo cáo | Đã triển khai |
| `/api/v1/reports` | POST | Tạo báo cáo mới theo yêu cầu | Đã triển khai |
| `/api/v1/reports/{report_id}` | PUT | Cập nhật thông tin báo cáo | Đã triển khai |
| `/api/v1/reports/{report_id}` | DELETE | Xóa báo cáo | Đã triển khai |
| `/api/v1/reports/run` | POST | Chạy báo cáo ngay lập tức | Đã triển khai |

## Download và Export Báo cáo

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/reports/{report_id}/download` | GET | Tải xuống báo cáo dưới dạng file | Đã triển khai |
| `/api/v1/reports/{report_id}/pdf` | GET | Tải xuống báo cáo dạng PDF | Đã triển khai |
| `/api/v1/reports/{report_id}/excel` | GET | Tải xuống báo cáo dạng Excel | Đã triển khai |
| `/api/v1/reports/{report_id}/csv` | GET | Tải xuống báo cáo dạng CSV | Đã triển khai |
| `/api/v1/reports/{report_id}/json` | GET | Lấy dữ liệu báo cáo dạng JSON | Đã triển khai |

## Quản lý Template Báo cáo

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/templates` | GET | Lấy danh sách template báo cáo | Đã triển khai |
| `/api/v1/templates/{template_id}` | GET | Lấy thông tin chi tiết của một template | Đã triển khai |
| `/api/v1/templates` | POST | Tạo template báo cáo mới | Đã triển khai |
| `/api/v1/templates/{template_id}` | PUT | Cập nhật template báo cáo | Đã triển khai |
| `/api/v1/templates/{template_id}` | DELETE | Xóa template báo cáo | Đã triển khai |
| `/api/v1/templates/{template_id}/preview` | POST | Xem trước báo cáo từ template | Đã triển khai |

## Lập lịch Báo cáo

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/schedules` | GET | Lấy danh sách lịch báo cáo | Đã triển khai |
| `/api/v1/schedules/{schedule_id}` | GET | Lấy thông tin chi tiết lịch báo cáo | Đã triển khai |
| `/api/v1/schedules` | POST | Tạo lịch báo cáo mới | Đã triển khai |
| `/api/v1/schedules/{schedule_id}` | PUT | Cập nhật lịch báo cáo | Đã triển khai |
| `/api/v1/schedules/{schedule_id}` | DELETE | Xóa lịch báo cáo | Đã triển khai |
| `/api/v1/schedules/{schedule_id}/pause` | POST | Tạm dừng lịch báo cáo | Đã triển khai |
| `/api/v1/schedules/{schedule_id}/resume` | POST | Tiếp tục lịch báo cáo | Đã triển khai |
| `/api/v1/schedules/history` | GET | Xem lịch sử chạy báo cáo tự động | Đã triển khai |

## Data Visualization và Biểu đồ

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/charts` | GET | Lấy danh sách biểu đồ đã lưu | Đã triển khai |
| `/api/v1/charts/{chart_id}` | GET | Lấy thông tin chi tiết biểu đồ | Đã triển khai |
| `/api/v1/charts` | POST | Tạo biểu đồ mới | Đã triển khai |
| `/api/v1/charts/{chart_id}` | PUT | Cập nhật biểu đồ | Đã triển khai |
| `/api/v1/charts/{chart_id}` | DELETE | Xóa biểu đồ | Đã triển khai |
| `/api/v1/charts/{chart_id}/data` | GET | Lấy dữ liệu biểu đồ | Đã triển khai |
| `/api/v1/charts/{chart_id}/image` | GET | Lấy hình ảnh biểu đồ | Đã triển khai |

## Query Builder và Dữ liệu

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/data/tickets` | GET | Lấy dữ liệu ticket cho báo cáo | Đã triển khai |
| `/api/v1/data/users` | GET | Lấy dữ liệu người dùng cho báo cáo | Đã triển khai |
| `/api/v1/data/departments` | GET | Lấy dữ liệu phòng ban cho báo cáo | Đã triển khai |
| `/api/v1/data/query` | POST | Thực hiện truy vấn tùy chỉnh | Đã triển khai |
| `/api/v1/data/aggregate` | POST | Thực hiện phân tích tổng hợp tùy chỉnh | Đã triển khai |
| `/api/v1/data/validate-query` | POST | Kiểm tra cú pháp truy vấn | Đã triển khai |

## Báo cáo Chuẩn Có Sẵn

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/standard-reports/ticket-resolution-time` | GET | Báo cáo thời gian giải quyết ticket | Đã triển khai |
| `/api/v1/standard-reports/ticket-by-status` | GET | Báo cáo ticket theo trạng thái | Đã triển khai |
| `/api/v1/standard-reports/ticket-by-department` | GET | Báo cáo ticket theo phòng ban | Đã triển khai |
| `/api/v1/standard-reports/agent-performance` | GET | Báo cáo hiệu suất nhân viên | Đã triển khai |
| `/api/v1/standard-reports/customer-satisfaction` | GET | Báo cáo mức độ hài lòng khách hàng | Đã triển khai |
| `/api/v1/standard-reports/workload-distribution` | GET | Báo cáo phân phối khối lượng công việc | Đã triển khai |

## Tích hợp và Hệ thống

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/` | GET | Health check | Đã triển khai |
| `/db-check` | GET | Kiểm tra kết nối database | Đã triển khai |
| `/cache-check` | GET | Kiểm tra kết nối cache | Đã triển khai |
| `/docs` | GET | Swagger API documentation | Đã triển khai |
| `/redoc` | GET | ReDoc API documentation | Đã triển khai |

## Ghi chú

- Các endpoint có trạng thái "Đã triển khai" đã được xác nhận hoạt động trong checklist.
- Tất cả các API endpoint đều yêu cầu xác thực JWT trừ endpoint health check.
- Một số endpoint báo cáo có thể yêu cầu thời gian xử lý dài đối với tập dữ liệu lớn.
- Hệ thống sử dụng caching để tối ưu hiệu suất các báo cáo được truy cập thường xuyên.
- Các báo cáo có thể được lập lịch gửi tự động qua email sử dụng Notification Service.
- Service này chủ yếu truy cập database ở chế độ read-only để đảm bảo an toàn dữ liệu.