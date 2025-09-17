import sys
import os
import json
import requests
from datetime import datetime

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Import from user service - adjust path as needed
sys.path.append(os.path.join(parent_dir, 'services', 'user-service'))
from app.db.session import SessionLocal
from app.models.user import Permission

# Default permissions from frontend
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

def migrate_permissions_via_api():
    """
    Migrate permissions via API (good for production or remote environments)
    """
    print("Migrating permissions via API...")
    
    # Get token (need to have a superuser account)
    login_url = "http://localhost:8000/api/v1/auth/login"
    login_data = {
        "username": "admin",  # Change to your superuser username
        "password": "admin"   # Change to your superuser password
    }
    
    try:
        login_response = requests.post(login_url, json=login_data)
        login_response.raise_for_status()
        token = login_response.json().get("access_token")
        
        if not token:
            print("Failed to obtain authentication token.")
            return
            
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Add permissions via API
        permissions_url = "http://localhost:8000/api/v1/permissions"
        
        for permission in DEFAULT_PERMISSIONS:
            try:
                # Check if permission exists
                get_response = requests.get(f"{permissions_url}/{permission['id']}", headers=headers)
                
                if get_response.status_code == 404:
                    # Create permission if it doesn't exist
                    create_response = requests.post(permissions_url, json=permission, headers=headers)
                    
                    if create_response.status_code == 200 or create_response.status_code == 201:
                        print(f"Created permission: {permission['id']}")
                    else:
                        print(f"Failed to create permission {permission['id']}: {create_response.text}")
                else:
                    # Update permission if it exists
                    update_response = requests.put(f"{permissions_url}/{permission['id']}", json=permission, headers=headers)
                    
                    if update_response.status_code == 200:
                        print(f"Updated permission: {permission['id']}")
                    else:
                        print(f"Failed to update permission {permission['id']}: {update_response.text}")
                        
            except Exception as e:
                print(f"Error processing permission {permission['id']}: {str(e)}")
                
        print("API migration completed!")
        
    except Exception as e:
        print(f"Error during API migration: {str(e)}")


def migrate_permissions_direct_db():
    """
    Migrate permissions directly to the database (good for development environments)
    """
    print("Migrating permissions directly to database...")
    
    try:
        db = SessionLocal()
        
        for permission_data in DEFAULT_PERMISSIONS:
            # Check if permission exists
            permission = db.query(Permission).filter(Permission.id == permission_data["id"]).first()
            
            if not permission:
                # Create new permission
                permission = Permission(
                    id=permission_data["id"],
                    name=permission_data["name"],
                    description=permission_data.get("description", ""),
                    category=permission_data["category"]
                )
                db.add(permission)
                print(f"Created permission: {permission_data['id']}")
            else:
                # Update existing permission
                permission.name = permission_data["name"]
                permission.description = permission_data.get("description", "")
                permission.category = permission_data["category"]
                db.add(permission)
                print(f"Updated permission: {permission_data['id']}")
        
        db.commit()
        print("Database migration completed!")
        
    except Exception as e:
        print(f"Error during database migration: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate permissions from frontend to backend")
    parser.add_argument(
        "--method", 
        choices=["api", "db"], 
        default="api", 
        help="Migration method: 'api' to use API calls, 'db' to write directly to database"
    )
    
    args = parser.parse_args()
    
    if args.method == "api":
        migrate_permissions_via_api()
    else:
        migrate_permissions_direct_db()