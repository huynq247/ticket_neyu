# File Service

Microservice cho việc lưu trữ và quản lý files trong hệ thống Ticket Management.

## Tính năng

- Upload và download files
- Quản lý metadata của files
- Liên kết files với tickets
- Phân quyền truy cập files
- Hỗ trợ nhiều backend lưu trữ (local filesystem, S3, MongoDB GridFS)

## Cài đặt

### Sử dụng Docker

```bash
docker build -t file-service .
docker run -d -p 8002:8002 --name file-service file-service
```

### Sử dụng Local Environment

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

## API Endpoints

- `POST /api/v1/files`: Upload file
- `GET /api/v1/files/{file_id}`: Download file
- `GET /api/v1/files`: Danh sách files
- `DELETE /api/v1/files/{file_id}`: Xóa file
- `GET /api/v1/files/metadata/{file_id}`: Lấy metadata của file

## Kết nối với services khác

File service tích hợp với:
- User Service: Xác thực và phân quyền
- Ticket Service: Liên kết files với tickets