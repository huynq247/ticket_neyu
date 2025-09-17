# Analytics Service API Endpoints

Dựa trên checklist của Analytics Service, dưới đây là danh sách các API endpoint cần thiết và trạng thái hiện tại của chúng.

## KPI Dashboards và Phân tích Tổng quan

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/dashboards` | GET | Lấy danh sách dashboard có sẵn | Đã triển khai |
| `/api/v1/dashboards/{dashboard_id}` | GET | Lấy dữ liệu dashboard cụ thể | Đã triển khai |
| `/api/v1/dashboards/default` | GET | Lấy dữ liệu dashboard mặc định | Đã triển khai |
| `/api/v1/dashboards/refresh` | POST | Làm mới dữ liệu dashboard | Đã triển khai |
| `/api/v1/kpis` | GET | Lấy danh sách tất cả KPI đã định nghĩa | Đã triển khai |
| `/api/v1/kpis/{kpi_id}` | GET | Lấy dữ liệu KPI cụ thể | Đã triển khai |
| `/api/v1/kpis/custom` | POST | Tạo KPI tùy chỉnh | Đã triển khai |

## Phân tích Thời gian và Hiệu suất

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/timeseries/tickets` | GET | Phân tích ticket theo thời gian | Đã triển khai |
| `/api/v1/timeseries/users` | GET | Phân tích hoạt động người dùng theo thời gian | Đã triển khai |
| `/api/v1/timeseries/departments` | GET | Phân tích hiệu suất phòng ban theo thời gian | Đã triển khai |
| `/api/v1/performance/users` | GET | Phân tích hiệu suất người dùng | Đã triển khai |
| `/api/v1/performance/departments` | GET | Phân tích hiệu suất phòng ban | Đã triển khai |
| `/api/v1/performance/system` | GET | Phân tích hiệu suất hệ thống | Đã triển khai |

## Phân tích Hành vi Người dùng 

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/user-behavior/ticket-patterns` | GET | Phân tích mẫu tạo ticket của người dùng | Đã triển khai |
| `/api/v1/user-behavior/response-times` | GET | Phân tích thời gian phản hồi của nhân viên | Đã triển khai |
| `/api/v1/user-behavior/activity-heatmap` | GET | Bản đồ nhiệt hoạt động người dùng | Đã triển khai |
| `/api/v1/user-behavior/interactions` | GET | Phân tích tương tác giữa người dùng | Đã triển khai |
| `/api/v1/user-behavior/satisfaction` | GET | Phân tích mức độ hài lòng khách hàng | Đã triển khai |

## Dự báo và Phát hiện Bất thường

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/forecasting/tickets` | GET | Dự báo số lượng ticket | Đã triển khai |
| `/api/v1/forecasting/workload` | GET | Dự báo khối lượng công việc | Đã triển khai |
| `/api/v1/forecasting/custom` | POST | Dự báo tùy chỉnh | Đã triển khai |
| `/api/v1/anomaly-detection/tickets` | GET | Phát hiện bất thường trong ticket | Đã triển khai |
| `/api/v1/anomaly-detection/users` | GET | Phát hiện bất thường trong hành vi người dùng | Đã triển khai |
| `/api/v1/anomaly-detection/system` | GET | Phát hiện bất thường trong hệ thống | Đã triển khai |
| `/api/v1/recommendations/assign` | GET | Đề xuất phân công ticket | Đã triển khai |

## Truy vấn Tùy chỉnh và Xuất dữ liệu

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/custom-query` | POST | Thực hiện truy vấn phân tích tùy chỉnh | Đã triển khai |
| `/api/v1/data-export/csv` | POST | Xuất dữ liệu phân tích sang CSV | Đang phát triển |
| `/api/v1/data-export/excel` | POST | Xuất dữ liệu phân tích sang Excel | Đang phát triển |
| `/api/v1/data-export/json` | POST | Xuất dữ liệu phân tích sang JSON | Đang phát triển |

## ETL và Quản lý Dữ liệu

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/etl/status` | GET | Kiểm tra trạng thái ETL jobs | Đã triển khai |
| `/api/v1/etl/trigger` | POST | Kích hoạt ETL job thủ công | Đã triển khai |
| `/api/v1/etl/schedule` | GET | Xem lịch trình ETL jobs | Đã triển khai |
| `/api/v1/etl/schedule` | POST | Cập nhật lịch trình ETL jobs | Đã triển khai |
| `/api/v1/data-health` | GET | Kiểm tra sức khỏe dữ liệu | Đã triển khai |
| `/api/v1/data-sources` | GET | Lấy danh sách nguồn dữ liệu | Đã triển khai |

## Tích hợp và Hệ thống

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/` | GET | Health check | Đã triển khai |
| `/db-check` | GET | Kiểm tra kết nối database | Đã triển khai |
| `/metrics` | GET | Prometheus metrics | Đã triển khai |
| `/docs` | GET | Swagger API documentation | Đã triển khai |
| `/redoc` | GET | ReDoc API documentation | Đã triển khai |

## Ghi chú

- Các endpoint có trạng thái "Đã triển khai" đã được xác nhận hoạt động trong checklist.
- Các endpoint có trạng thái "Đang phát triển" đang trong quá trình triển khai.
- Tất cả các API endpoint đều yêu cầu xác thực JWT trừ endpoint health check.
- Các endpoint phân tích phức tạp có thể mất nhiều thời gian để xử lý với tập dữ liệu lớn.
- Hệ thống sử dụng caching để tối ưu hiệu suất các truy vấn phân tích thường xuyên.
- ETL jobs chạy theo lịch trình để cập nhật dữ liệu phân tích.
- Machine learning models được sử dụng cho dự báo và phát hiện bất thường.
- Một số endpoint có thể yêu cầu quyền admin hoặc phân quyền đặc biệt.