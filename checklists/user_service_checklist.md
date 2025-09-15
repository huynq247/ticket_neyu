# Checklist cho User Service

## Thiết kế Cơ sở dữ liệu
- [ ] Thiết kế schema cho bảng users
- [ ] Thiết kế schema cho bảng roles và permissions
- [ ] Thiết kế schema cho bảng departments
- [ ] Thiết lập vai trò Dispatcher/Coordinator cho phân chia tickets
- [ ] Thiết lập quan hệ giữa các bảng
- [ ] Thiết lập indexes cho tối ưu truy vấn
- [ ] Thiết kế migration scripts

## Phát triển API
- [ ] Thiết lập project structure (FastAPI/Flask)
- [ ] Xây dựng models và schemas
- [ ] Phát triển API endpoint cho quản lý người dùng (CRUD)
- [ ] Phát triển API endpoint cho xác thực (login, logout)
- [ ] Phát triển API endpoint cho quản lý vai trò và quyền
- [ ] Phát triển API endpoint cho quản lý phòng ban
- [ ] Phát triển API endpoint cho Dispatcher/Coordinator
- [ ] Xây dựng middleware xác thực và phân quyền

## Tính năng bảo mật
- [ ] Mã hóa mật khẩu
- [ ] Xây dựng cơ chế JWT
- [ ] Xây dựng refresh token
- [ ] Xây dựng cơ chế khóa tài khoản
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
- [ ] Tạo Dockerfile
- [ ] Cấu hình kết nối PostgreSQL
- [ ] Thiết lập migrations và seeding
- [ ] Thiết lập logging và monitoring

## Documentation
- [ ] API documentation
- [ ] Database schema documentation
- [ ] Authentication flow documentation