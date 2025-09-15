# Report Service

Report Service là một microservice trong hệ thống quản lý ticket, chịu trách nhiệm tạo, quản lý và lập lịch các báo cáo phân tích.

## Tính năng

- Tạo và quản lý báo cáo phân tích
- Quản lý mẫu báo cáo
- Tạo và quản lý dashboards
- Lập lịch và tự động hóa báo cáo
- Xuất báo cáo sang nhiều định dạng (JSON, CSV, Excel, PDF, HTML)
- Tích hợp với các dịch vụ khác để lấy dữ liệu

## Công nghệ sử dụng

- Python 3.11
- FastAPI
- MongoDB (lưu trữ báo cáo, mẫu và cấu hình)
- Redis (caching)
- Pandas, NumPy, Matplotlib, Seaborn (phân tích dữ liệu và trực quan hóa)
- APScheduler (lập lịch báo cáo)
- Docker

## API Endpoints

### Reports API

- `GET /api/reports` - Lấy danh sách báo cáo
- `GET /api/reports/{report_id}` - Lấy chi tiết báo cáo
- `POST /api/reports` - Tạo báo cáo mới
- `PUT /api/reports/{report_id}` - Cập nhật báo cáo
- `DELETE /api/reports/{report_id}` - Xóa báo cáo

### Templates API

- `GET /api/templates` - Lấy danh sách mẫu báo cáo
- `GET /api/templates/{template_id}` - Lấy chi tiết mẫu báo cáo
- `POST /api/templates` - Tạo mẫu báo cáo mới
- `PUT /api/templates/{template_id}` - Cập nhật mẫu báo cáo
- `DELETE /api/templates/{template_id}` - Xóa mẫu báo cáo

### Dashboards API

- `GET /api/dashboards` - Lấy danh sách dashboards
- `GET /api/dashboards/{dashboard_id}` - Lấy chi tiết dashboard
- `POST /api/dashboards` - Tạo dashboard mới
- `PUT /api/dashboards/{dashboard_id}` - Cập nhật dashboard
- `DELETE /api/dashboards/{dashboard_id}` - Xóa dashboard

### Scheduled Reports API

- `GET /api/scheduled-reports` - Lấy danh sách báo cáo theo lịch
- `GET /api/scheduled-reports/{report_id}` - Lấy chi tiết báo cáo theo lịch
- `POST /api/scheduled-reports` - Tạo báo cáo theo lịch mới
- `PUT /api/scheduled-reports/{report_id}` - Cập nhật báo cáo theo lịch
- `DELETE /api/scheduled-reports/{report_id}` - Xóa báo cáo theo lịch

### Report Execution API

- `POST /api/execute/generate` - Tạo báo cáo theo yêu cầu
- `GET /api/execute/download/{report_id}` - Tải xuống báo cáo đã tạo

## Cài đặt và chạy

### Sử dụng Docker

```bash
docker-compose up -d
```

### Cài đặt thủ công

1. Cài đặt các dependencies:

```bash
pip install -r requirements.txt
```

2. Cài đặt wkhtmltopdf cho việc tạo file PDF:

```bash
# Trên Ubuntu/Debian
apt-get install wkhtmltopdf

# Trên CentOS/RHEL
yum install wkhtmltopdf

# Trên Windows
# Tải và cài đặt từ https://wkhtmltopdf.org/downloads.html
```

3. Chạy ứng dụng:

```bash
uvicorn main:app --host 0.0.0.0 --port 8004 --reload
```

## Biến môi trường

Tạo file `.env` với các biến môi trường sau:

```
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=report_service
REDIS_URL=redis://localhost:6379/0
TICKET_SERVICE_URL=http://localhost:8001
USER_SERVICE_URL=http://localhost:8000
NOTIFICATION_SERVICE_URL=http://localhost:8003
REPORT_SERVICE_URL=http://localhost:8004
JWT_SECRET=your_jwt_secret_key
SERVICE_API_KEY=your_service_api_key
DEBUG_MODE=True
```

## Loại báo cáo hỗ trợ

- **Ticket Summary**: Tổng quan về ticket (số lượng, trạng thái, mức độ ưu tiên, thời gian giải quyết)
- **User Activity**: Hoạt động của người dùng (tickets tạo, người dùng tích cực nhất)
- **Response Time**: Phân tích thời gian phản hồi và giải quyết

## Định dạng xuất

- JSON
- CSV
- Excel
- PDF
- HTML

## Đóng góp

Vui lòng đọc [CONTRIBUTING.md](CONTRIBUTING.md) để biết chi tiết về quy trình gửi pull request.