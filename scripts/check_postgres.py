import psycopg2
import time

# Thông tin kết nối
host = "14.161.50.86"
port = "25432"
dbname = "postgres"
user = "admin"
password = "Mypassword123"

# Thử kết nối với timeout
print(f"Đang thử kết nối đến PostgreSQL tại {host}:{port}...")
print(f"Database: {dbname}")
print(f"Username: {user}")
print(f"Password: {password}")

try:
    # Đặt timeout ngắn hơn (5 giây)
    connect_timeout = 5
    
    # Thử kết nối
    start_time = time.time()
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        connect_timeout=connect_timeout
    )
    end_time = time.time()
    
    # Nếu kết nối thành công
    print(f"Kết nối thành công! (Thời gian: {end_time - start_time:.2f} giây)")
    
    # Kiểm tra phiên bản PostgreSQL
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    print(f"PostgreSQL version: {version}")
    
    # Liệt kê các schema
    cur.execute("SELECT schema_name FROM information_schema.schemata;")
    schemas = cur.fetchall()
    print("Schemas:")
    for schema in schemas:
        print(f"  - {schema[0]}")
    
    # Liệt kê các bảng trong schema public
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cur.fetchall()
    print("Bảng trong schema public:")
    if tables:
        for table in tables:
            print(f"  - {table[0]}")
    else:
        print("  Không có bảng nào trong schema public")
    
    # Đóng kết nối
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"Lỗi kết nối: {str(e)}")
    
    # Phân tích lỗi
    if "timeout" in str(e).lower():
        print("\nGợi ý khắc phục:")
        print("1. Kiểm tra xem server PostgreSQL có đang chạy không")
        print("2. Kiểm tra cấu hình firewall, đảm bảo port 25432 được mở")
        print("3. Kiểm tra file pg_hba.conf của PostgreSQL, đảm bảo cho phép kết nối từ IP của bạn")
        print("4. Kiểm tra cấu hình postgresql.conf, đảm bảo listen_addresses bao gồm '*' hoặc địa chỉ IP của server")
    elif "password authentication" in str(e).lower():
        print("\nGợi ý khắc phục:")
        print("1. Kiểm tra lại username và password")
        print("2. Kiểm tra quyền của user")
    elif "does not exist" in str(e).lower():
        print("\nGợi ý khắc phục:")
        print("1. Kiểm tra lại tên database")
        print("2. Kiểm tra xem user có quyền truy cập database này không")