# Checklist cho File Service

## Thiết kế Hệ thống
- [ ] Thiết kế cấu trúc lưu trữ file
- [ ] Thiết kế metadata cho files
- [ ] Thiết kế cơ chế phân quyền truy cập file
- [ ] Thiết kế cơ chế version control (nếu cần)

## Phát triển Core Components
- [ ] Thiết lập project structure (FastAPI)
- [ ] Xây dựng models và schemas
- [ ] Xây dựng cơ chế upload và download
- [ ] Xây dựng cơ chế xác thực tệp
- [ ] Xây dựng cơ chế quét virus/malware
- [ ] Xây dựng cơ chế xử lý file (resize, convert, etc. nếu cần)

## Phát triển Storage Backends
- [ ] Tích hợp với local filesystem (cho development)
- [ ] Tích hợp với Object Storage (MinIO/S3)
- [ ] Tích hợp với MongoDB GridFS (tùy chọn)
- [ ] Xây dựng adapter pattern cho các storage backends

## Phát triển API
- [ ] Phát triển API endpoint cho upload file
- [ ] Phát triển API endpoint cho download file
- [ ] Phát triển API endpoint cho quản lý file metadata
- [ ] Phát triển API endpoint cho kiểm tra quyền truy cập
- [ ] Phát triển API endpoint cho tìm kiếm file

## Tính năng Nâng cao
- [ ] Xây dựng cơ chế multipart upload cho file lớn
- [ ] Xây dựng cơ chế caching
- [ ] Xây dựng cơ chế generate thumbnail
- [ ] Xây dựng cơ chế file expiration

## Tích hợp với Services khác
- [ ] Tích hợp với User Service (để xác thực quyền)
- [ ] Tích hợp với Ticket Service (để liên kết file với ticket)

## Testing
- [ ] Unit tests cho file handling
- [ ] Integration tests cho storage backends
- [ ] Performance tests cho upload/download
- [ ] Security tests

## Triển khai
- [ ] Tạo Dockerfile
- [ ] Cấu hình Object Storage
- [ ] Thiết lập logging và monitoring
- [ ] Cấu hình backup và recovery

## Documentation
- [ ] API documentation
- [ ] File storage guidelines
- [ ] Security policies