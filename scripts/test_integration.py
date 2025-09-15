import requests
import json
import os
import sys
from datetime import datetime

# Cấu hình
API_GATEWAY_URL = "http://localhost:3000"
USER_SERVICE_URL = "http://localhost:8000"
TICKET_SERVICE_URL = "http://localhost:8001"

# Màu sắc cho terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 50}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(50)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 50}{Colors.ENDC}")

def print_result(test_name, status, message=""):
    if status:
        print(f"{Colors.OKGREEN}[✓] {test_name}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}[✗] {test_name}{Colors.ENDC}")
    if message:
        print(f"   {message}")

def test_service_status():
    print_header("KIỂM TRA TRẠNG THÁI SERVICES")
    
    # Kiểm tra User Service
    try:
        response = requests.get(f"{USER_SERVICE_URL}/api/v1/health", timeout=5)
        print_result("User Service", response.status_code == 200, f"Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_result("User Service", False, f"Error: {str(e)}")
    
    # Kiểm tra Ticket Service
    try:
        response = requests.get(f"{TICKET_SERVICE_URL}/api/v1/health", timeout=5)
        print_result("Ticket Service", response.status_code == 200, f"Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_result("Ticket Service", False, f"Error: {str(e)}")
    
    # Kiểm tra API Gateway
    try:
        response = requests.get(f"{API_GATEWAY_URL}/health", timeout=5)
        print_result("API Gateway", response.status_code == 200, f"Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_result("API Gateway", False, f"Error: {str(e)}")

def test_authentication():
    print_header("KIỂM TRA ĐĂNG NHẬP")
    
    # Thông tin đăng nhập mẫu
    login_data = {
        "username": "admin@example.com",
        "password": "admin123"
    }
    
    # Thử đăng nhập trực tiếp vào User Service
    try:
        response = requests.post(f"{USER_SERVICE_URL}/api/v1/auth/login", json=login_data, timeout=5)
        user_service_auth = response.status_code == 200
        user_service_token = response.json().get("access_token") if user_service_auth else None
        print_result("User Service Login", user_service_auth, 
                    f"Status: {response.status_code}" + (", Token received" if user_service_auth else ""))
    except requests.exceptions.RequestException as e:
        print_result("User Service Login", False, f"Error: {str(e)}")
        user_service_token = None
    
    # Thử đăng nhập qua API Gateway
    try:
        response = requests.post(f"{API_GATEWAY_URL}/api/auth/login", json=login_data, timeout=5)
        gateway_auth = response.status_code == 200
        gateway_token = response.json().get("access_token") if gateway_auth else None
        print_result("API Gateway Login", gateway_auth, 
                    f"Status: {response.status_code}" + (", Token received" if gateway_auth else ""))
    except requests.exceptions.RequestException as e:
        print_result("API Gateway Login", False, f"Error: {str(e)}")
        gateway_token = None
    
    return user_service_token, gateway_token

def test_user_management(token):
    print_header("KIỂM TRA QUẢN LÝ NGƯỜI DÙNG")
    
    if not token:
        print_result("User Management Tests", False, "Không có token đăng nhập")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Lấy danh sách người dùng
    try:
        response = requests.get(f"{API_GATEWAY_URL}/api/users", headers=headers, timeout=5)
        print_result("Get Users List", response.status_code == 200, 
                    f"Status: {response.status_code}, Users: {len(response.json()) if response.status_code == 200 else 0}")
    except requests.exceptions.RequestException as e:
        print_result("Get Users List", False, f"Error: {str(e)}")
    
    # Lấy thông tin người dùng hiện tại
    try:
        response = requests.get(f"{API_GATEWAY_URL}/api/users/me", headers=headers, timeout=5)
        print_result("Get Current User", response.status_code == 200, 
                    f"Status: {response.status_code}" + (f", User: {response.json().get('email')}" if response.status_code == 200 else ""))
    except requests.exceptions.RequestException as e:
        print_result("Get Current User", False, f"Error: {str(e)}")

def test_ticket_management(token):
    print_header("KIỂM TRA QUẢN LÝ TICKET")
    
    if not token:
        print_result("Ticket Management Tests", False, "Không có token đăng nhập")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Lấy danh sách ticket
    try:
        response = requests.get(f"{API_GATEWAY_URL}/api/tickets", headers=headers, timeout=5)
        print_result("Get Tickets List", response.status_code == 200, 
                    f"Status: {response.status_code}, Tickets: {len(response.json()) if response.status_code == 200 else 0}")
    except requests.exceptions.RequestException as e:
        print_result("Get Tickets List", False, f"Error: {str(e)}")
    
    # Tạo ticket mới
    new_ticket = {
        "title": f"Test Ticket {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "description": "This is a test ticket created by the integration test script",
        "priority": "medium",
        "status": "open",
        "category_id": "1"  # Giả định có category với ID=1
    }
    
    try:
        response = requests.post(f"{API_GATEWAY_URL}/api/tickets", headers=headers, json=new_ticket, timeout=5)
        ticket_created = response.status_code == 201 or response.status_code == 200
        ticket_id = response.json().get("id") if ticket_created else None
        print_result("Create New Ticket", ticket_created, 
                    f"Status: {response.status_code}" + (f", Ticket ID: {ticket_id}" if ticket_created else ""))
    except requests.exceptions.RequestException as e:
        print_result("Create New Ticket", False, f"Error: {str(e)}")
        ticket_id = None
    
    # Lấy chi tiết ticket nếu tạo thành công
    if ticket_id:
        try:
            response = requests.get(f"{API_GATEWAY_URL}/api/tickets/{ticket_id}", headers=headers, timeout=5)
            print_result("Get Ticket Details", response.status_code == 200, 
                        f"Status: {response.status_code}, Title: {response.json().get('title') if response.status_code == 200 else 'N/A'}")
        except requests.exceptions.RequestException as e:
            print_result("Get Ticket Details", False, f"Error: {str(e)}")

def main():
    print_header("KIỂM TRA TÍCH HỢP MICROSERVICES")
    print(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Gateway: {API_GATEWAY_URL}")
    print(f"User Service: {USER_SERVICE_URL}")
    print(f"Ticket Service: {TICKET_SERVICE_URL}")
    print("")
    
    # Kiểm tra trạng thái các service
    test_service_status()
    
    # Kiểm tra đăng nhập
    user_token, gateway_token = test_authentication()
    
    # Sử dụng token từ API Gateway nếu có, nếu không thì dùng token từ User Service
    token = gateway_token or user_token
    
    # Kiểm tra quản lý người dùng
    test_user_management(token)
    
    # Kiểm tra quản lý ticket
    test_ticket_management(token)
    
    print_header("KẾT THÚC KIỂM TRA")

if __name__ == "__main__":
    main()