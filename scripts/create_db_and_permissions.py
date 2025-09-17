import psycopg2
import psycopg2.extras
import os
import sys
from datetime import datetime

# Permissions from frontend
DEFAULT_PERMISSIONS = [
    # Ticket Permissions
    {
        "id": "ticket:view",
        "name": "View Tickets",
        "description": "Xem danh sách và chi tiết ticket",
        "category": "Ticket"
    },
    {
        "id": "ticket:create",
        "name": "Create Tickets",
        "description": "Tạo ticket mới",
        "category": "Ticket"
    },
    {
        "id": "ticket:update",
        "name": "Update Tickets",
        "description": "Cập nhật thông tin ticket",
        "category": "Ticket"
    },
    {
        "id": "ticket:delete",
        "name": "Delete Tickets",
        "description": "Xóa ticket",
        "category": "Ticket"
    },
    {
        "id": "ticket:assign",
        "name": "Assign Tickets",
        "description": "Phân công ticket cho người dùng khác",
        "category": "Ticket"
    },
    {
        "id": "ticket:comment",
        "name": "Comment on Tickets",
        "description": "Thêm bình luận vào ticket",
        "category": "Ticket"
    },
    {
        "id": "ticket:change-status",
        "name": "Change Ticket Status",
        "description": "Thay đổi trạng thái của ticket",
        "category": "Ticket"
    },
    {
        "id": "ticket:view-all",
        "name": "View All Tickets",
        "description": "Xem tất cả ticket trong hệ thống (không giới hạn bởi phòng ban)",
        "category": "Ticket"
    },
    
    # User Permissions
    {
        "id": "user:view",
        "name": "View Users",
        "description": "Xem danh sách và thông tin người dùng",
        "category": "User"
    },
    {
        "id": "user:create",
        "name": "Create Users",
        "description": "Tạo người dùng mới",
        "category": "User"
    },
    {
        "id": "user:update",
        "name": "Update Users",
        "description": "Cập nhật thông tin người dùng",
        "category": "User"
    },
    {
        "id": "user:delete",
        "name": "Delete Users",
        "description": "Xóa người dùng",
        "category": "User"
    },
    
    # Role Permissions
    {
        "id": "role:view",
        "name": "View Roles",
        "description": "Xem danh sách và chi tiết vai trò",
        "category": "Role"
    },
    {
        "id": "role:create",
        "name": "Create Roles",
        "description": "Tạo vai trò mới",
        "category": "Role"
    },
    {
        "id": "role:update",
        "name": "Update Roles",
        "description": "Cập nhật thông tin vai trò",
        "category": "Role"
    },
    {
        "id": "role:delete",
        "name": "Delete Roles",
        "description": "Xóa vai trò",
        "category": "Role"
    },
    {
        "id": "role:assign",
        "name": "Assign Roles",
        "description": "Gán vai trò cho người dùng",
        "category": "Role"
    },
    
    # Department Permissions
    {
        "id": "department:view",
        "name": "View Departments",
        "description": "Xem danh sách và chi tiết phòng ban",
        "category": "Department"
    },
    {
        "id": "department:create",
        "name": "Create Departments",
        "description": "Tạo phòng ban mới",
        "category": "Department"
    },
    {
        "id": "department:update",
        "name": "Update Departments",
        "description": "Cập nhật thông tin phòng ban",
        "category": "Department"
    },
    {
        "id": "department:delete",
        "name": "Delete Departments",
        "description": "Xóa phòng ban",
        "category": "Department"
    },
    {
        "id": "department:manage-members",
        "name": "Manage Department Members",
        "description": "Thêm/xóa thành viên của phòng ban",
        "category": "Department"
    },
    
    # Dispatcher/Coordinator Permissions
    {
        "id": "dispatcher:assign",
        "name": "Assign as Dispatcher",
        "description": "Chỉ định người dùng làm Dispatcher",
        "category": "Dispatcher"
    },
    {
        "id": "dispatcher:remove",
        "name": "Remove Dispatcher",
        "description": "Xóa vai trò Dispatcher của người dùng",
        "category": "Dispatcher"
    },
    {
        "id": "coordinator:assign",
        "name": "Assign as Coordinator",
        "description": "Chỉ định người dùng làm Coordinator",
        "category": "Coordinator"
    },
    {
        "id": "coordinator:remove",
        "name": "Remove Coordinator",
        "description": "Xóa vai trò Coordinator của người dùng",
        "category": "Coordinator"
    },
    
    # Report Permissions
    {
        "id": "report:view",
        "name": "View Reports",
        "description": "Xem báo cáo",
        "category": "Report"
    },
    {
        "id": "report:create",
        "name": "Create Reports",
        "description": "Tạo báo cáo mới",
        "category": "Report"
    },
    {
        "id": "report:export",
        "name": "Export Reports",
        "description": "Xuất báo cáo ra file",
        "category": "Report"
    },
    
    # Analytics Permissions
    {
        "id": "analytics:view",
        "name": "View Analytics",
        "description": "Xem dữ liệu phân tích",
        "category": "Analytics"
    },
    {
        "id": "analytics:advanced",
        "name": "Advanced Analytics",
        "description": "Sử dụng tính năng phân tích nâng cao",
        "category": "Analytics"
    },
    
    # System Permissions
    {
        "id": "system:settings",
        "name": "Manage System Settings",
        "description": "Quản lý cài đặt hệ thống",
        "category": "System"
    },
    {
        "id": "system:logs",
        "name": "View System Logs",
        "description": "Xem nhật ký hệ thống",
        "category": "System"
    },
    {
        "id": "system:backup",
        "name": "Backup & Restore",
        "description": "Sao lưu và khôi phục dữ liệu",
        "category": "System"
    },
    
    # Project Permissions
    {
        "id": "project:view",
        "name": "View Projects",
        "description": "Xem danh sách và chi tiết dự án",
        "category": "Project"
    },
    {
        "id": "project:create",
        "name": "Create Projects",
        "description": "Tạo dự án mới",
        "category": "Project"
    },
    {
        "id": "project:update",
        "name": "Update Projects",
        "description": "Cập nhật thông tin dự án",
        "category": "Project"
    },
    {
        "id": "project:delete",
        "name": "Delete Projects",
        "description": "Xóa dự án",
        "category": "Project"
    },
    {
        "id": "project:manage-members",
        "name": "Manage Project Members",
        "description": "Thêm/xóa thành viên dự án",
        "category": "Project"
    }
]

def create_ticket_db():
    """
    Create the ticket_db database if it doesn't exist
    """
    print("Checking if ticket_db exists...")
    
    # Get connection parameters
    conn_params = {}
    try:
        # Read from database.env file if exists
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'database.env')
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        conn_params[key] = value
            
            print("Using database connection from config/database.env")
            db_host = conn_params.get('POSTGRES_HOST', 'localhost')
            db_port = conn_params.get('POSTGRES_PORT', '5432')
            db_user = conn_params.get('POSTGRES_USER', 'admin')
            db_password = conn_params.get('POSTGRES_PASSWORD', 'admin')
        else:
            # Default values
            print("No database.env found, using default connection parameters")
            db_host = 'localhost'
            db_port = '5432'
            db_user = 'admin'
            db_password = 'admin'
    except Exception as e:
        print(f"Error reading environment file: {str(e)}")
        # Default values
        db_host = 'localhost'
        db_port = '5432'
        db_user = 'admin'
        db_password = 'admin'
    
    # Get credentials from user input if needed
    if 'y' in input(f"Use connection: {db_user}@{db_host}:{db_port}? (y/n): ").lower():
        pass
    else:
        db_host = input(f"Database host [{db_host}]: ") or db_host
        db_port = input(f"Database port [{db_port}]: ") or db_port
        db_user = input(f"Database user [{db_user}]: ") or db_user
        db_password = input(f"Database password: ") or db_password
    
    try:
        # Connect to PostgreSQL server (default 'postgres' database)
        print(f"Connecting to PostgreSQL server on {db_host}:{db_port}...")
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database="postgres",  # Connect to default database
            user=db_user,
            password=db_password
        )
        conn.autocommit = True  # Set autocommit mode
        
        # Create a cursor
        cur = conn.cursor()
        
        # Check if ticket_db exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'ticket_db'")
        db_exists = cur.fetchone()
        
        if not db_exists:
            print("Database ticket_db does not exist. Creating it...")
            cur.execute("CREATE DATABASE ticket_db")
            print("Database ticket_db created successfully!")
        else:
            print("Database ticket_db already exists.")
        
        # Close connection
        cur.close()
        conn.close()
        
        return True, db_host, db_port, db_user, db_password
        
    except Exception as e:
        print(f"Error creating database: {str(e)}")
        return False, db_host, db_port, db_user, db_password

def migrate_permissions_direct_db(db_host, db_port, db_user, db_password):
    """
    Migrate permissions directly to the database
    """
    print("Migrating permissions to ticket_db database...")
    
    try:
        # Connect to the ticket_db database
        print(f"Connecting to ticket_db database on {db_host}:{db_port}...")
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database="ticket_db",
            user=db_user,
            password=db_password
        )
        
        # Create a cursor
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Check if permissions table exists
        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'permissions')")
        table_exists = cur.fetchone()[0]
        
        if not table_exists:
            print("Permissions table does not exist. Creating table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS permissions (
                    id VARCHAR PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    description VARCHAR,
                    category VARCHAR NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """)
            conn.commit()
        
        # Add permissions
        permissions_added = 0
        permissions_updated = 0
        
        for permission in DEFAULT_PERMISSIONS:
            # Check if permission exists
            cur.execute("SELECT * FROM permissions WHERE id = %s", (permission["id"],))
            exists = cur.fetchone()
            
            now = datetime.now()
            
            if not exists:
                # Create new permission
                cur.execute(
                    """
                    INSERT INTO permissions (id, name, description, category, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        permission["id"],
                        permission["name"],
                        permission.get("description", ""),
                        permission["category"],
                        now
                    )
                )
                permissions_added += 1
                print(f"Created permission: {permission['id']}")
            else:
                # Update existing permission
                cur.execute(
                    """
                    UPDATE permissions
                    SET name = %s, description = %s, category = %s, updated_at = %s
                    WHERE id = %s
                    """,
                    (
                        permission["name"],
                        permission.get("description", ""),
                        permission["category"],
                        now,
                        permission["id"]
                    )
                )
                permissions_updated += 1
                print(f"Updated permission: {permission['id']}")
        
        # Commit the transaction
        conn.commit()
        
        print(f"Migration completed! Added: {permissions_added}, Updated: {permissions_updated}")
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error during database migration: {str(e)}")
        return False

if __name__ == "__main__":
    # First, ensure the ticket_db database exists
    success, db_host, db_port, db_user, db_password = create_ticket_db()
    
    if success:
        # Then migrate permissions
        migrate_permissions_direct_db(db_host, db_port, db_user, db_password)