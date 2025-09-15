# Kiến Trúc Microservices cho Hệ Thống Quản Lý Ticket

## Tổng quan kiến trúc

```
┌───────────────────────────────────────────────────────────────────────┐
│                         Client Applications                            │
│                                                                       │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐              │
│  │  Web Browser │   │  Mobile App  │   │Telegram Bot  │              │
│  └──────────────┘   └──────────────┘   └──────────────┘              │
└───────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────────────┐
│                            API Gateway                                │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  - Điểm vào duy nhất cho tất cả client                         │  │
│  │  - Xác thực và ủy quyền                                        │  │
│  │  - Cân bằng tải                                                │  │
│  │  - Định tuyến requests                                         │  │
│  │  - Giám sát và logging                                         │  │
│  └────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────────────┐
│                          Microservices                                │
│                                                                       │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐              │
│  │ User Service │   │Ticket Service│   │   File       │              │
│  │(PostgreSQL)  │   │  (MongoDB)   │   │  Service     │              │
│  └──────────────┘   └──────────────┘   └──────────────┘              │
│                                                                       │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐              │
│  │Notification  │   │ Report       │   │  Analytics   │              │
│  │  Service     │   │  Service     │   │   Service    │              │
│  └──────────────┘   └──────────────┘   └──────────────┘              │
└───────────────────────────────────────────────────────────────────────┘
```

## Chi tiết từng Microservice

### 1. API Gateway
- **Chức năng**: 
  - Điểm vào duy nhất cho tất cả client (Web, Mobile, Telegram Bot)
  - Xác thực token và phân quyền truy cập
  - Định tuyến request đến microservice tương ứng
  - Cân bằng tải
  - Xử lý timeout và retry
  - Logging và monitoring
- **Công nghệ đề xuất**: 
  - Kong, Nginx, hoặc API Gateway tự phát triển bằng FastAPI

### 2. User Service
- **Chức năng**:
  - Quản lý thông tin người dùng
  - Xác thực và phân quyền
  - Quản lý vai trò và phân quyền
  - Tích hợp với các hệ thống xác thực bên ngoài (nếu cần)
- **Cơ sở dữ liệu**: PostgreSQL
- **Công nghệ đề xuất**: Python với Flask/FastAPI + SQLAlchemy

### 3. Ticket Service
- **Chức năng**:
  - Tạo và quản lý ticket
  - Phân loại và ưu tiên ticket
  - Phân công ticket
  - Cập nhật trạng thái và theo dõi tiến độ
  - Tìm kiếm và lọc ticket
- **Cơ sở dữ liệu**: MongoDB
- **Công nghệ đề xuất**: Python với FastAPI + Motor/PyMongo

### 4. File Service
- **Chức năng**:
  - Quản lý tệp đính kèm
  - Lưu trữ và truy xuất tệp
  - Quét virus và xác thực tệp
  - Phân quyền truy cập tệp
- **Lưu trữ**: Object Storage (MinIO, S3) hoặc GridFS (MongoDB)
- **Công nghệ đề xuất**: Python với FastAPI

### 5. Notification Service
- **Chức năng**:
  - Gửi thông báo qua email
  - Gửi thông báo qua Telegram
  - Quản lý mẫu thông báo
  - Lập lịch nhắc nhở
- **Cơ sở dữ liệu**: Redis (hàng đợi thông báo)
- **Công nghệ đề xuất**: Python với Celery + Redis

### 6. Report Service
- **Chức năng**:
  - Tạo báo cáo và thống kê
  - Xuất báo cáo ra các định dạng (PDF, Excel)
  - Lập lịch báo cáo tự động
- **Cơ sở dữ liệu**: Kết nối đến MongoDB (đọc) và PostgreSQL (đọc)
- **Công nghệ đề xuất**: Python với FastAPI + Pandas

### 7. Analytics Service
- **Chức năng**:
  - Phân tích dữ liệu nâng cao
  - Cung cấp chỉ số KPI
  - Dashboard trực quan
- **Cơ sở dữ liệu**: Data Warehouse / MongoDB Aggregation
- **Công nghệ đề xuất**: Python với FastAPI + Pandas + Plotly

## Mô hình Dữ liệu

### User Service (PostgreSQL)
```
- users (id, username, email, password_hash, role_id, department_id, created_at, updated_at)
- roles (id, name, description, permissions)
- departments (id, name, description, manager_id)
- permissions (id, name, description)
- role_permissions (role_id, permission_id)
```

### Ticket Service (MongoDB)
```
tickets {
  _id: ObjectId,
  title: String,
  description: String,
  created_by: ObjectId, // reference to user
  assigned_to: ObjectId, // reference to user
  department_id: ObjectId,
  status: String, // New, Acknowledged, InProgress, WaitingForResponse, Resolved, Closed, Reopened
  priority: String, // Low, Medium, High, Critical
  category: String,
  created_at: DateTime,
  updated_at: DateTime,
  due_date: DateTime,
  tags: Array,
  attachments: Array of references to files,
  comments: Array of {
    user_id: ObjectId,
    content: String,
    created_at: DateTime
  },
  history: Array of status changes
}
```

## Giao tiếp giữa các Microservices

### Đồng bộ (Synchronous)
- REST API giữa các service khi cần dữ liệu ngay lập tức
- gRPC cho các cuộc gọi nội bộ hiệu suất cao

### Bất đồng bộ (Asynchronous)
- Message broker (RabbitMQ hoặc Kafka) cho các sự kiện và thông báo
- Redis pub/sub cho các cập nhật thời gian thực

## Triển khai

### Containerization
- Docker cho đóng gói các microservices
- Docker Compose cho môi trường phát triển

### Orchestration
- Kubernetes cho môi trường sản xuất
- Helm charts cho quản lý cấu hình triển khai

### CI/CD
- GitHub Actions hoặc GitLab CI
- Automated testing (unit, integration, end-to-end)
- Automated deployment

## Monitoring & Logging
- Prometheus cho metrics
- Grafana cho visualization
- ELK Stack (Elasticsearch, Logstash, Kibana) cho logging
- Jaeger hoặc Zipkin cho distributed tracing