# Ticket Service

Service này chịu trách nhiệm quản lý các ticket requests từ người dùng.

## Chức năng chính

- Tạo và quản lý tickets (CRUD)
- Quản lý comments và attachments
- Theo dõi trạng thái và lịch sử thay đổi
- Phân loại và ưu tiên tickets
- Phân công tickets cho nhân viên hỗ trợ
- Đánh giá mức độ hài lòng

## Cơ sở dữ liệu

- MongoDB

## Công nghệ

- Python (FastAPI)
- PyMongo (MongoDB driver)
- JWT Authentication

## Cài đặt và Chạy

### Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Thiết lập biến môi trường

Sử dụng các biến môi trường từ `database.env` trong thư mục `config`:

- MONGODB_URI
- MONGODB_USER
- MONGODB_PASSWORD
- MONGODB_DATABASE

### Chạy ứng dụng

```bash
uvicorn main:app --reload
```

Truy cập API tại http://localhost:8001

## API Endpoints

### Tickets

- `GET /api/v1/tickets` - Lấy danh sách tickets với các bộ lọc
- `POST /api/v1/tickets` - Tạo ticket mới
- `GET /api/v1/tickets/{ticket_id}` - Lấy chi tiết một ticket
- `PUT /api/v1/tickets/{ticket_id}` - Cập nhật ticket
- `DELETE /api/v1/tickets/{ticket_id}` - Xóa ticket

### Categories

- `GET /api/v1/categories` - Lấy danh sách categories
- `POST /api/v1/categories` - Tạo category mới
- `GET /api/v1/categories/{category_id}` - Lấy chi tiết một category
- `PUT /api/v1/categories/{category_id}` - Cập nhật category
- `DELETE /api/v1/categories/{category_id}` - Xóa category

### Comments

- `GET /api/v1/comments/{ticket_id}` - Lấy comments của một ticket
- `POST /api/v1/comments/{ticket_id}` - Thêm comment mới
- `DELETE /api/v1/comments/{comment_id}` - Xóa comment

## Documentation

API documentation có sẵn tại http://localhost:8001/docs sau khi chạy ứng dụng.