# Git Branching Strategy

Dự án sử dụng chiến lược phân nhánh Gitflow với các nhánh chính như sau:

## Các nhánh chính

- `main`: Nhánh chính, chứa code sản phẩm đã sẵn sàng triển khai
- `develop`: Nhánh phát triển, tích hợp các tính năng đã hoàn thành

## Các nhánh phụ

- `feature/[feature-name]`: Nhánh phát triển tính năng mới
- `bugfix/[bug-name]`: Nhánh sửa lỗi
- `hotfix/[hotfix-name]`: Nhánh sửa lỗi khẩn cấp trên production
- `release/[version]`: Nhánh chuẩn bị phát hành

## Quy trình làm việc

1. **Phát triển tính năng mới**:
   - Tạo nhánh `feature/[feature-name]` từ `develop`
   - Hoàn thành phát triển tính năng
   - Tạo Pull Request vào `develop`
   - Sau khi review, merge vào `develop`

2. **Sửa lỗi**:
   - Tạo nhánh `bugfix/[bug-name]` từ `develop`
   - Sửa lỗi
   - Tạo Pull Request vào `develop`
   - Sau khi review, merge vào `develop`

3. **Phát hành**:
   - Tạo nhánh `release/[version]` từ `develop`
   - Sửa các lỗi cuối cùng
   - Merge vào cả `main` và `develop`
   - Tag version trên `main`

4. **Hotfix**:
   - Tạo nhánh `hotfix/[hotfix-name]` từ `main`
   - Sửa lỗi khẩn cấp
   - Merge vào cả `main` và `develop`
   - Tag version mới trên `main`

## Quy ước đặt tên commit

- feat: Tính năng mới
- fix: Sửa lỗi
- docs: Thay đổi tài liệu
- style: Thay đổi không ảnh hưởng đến code (formatting, etc)
- refactor: Tái cấu trúc code
- test: Thêm hoặc sửa tests
- chore: Các thay đổi khác (build process, etc)

Ví dụ: `feat: Thêm tính năng đăng nhập qua Telegram`