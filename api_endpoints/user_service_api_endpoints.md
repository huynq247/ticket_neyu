# User Service API Endpoints

Dựa trên checklist của User Service, dưới đây là danh sách các API endpoint cần thiết và trạng thái hiện tại của chúng.

## Quản lý người dùng (CRUD)

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/users` | GET | Lấy danh sách người dùng với phân trang và lọc | Đã triển khai |
| `/api/v1/users/{user_id}` | GET | Lấy thông tin chi tiết của một người dùng | Đã triển khai |
| `/api/v1/users` | POST | Tạo người dùng mới | Đã triển khai |
| `/api/v1/users/{user_id}` | PUT | Cập nhật thông tin người dùng | Đã triển khai |
| `/api/v1/users/{user_id}` | DELETE | Xóa người dùng | Đã triển khai |
| `/api/v1/users/me` | GET | Lấy thông tin người dùng hiện tại | Đã triển khai |
| `/api/v1/users/me` | PUT | Cập nhật thông tin người dùng hiện tại | Đã triển khai |

## Xác thực (Authentication)

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/auth/login` | POST | Đăng nhập và nhận JWT token | Đã triển khai |
| `/api/v1/auth/logout` | POST | Đăng xuất (vô hiệu hóa token) | Đã triển khai |
| `/api/v1/auth/refresh` | POST | Làm mới JWT token | Đã triển khai |
| `/api/v1/auth/reset-password` | POST | Yêu cầu reset mật khẩu | Cần triển khai |
| `/api/v1/auth/reset-password/{token}` | POST | Reset mật khẩu với token | Cần triển khai |
| `/api/v1/auth/verify-email/{token}` | GET | Xác thực email | Cần triển khai |

## Quản lý vai trò và quyền

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/roles` | GET | Lấy danh sách vai trò | Đã triển khai |
| `/api/v1/roles/{role_id}` | GET | Lấy thông tin chi tiết vai trò | Đã triển khai |
| `/api/v1/roles` | POST | Tạo vai trò mới | Đã triển khai |
| `/api/v1/roles/{role_id}` | PUT | Cập nhật vai trò | Đã triển khai |
| `/api/v1/roles/{role_id}` | DELETE | Xóa vai trò | Đã triển khai |
| `/api/v1/permissions` | GET | Lấy danh sách quyền | Đã triển khai |
| `/api/v1/users/{user_id}/roles` | GET | Lấy vai trò của người dùng | Đã triển khai |
| `/api/v1/users/{user_id}/roles` | POST | Gán vai trò cho người dùng | Đã triển khai |
| `/api/v1/users/{user_id}/roles/{role_id}` | DELETE | Xóa vai trò khỏi người dùng | Đã triển khai |

## Quản lý phòng ban

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/departments` | GET | Lấy danh sách phòng ban | Đã triển khai |
| `/api/v1/departments/{department_id}` | GET | Lấy thông tin chi tiết phòng ban | Đã triển khai |
| `/api/v1/departments` | POST | Tạo phòng ban mới | Đã triển khai |
| `/api/v1/departments/{department_id}` | PUT | Cập nhật phòng ban | Đã triển khai |
| `/api/v1/departments/{department_id}` | DELETE | Xóa phòng ban | Đã triển khai |
| `/api/v1/departments/{department_id}/users` | GET | Lấy danh sách nhân viên trong phòng ban | Đã triển khai |

## Quản lý Dispatcher/Coordinator

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/dispatchers` | GET | Lấy danh sách dispatchers | Đã triển khai |
| `/api/v1/coordinators` | GET | Lấy danh sách coordinators | Đã triển khai |
| `/api/v1/departments/{department_id}/dispatchers` | GET | Lấy danh sách dispatchers của phòng ban | Đã triển khai |
| `/api/v1/departments/{department_id}/dispatchers` | POST | Thêm dispatcher cho phòng ban | Đã triển khai |
| `/api/v1/departments/{department_id}/dispatchers/{user_id}` | DELETE | Xóa dispatcher khỏi phòng ban | Đã triển khai |

## Tích hợp và Hệ thống

| Endpoint | Method | Mô tả | Trạng thái |
|----------|--------|-------|------------|
| `/api/v1/users/validate-token` | POST | Xác thực token (sử dụng bởi API Gateway) | Đã triển khai |
| `/` | GET | Health check | Đã triển khai |
| `/db-check` | GET | Kiểm tra kết nối database | Đã triển khai |
| `/docs` | GET | Swagger API documentation | Đã triển khai |
| `/redoc` | GET | ReDoc API documentation | Đã triển khai |

## Ghi chú

- Các endpoint có trạng thái "Đã triển khai" đã được xác nhận hoạt động trong checklist.
- Các endpoint có trạng thái "Cần triển khai" cần được phát triển dựa trên checklist.
- Tất cả các API endpoint đều yêu cầu xác thực JWT trừ các endpoint đăng nhập, đăng ký và health check.
- Đối với một số endpoint, có thể yêu cầu quyền admin hoặc quyền phù hợp theo vai trò.