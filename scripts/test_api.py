import requests
import json

# Base URL for the API
base_url = "http://localhost:8000/api/v1"

def login():
    """Login and get access token"""
    login_url = f"{base_url}/auth/login/email"
    
    # Sử dụng endpoint mới chấp nhận email và password
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    # Gửi dữ liệu dưới dạng JSON
    response = requests.post(login_url, json=login_data)
    
    if response.status_code != 200:
        print(f"Login failed with status code {response.status_code}")
        print(f"Response: {response.text}")
        return None
    
    token_data = response.json()
    return token_data["access_token"]

def get_permissions(token):
    """Get permissions with token"""
    permissions_url = f"{base_url}/permissions/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(permissions_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to get permissions with status code {response.status_code}")
        print(f"Response: {response.text}")
        return None
    
    return response.json()

if __name__ == "__main__":
    # Login to get token
    print("Logging in...")
    token = login()
    
    if token:
        print("Login successful!")
        print(f"Token: {token}")
        
        # Get permissions
        print("\nGetting permissions...")
        permissions = get_permissions(token)
        
        if permissions:
            print(f"Found {len(permissions)} permissions:")
            for perm in permissions:
                print(f"- {perm['id']}: {perm['name']} ({perm['category']})")
        else:
            print("Failed to get permissions.")
    else:
        print("Login failed.")