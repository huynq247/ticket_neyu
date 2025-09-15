# Cấu hình Dự án

Thư mục này chứa các file cấu hình cho dự án Ticket Management System.

## Database Configuration

File `database.env.example` là mẫu cho cấu hình kết nối database. Để sử dụng:

1. Sao chép file mẫu:
   ```
   cp database.env.example database.env
   ```

2. Chỉnh sửa file `database.env` với thông tin kết nối thực tế:
   ```
   # MongoDB Configuration
   MONGODB_URI=mongodb://your-mongodb-host:27017/your-database
   MONGODB_USER=your-username
   MONGODB_PASSWORD=your-password
   MONGODB_DATABASE=your-database
   MONGODB_AUTH_SOURCE=admin

   # PostgreSQL Configuration
   POSTGRES_URI=postgresql://your-postgres-host:5432/your-database
   POSTGRES_USER=your-username
   POSTGRES_PASSWORD=your-password
   POSTGRES_DATABASE=your-database

   # Redis Configuration
   REDIS_URI=redis://your-redis-host:6379/0
   REDIS_PASSWORD=your-redis-password
   ```

3. Không commit file `database.env` vào Git repository vì nó chứa thông tin nhạy cảm.

## Sử dụng trong Code

Để sử dụng cấu hình database trong code:

```python
from config.database import get_mongodb_database, get_sqlalchemy_session_maker, get_redis_client

# Kết nối MongoDB
mongo_db = get_mongodb_database()
tickets_collection = mongo_db["tickets"]

# Kết nối PostgreSQL với SQLAlchemy
SessionLocal = get_sqlalchemy_session_maker()
db = SessionLocal()

# Kết nối Redis
redis_client = get_redis_client()
```

## Kiểm tra kết nối

Bạn có thể kiểm tra kết nối đến tất cả databases bằng cách chạy:

```bash
python config/database.py
```

Lệnh này sẽ hiển thị trạng thái kết nối đến từng database.