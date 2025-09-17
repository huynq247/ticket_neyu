"""
Script to test MongoDB connection
"""

from pymongo import MongoClient
import sys

# Thông tin kết nối MongoDB từ database.env
uri = "mongodb://admin:Mypassword123@14.161.50.86:27017/content_db?authSource=admin"

try:
    # Tạo kết nối
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    
    # Kiểm tra kết nối bằng cách lấy thông tin server
    server_info = client.server_info()
    
    print("Kết nối MongoDB thành công!")
    print(f"Server info: {server_info}")
    
    # Liệt kê các database
    print("\nDanh sách databases:")
    for db_name in client.list_database_names():
        print(f" - {db_name}")
    
except Exception as e:
    print(f"Lỗi kết nối MongoDB: {e}")
    sys.exit(1)
finally:
    # Đóng kết nối
    if 'client' in locals():
        client.close()