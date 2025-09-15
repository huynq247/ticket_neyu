# Ticket Frontend

Frontend cho hệ thống quản lý ticket sử dụng React, TypeScript và Vite.

## 📋 Mục lục

- [Cài đặt](#cài-đặt)
- [Cấu hình môi trường](#cấu-hình-môi-trường)
- [Phát triển](#phát-triển)
- [Kết nối với Backend](#kết-nối-với-backend)
- [Tính năng](#tính-năng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Tài liệu bổ sung](#tài-liệu-bổ-sung)

## 🚀 Cài đặt

Đảm bảo bạn đã cài đặt [Node.js](https://nodejs.org/) (v14.0.0 hoặc cao hơn) và npm.

```bash
# Clone repository nếu chưa có
git clone <repository-url>

# Di chuyển đến thư mục dự án
cd ticket-frontend

# Cài đặt dependencies
npm install
```

## ⚙️ Cấu hình môi trường

Dự án sử dụng file `.env` để cấu hình các biến môi trường. Bạn có thể tùy chỉnh các cài đặt trong file này.

### Các file cấu hình:

- `.env`: Cấu hình cho môi trường phát triển cục bộ
- `.env.production`: Cấu hình cho môi trường sản xuất
- `.env.example`: File mẫu, sử dụng khi không có file `.env`

### Kiểm tra cấu hình:

Sử dụng script `check_env.bat` để kiểm tra cấu hình hiện tại:

```bash
.\check_env.bat
```

Hoặc sử dụng npm script:

```bash
npm run check-env
```

### Các biến môi trường chính:

| Biến | Mô tả | Giá trị mặc định |
|------|-------|-----------------|
| `VITE_API_BASE_URL` | URL cơ sở của API Gateway | http://localhost:8080 |
| `VITE_DEV_SERVER_PORT` | Cổng của dev server | 3000 |
| `VITE_API_TIMEOUT` | Thời gian timeout cho API calls (ms) | 10000 |
| `VITE_AUTH_STORAGE_KEY` | Khóa lưu trữ token xác thực | auth_token |

## 💻 Phát triển

### Khởi động môi trường phát triển:

```bash
# Khởi động server phát triển
npm run dev
```

### Kiểm tra code:

```bash
# Kiểm tra lỗi
npm run lint

# Tự động sửa lỗi
npm run lint:fix

# Format code
npm run format
```

### Build cho môi trường sản xuất:

```bash
# Build
npm run build

# Xem trước bản build
npm run preview
```

## 🔌 Kết nối với Backend

### Kiểm tra kết nối đến các microservices:

```bash
# Sử dụng PowerShell script
.\check-connections.ps1

# Hoặc sử dụng npm script
npm run check-connections
```

### Chạy toàn bộ hệ thống:

1. Khởi động backend microservices:
   ```bash
   cd D:\NeyuProject
   .\run_local_enhanced.ps1 start
   ```

2. Khởi động frontend:
   ```bash
   cd D:\NeyuProject\ticket-frontend
   npm run dev
   ```

Hoặc sử dụng script tự động:
```bash
cd D:\NeyuProject
.\start_all_enhanced.bat
```

## ✨ Tính năng

- Xác thực người dùng (đăng nhập, đăng ký, quên mật khẩu)
- Quản lý tickets (tạo, xem, cập nhật, xóa)
- Dashboard phân tích dữ liệu
- Thông báo thời gian thực
- Giao diện người dùng thân thiện với Ant Design

## 📁 Cấu trúc dự án

```
ticket-frontend/
├── public/              # Static files
├── src/
│   ├── api/             # API service calls
│   ├── assets/          # Images, fonts, etc.
│   ├── components/      # Reusable components
│   ├── context/         # React contexts
│   ├── hooks/           # Custom hooks
│   ├── pages/           # Page components
│   ├── services/        # Business logic services
│   ├── types/           # TypeScript type definitions
│   ├── utils/           # Utility functions
│   ├── App.tsx          # Main app component
│   └── main.tsx         # Entry point
├── .env                 # Environment variables
├── .env.example         # Example environment file
├── .env.production      # Production environment variables
├── vite.config.ts       # Vite configuration
└── tsconfig.json        # TypeScript configuration
```

## 📚 Tài liệu bổ sung

- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Vite Documentation](https://vitejs.dev/guide/)
- [Ant Design Documentation](https://ant.design/docs/react/introduce)