# Checklist Thu thập Yêu cầu cho Dự án Quản lý Ticket

## 1. Thông tin cơ bản về dự án
- [x] Mục đích chính của hệ thống (hỗ trợ khách hàng, IT helpdesk, quản lý nội bộ...)? -> IT helpdesk, quản lý nội bộ, 
- [x] Quy mô dự kiến (số lượng người dùng, số lượng ticket hàng ngày/tháng), khoảng 100-200 users. 
- [x] Thời gian dự kiến triển khai -> 1 tháng.
- [ ] Ngân sách (nếu có)

## 2. Đối tượng người dùng
- [x] Các nhóm người dùng (khách hàng, nhân viên hỗ trợ, quản trị viên...) -> nhân viên các phòng ban gửi request về lỗi của các ứng dụng mà nhân viên phòng ban đó đang sử dụng, có nhiều kiểu users, có authe, author users.
- [x] Vai trò và quyền hạn của từng nhóm người dùng
-> các nhóm users có line manager của nhóm đó, sẽ thấy được hết các tickets mà thành viên nhóm đã tạo. Còn users tạo ra tickets sẽ view được tickets và trạng thái tickets, Và user tiếp nhận tickets sẽ tiếp nhận tickets, xử lý và set trạng thái.
- [ ] Yêu cầu đặc biệt về trải nghiệm người dùng (UX/UI)

## 3. Quy trình xử lý ticket
- [x] Các bước trong quy trình xử lý ticket
- [x] Các trạng thái của ticket: Mới (New), Đã tiếp nhận (Acknowledged), Đang xử lý (In Progress), Chờ phản hồi (Waiting for Response), Đã giải quyết (Resolved), Đóng (Closed), Mở lại (Reopened)
- [x] Quy trình phân công và chuyển giao ticket -> Phân công tự động dựa trên loại vấn đề và kỹ năng của nhân viên hỗ trợ
- [x] Quy trình báo cáo và đánh giá

## 4. Tính năng quản lý ticket
- [x] Tạo ticket (thông tin cần thu thập khi tạo ticket)
- [x] Phân loại ticket (theo loại vấn đề, mức độ ưu tiên...)
- [x] Tìm kiếm và lọc ticket
- [x] Cập nhật và theo dõi tiến độ
- [x] Đính kèm tệp và tài liệu
- [x] Ghi chú và bình luận
- [x] Đóng ticket và đánh giá mức độ hài lòng

## 5. Tính năng người dùng và xác thực
- [x] Đăng ký và đăng nhập
- [x] Quản lý hồ sơ người dùng
- [x] Phân quyền và vai trò
- [x] Tích hợp với Telegram: Cho phép user sau khi xác thực (nhập account/password) có thể tạo và quản lý ticket trực tiếp trên Telegram

## 6. Thông báo và cảnh báo
- [x] Loại thông báo (email, SMS, push notification...)
- [x] Điều kiện kích hoạt thông báo
- [x] Tùy chỉnh thông báo theo người dùng
- [x] Nhắc nhở thời hạn xử lý

## 7. Báo cáo và thống kê
- [x] Các loại báo cáo cần thiết
- [x] Chỉ số hiệu suất (KPI) cần theo dõi
- [x] Bảng điều khiển (dashboard) và trực quan hóa dữ liệu
- [x] Xuất báo cáo (PDF, Excel...)

## 8. Tích hợp hệ thống
- [x] Tích hợp với email
- [x] Tích hợp với các công cụ chat -> Telegram

## 9. Yêu cầu kỹ thuật
- [x] Công nghệ backend ưa thích -> Python
- [x] Công nghệ frontend ưa thích -> ReactJS
- [x] Cơ sở dữ liệu -> MongoDB cho quản lý tickets, PostgreSQL cho quản lý users
- [x] Yêu cầu về hiệu suất và khả năng mở rộng -> Kiến trúc microservices để dễ dàng mở rộng từng thành phần riêng biệt
- [x] Môi trường triển khai (cloud, on-premise...) -> trước là on-premise, sau đó sẽ triển khai cloud.

## 10. Yêu cầu bảo trì và hỗ trợ
- [x] Yêu cầu về sao lưu và khôi phục dữ liệu
- [x] Tài liệu hướng dẫn sử dụng
- [x] Đào tạo người dùng