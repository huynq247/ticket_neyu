# Hướng dẫn sử dụng các file bat để chạy microservices

Các file bat này được tạo ra để giúp bạn dễ dàng chạy từng microservice riêng biệt trong môi trường CMD.

## Thứ tự khuyến nghị để chạy các services:

1. `run_user_service.bat` - Chạy User Service (Port 8000)
2. `run_ticket_service.bat` - Chạy Ticket Service (Port 8001)
3. `run_file_service.bat` - Chạy File Service (Port 8002)
4. `run_notification_service.bat` - Chạy Notification Service (Port 8003)
5. `run_report_service.bat` - Chạy Report Service (Port 8004)
6. `run_analytics_service.bat` - Chạy Analytics Service (Port 8005)
7. `run_api_gateway.bat` - Chạy API Gateway (Port 8080)
8. `run_frontend.bat` - Chạy Frontend (Vite development server)

## Cách sử dụng:

1. Mở nhiều cửa sổ CMD riêng biệt (mỗi service một cửa sổ)
2. Trong mỗi cửa sổ, điều hướng đến thư mục run_scripts:
   ```
   cd D:\NeyuProject\run_scripts
   ```
3. Chạy file bat tương ứng, ví dụ:
   ```
   run_user_service.bat
   ```
4. Đợi mỗi service khởi động hoàn tất trước khi chạy service tiếp theo

## Kiểm tra kết nối:

Sau khi chạy tất cả các services, bạn có thể kiểm tra:

- API Gateway: http://localhost:8080/api/health
- Swagger UI của các services:
  - User Service: http://localhost:8000/docs
  - Ticket Service: http://localhost:8001/docs
  - File Service: http://localhost:8002/docs
  - Notification Service: http://localhost:8003/docs
  - Report Service: http://localhost:8004/docs
  - Analytics Service: http://localhost:8005/docs
- Frontend: http://localhost:5173 (hoặc port được hiển thị trong terminal)

## Lưu ý:

- Mỗi service cần một cửa sổ CMD riêng biệt
- Nếu bạn đóng một terminal, service chạy trong terminal đó sẽ bị dừng
- Đảm bảo các ports không bị chiếm bởi các ứng dụng khác