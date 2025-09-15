# Checklist cho User Service

## Thiết kế Cơ sở dữ liệu
- [x] Thiết kế schema cho bảng users
- [x] Thiết kế schema cho bảng roles và permissions
- [x] Thiết kế schema cho bảng departments
- [x] Thiết lập vai trò Dispatcher/Coordinator cho phân chia tickets
- [x] Thiết lập quan hệ giữa các bảng
- [x] Thiết lập indexes cho tối ưu truy vấn
- [ ] Thiết kế migration scripts

## Phát triển API
- [x] Thiết lập project structure (FastAPI)
- [x] Xây dựng models và schemas
- [x] Phát triển API endpoint cho quản lý người dùng (CRUD)
- [x] Phát triển API endpoint cho xác thực (login, logout)
- [x] Phát triển API endpoint cho quản lý vai trò và quyền
- [x] Phát triển API endpoint cho quản lý phòng ban
- [x] Phát triển API endpoint cho Dispatcher/Coordinator
- [x] Xây dựng middleware xác thực và phân quyền

## Tính năng bảo mật
- [x] Mã hóa mật khẩu
- [x] Xây dựng cơ chế JWT
- [x] Xây dựng refresh token
- [x] Xây dựng cơ chế khóa tài khoản
- [ ] Xây dựng cơ chế reset mật khẩu
- [ ] Xây dựng cơ chế xác thực hai lớp (nếu cần)

## Tích hợp
- [ ] Tích hợp với API Gateway
- [ ] Tích hợp với Notification Service (cho email xác thực, reset mật khẩu)
- [ ] Thiết lập giao tiếp event-based với các service khác

## Testing
- [ ] Unit tests cho các model
- [ ] Integration tests cho API endpoints
- [ ] Security tests
- [ ] Performance tests

## Triển khai
- [x] Tạo Dockerfile
- [x] Cấu hình kết nối PostgreSQL
- [ ] Thiết lập migrations và seeding
- [ ] Thiết lập logging và monitoring

## Documentation
- [x] API documentation
- [x] Database schema documentation
- [x] Authentication flow documentation