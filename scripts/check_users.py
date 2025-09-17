import psycopg2
from psycopg2.extras import RealDictCursor
import os
import sys

def check_users_in_database():
    """
    Kiểm tra dữ liệu users trong database
    """
    try:
        # Kết nối đến PostgreSQL database
        conn = psycopg2.connect(
            host="14.161.50.86",
            port="25432",
            database="postgres",
            user="admin",
            password="Mypassword123"
        )
        
        # Tạo cursor để thực thi các truy vấn
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Kiểm tra nếu database ticket_db tồn tại
        cursor.execute("SELECT datname FROM pg_database WHERE datname = 'ticket_db'")
        if cursor.fetchone() is None:
            print("Database ticket_db không tồn tại.")
            return
        
        # Đóng kết nối hiện tại và kết nối đến database ticket_db
        conn.close()
        conn = psycopg2.connect(
            host="14.161.50.86",
            port="25432",
            database="ticket_db",
            user="admin",
            password="Mypassword123"
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Kiểm tra bảng users
        cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_name = 'users'
        """)
        
        if cursor.fetchone() is None:
            print("Bảng users không tồn tại.")
            return
        
        # Lấy danh sách users
        cursor.execute("SELECT id, email, username, full_name, is_active FROM users")
        users = cursor.fetchall()
        
        if not users:
            print("Không có user nào trong database.")
        else:
            print(f"Tìm thấy {len(users)} user trong database:")
            for user in users:
                print(f"ID: {user['id']}, Email: {user['email']}, Username: {user['username']}, " 
                      f"Full name: {user['full_name']}, Active: {user['is_active']}")
        
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_users_in_database()