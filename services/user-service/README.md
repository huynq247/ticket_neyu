# User Service

Service này chịu trách nhiệm quản lý thông tin người dùng, xác thực và phân quyền.

## Chức năng chính

- Quản lý thông tin người dùng (CRUD)
- Xác thực (authentication)
- Phân quyền (authorization)
- Quản lý vai trò và phòng ban
- Quản lý người phân chia tickets (Dispatcher/Coordinator)

## Cơ sở dữ liệu

- PostgreSQL

## Công nghệ

- Python (FastAPI)
- SQLAlchemy ORM
- JWT Authentication
- Bcrypt (mã hóa mật khẩu)

## Cài đặt và Chạy

### Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Thiết lập biến môi trường

Sử dụng các biến môi trường từ `database.env` trong thư mục `config`:

- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_HOST
- POSTGRES_PORT
- POSTGRES_DATABASE

### Khởi tạo cơ sở dữ liệu

```bash
python -m app.db.init_db
```

### Chạy ứng dụng

```bash
uvicorn main:app --reload
```

Truy cập API tại http://localhost:8000

## API Endpoints

### Authentication

- `POST /api/v1/auth/login` - Đăng nhập và lấy token
- `POST /api/v1/auth/refresh` - Làm mới token

### Users

- `GET /api/v1/users/` - Lấy danh sách người dùng
- `POST /api/v1/users/` - Tạo người dùng mới
- `GET /api/v1/users/me` - Lấy thông tin người dùng hiện tại
- `PUT /api/v1/users/me` - Cập nhật thông tin người dùng hiện tại
- `GET /api/v1/users/{user_id}` - Lấy thông tin người dùng theo ID
- `PUT /api/v1/users/{user_id}` - Cập nhật thông tin người dùng theo ID

### Roles

- `GET /api/v1/roles/` - Lấy danh sách vai trò
- `POST /api/v1/roles/` - Tạo vai trò mới
- `GET /api/v1/roles/{role_id}` - Lấy thông tin vai trò theo ID
- `PUT /api/v1/roles/{role_id}` - Cập nhật thông tin vai trò theo ID
- `DELETE /api/v1/roles/{role_id}` - Xóa vai trò

### Departments

- `GET /api/v1/departments/` - Lấy danh sách phòng ban
- `POST /api/v1/departments/` - Tạo phòng ban mới
- `GET /api/v1/departments/{department_id}` - Lấy thông tin phòng ban theo ID
- `PUT /api/v1/departments/{department_id}` - Cập nhật thông tin phòng ban theo ID
- `DELETE /api/v1/departments/{department_id}` - Xóa phòng ban

## Documentation

API documentation có sẵn tại http://localhost:8000/docs sau khi chạy ứng dụng.