import sys
import os
import requests
import json

# Thông tin API
API_URL = "http://localhost:8000"  # URL của User Service
LOGIN_ENDPOINT = "/api/auth/login"
ROLES_ENDPOINT = "/api/roles"

# Thông tin đăng nhập admin
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Các quyền cần thêm
ADMIN_PERMISSIONS = [
    "analytics:view", 
    "analytics:advanced",
    "ticket:view", 
    "ticket:create", 
    "ticket:update", 
    "ticket:delete", 
    "ticket:assign", 
    "ticket:comment", 
    "ticket:change-status", 
    "ticket:view-all"
]

MANAGER_PERMISSIONS = [
    "analytics:view",
    "ticket:view", 
    "ticket:create", 
    "ticket:update", 
    "ticket:assign", 
    "ticket:comment", 
    "ticket:change-status", 
    "ticket:view-all"
]

def login():
    """Đăng nhập và lấy token"""
    try:
        response = requests.post(
            f"{API_URL}{LOGIN_ENDPOINT}",
            data={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        )
        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            print("Lỗi: Không lấy được token")
            sys.exit(1)
        return token
    except Exception as e:
        print(f"Lỗi đăng nhập: {str(e)}")
        sys.exit(1)

def get_roles(token):
    """Lấy danh sách các vai trò"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}{ROLES_ENDPOINT}", headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Lỗi lấy danh sách vai trò: {str(e)}")
        sys.exit(1)

def update_role_permissions(token, role_id, permissions):
    """Cập nhật quyền cho vai trò"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        # Lấy thông tin vai trò hiện tại
        response = requests.get(f"{API_URL}{ROLES_ENDPOINT}/{role_id}", headers=headers)
        response.raise_for_status()
        role_data = response.json()
        
        # Lấy danh sách quyền hiện tại
        current_permissions = role_data.get("permissions", [])
        
        # Chuyển các quyền hiện tại thành một tập hợp ID
        current_permission_ids = set()
        for perm in current_permissions:
            if isinstance(perm, dict):
                current_permission_ids.add(perm.get("id"))
            elif isinstance(perm, str):
                current_permission_ids.add(perm)
        
        # Thêm các quyền mới vào tập hợp
        all_permissions = current_permission_ids.union(set(permissions))
        
        # Cập nhật vai trò với danh sách quyền mới
        update_data = {
            "name": role_data.get("name"),
            "description": role_data.get("description"),
            "permissions": list(all_permissions)
        }
        
        response = requests.put(
            f"{API_URL}{ROLES_ENDPOINT}/{role_id}",
            headers=headers,
            json=update_data
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Lỗi cập nhật quyền cho vai trò: {str(e)}")
        return None

def main():
    print("Bắt đầu cập nhật quyền cho các vai trò...")
    
    # Đăng nhập
    token = login()
    print("Đăng nhập thành công!")
    
    # Lấy danh sách vai trò
    roles = get_roles(token)
    
    # Tìm vai trò admin và manager
    admin_role = next((role for role in roles if role.get("name") == "admin"), None)
    manager_role = next((role for role in roles if role.get("name") == "manager"), None)
    
    if admin_role:
        print(f"Cập nhật quyền cho vai trò admin (ID: {admin_role.get('id')})...")
        result = update_role_permissions(token, admin_role.get("id"), ADMIN_PERMISSIONS)
        if result:
            print("Cập nhật quyền cho admin thành công!")
    else:
        print("Không tìm thấy vai trò admin!")
    
    if manager_role:
        print(f"Cập nhật quyền cho vai trò manager (ID: {manager_role.get('id')})...")
        result = update_role_permissions(token, manager_role.get("id"), MANAGER_PERMISSIONS)
        if result:
            print("Cập nhật quyền cho manager thành công!")
    else:
        print("Không tìm thấy vai trò manager!")
    
    print("Hoàn thành cập nhật quyền!")

if __name__ == "__main__":
    main()