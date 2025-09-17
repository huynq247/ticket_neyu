"""
Database Initialization Script for User Service
This script creates test users, roles, departments and permissions for testing.
"""
import sys
import os
import time

# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.init_db import create_tables
from app.db.session import SessionLocal
from app.models.user import User, Role, Department, Permission
from app.core.security import get_password_hash

def create_test_data():
    """
    Create test users, roles, departments and permissions
    """
    db = SessionLocal()
    
    # Create departments
    departments = [
        {"name": "IT", "description": "Information Technology Department"},
        {"name": "HR", "description": "Human Resources Department"},
        {"name": "Finance", "description": "Finance Department"},
        {"name": "Marketing", "description": "Marketing Department"},
        {"name": "Sales", "description": "Sales Department"},
        {"name": "Customer Support", "description": "Customer Support Department"}
    ]
    
    department_objects = {}
    for dept_data in departments:
        dept = db.query(Department).filter(Department.name == dept_data["name"]).first()
        if not dept:
            dept = Department(**dept_data)
            db.add(dept)
            db.commit()
            db.refresh(dept)
            print(f"Created department: {dept.name}")
        department_objects[dept.name] = dept
    
    # Create roles
    roles = [
        {"name": "admin", "description": "Administrator with all privileges"},
        {"name": "manager", "description": "Department manager with elevated privileges"},
        {"name": "agent", "description": "Support agent with ticket management capabilities"},
        {"name": "user", "description": "Regular user who can submit tickets"}
    ]
    
    role_objects = {}
    for role_data in roles:
        role = db.query(Role).filter(Role.name == role_data["name"]).first()
        if not role:
            role = Role(**role_data)
            db.add(role)
            db.commit()
            db.refresh(role)
            print(f"Created role: {role.name}")
        role_objects[role.name] = role
    
    # Create permissions
    permissions = [
        {"name": "create_ticket", "description": "Can create tickets", "role_id": role_objects["user"].id},
        {"name": "view_ticket", "description": "Can view tickets", "role_id": role_objects["user"].id},
        {"name": "update_ticket", "description": "Can update tickets", "role_id": role_objects["agent"].id},
        {"name": "delete_ticket", "description": "Can delete tickets", "role_id": role_objects["manager"].id},
        {"name": "assign_ticket", "description": "Can assign tickets", "role_id": role_objects["manager"].id},
        {"name": "manage_users", "description": "Can manage users", "role_id": role_objects["admin"].id},
        {"name": "view_reports", "description": "Can view reports", "role_id": role_objects["manager"].id},
        {"name": "manage_settings", "description": "Can manage system settings", "role_id": role_objects["admin"].id}
    ]
    
    for perm_data in permissions:
        perm = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
        if not perm:
            perm = Permission(**perm_data)
            db.add(perm)
            db.commit()
            db.refresh(perm)
            print(f"Created permission: {perm.name}")
    
    # Create users
    users = [
        {
            "email": "admin@example.com",
            "username": "admin",
            "password": "admin123",
            "full_name": "Admin User",
            "department": "IT",
            "roles": ["admin"]
        },
        {
            "email": "manager@example.com",
            "username": "manager",
            "password": "manager123",
            "full_name": "Department Manager",
            "department": "IT",
            "roles": ["manager"]
        },
        {
            "email": "agent1@example.com",
            "username": "agent1",
            "password": "agent123",
            "full_name": "Support Agent 1",
            "department": "Customer Support",
            "roles": ["agent"]
        },
        {
            "email": "agent2@example.com",
            "username": "agent2",
            "password": "agent123",
            "full_name": "Support Agent 2",
            "department": "Customer Support",
            "roles": ["agent"]
        },
        {
            "email": "user1@example.com",
            "username": "user1",
            "password": "user123",
            "full_name": "Regular User 1",
            "department": "Finance",
            "roles": ["user"]
        },
        {
            "email": "user2@example.com",
            "username": "user2",
            "password": "user123",
            "full_name": "Regular User 2",
            "department": "Marketing",
            "roles": ["user"]
        },
        {
            "email": "hrmanager@example.com",
            "username": "hrmanager",
            "password": "hr123",
            "full_name": "HR Manager",
            "department": "HR",
            "roles": ["manager"]
        },
        {
            "email": "salesrep@example.com",
            "username": "salesrep",
            "password": "sales123",
            "full_name": "Sales Representative",
            "department": "Sales",
            "roles": ["user"]
        }
    ]
    
    for user_data in users:
        user = db.query(User).filter(User.email == user_data["email"]).first()
        if not user:
            # Create new user
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                hashed_password=get_password_hash(user_data["password"]),
                full_name=user_data["full_name"],
                is_active=True,
                department_id=department_objects[user_data["department"]].id
            )
            
            # Add roles
            for role_name in user_data["roles"]:
                user.roles.append(role_objects[role_name])
                
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created user: {user.username} with roles: {', '.join(user_data['roles'])}")
        else:
            print(f"User already exists: {user.username}")
    
    db.close()
    print("Test data initialization completed.")

if __name__ == "__main__":
    print("Creating database tables...")
    create_tables()
    
    print("Creating test data...")
    create_test_data()
    
    print("Database initialization completed successfully!")