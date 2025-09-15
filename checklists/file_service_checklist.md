# Checklist cho File Service

## Thiết kế Hệ thống
- [x] Thiết kế cấu trúc lưu trữ file
- [x] Thiết kế metadata cho files
- [x] Thiết kế cơ chế phân quyền truy cập file
- [ ] Thiết kế cơ chế version control (nếu cần)

## Phát triển Core Components
- [x] Thiết lập project structure (FastAPI)
- [x] Xây dựng models và schemas
- [x] Xây dựng cơ chế upload và download
- [x] Xây dựng cơ chế xác thực tệp
- [ ] Xây dựng cơ chế quét virus/malware
- [ ] Xây dựng cơ chế xử lý file (resize, convert, etc. nếu cần)

## Phát triển Storage Backends
- [x] Tích hợp với local filesystem (cho development)
- [ ] Tích hợp với Object Storage (MinIO/S3)
- [ ] Tích hợp với MongoDB GridFS (tùy chọn)
- [x] Xây dựng adapter pattern cho các storage backends

## Phát triển API
- [x] Phát triển API endpoint cho upload file
- [x] Phát triển API endpoint cho download file
- [x] Phát triển API endpoint cho quản lý file metadata
- [x] Phát triển API endpoint cho kiểm tra quyền truy cập
- [x] Phát triển API endpoint cho tìm kiếm file

## Tính năng Nâng cao
- [ ] Xây dựng cơ chế multipart upload cho file lớn
- [ ] Xây dựng cơ chế caching
- [ ] Xây dựng cơ chế generate thumbnail
- [ ] Xây dựng cơ chế file expiration

## Tích hợp với Services khác
- [x] Tích hợp với User Service (để xác thực quyền)
- [x] Tích hợp với Ticket Service (để liên kết file với ticket)

## Testing
- [ ] Unit tests cho file handling
- [ ] Integration tests cho storage backends
- [ ] Performance tests cho upload/download
- [ ] Security tests

## Triển khai
- [x] Tạo Dockerfile
- [ ] Cấu hình Object Storage
- [ ] Thiết lập logging và monitoring
- [ ] Cấu hình backup và recovery

## Documentation
- [x] API documentation
- [ ] File storage guidelines
- [ ] Security policies