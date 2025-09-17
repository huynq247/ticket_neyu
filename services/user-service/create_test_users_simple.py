"""
Database Initialization Script for User Service
This script creates test users, roles, and permissions for testing.
"""
import sys
import os
import time

# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.init_db import create_tables
from app.db.session import SessionLocal
from app.models.user import User, Role, Permission
from app.core.security import get_password_hash

def create_test_data():
    """
    Create test users, roles, and permissions
    """
    db = SessionLocal()
    
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
    
    # Create users without department_id
    users = [
        {
            "email": "admin@example.com",
            "username": "admin",
            "password": "admin123",
            "full_name": "Admin User",
            "roles": ["admin"]
        },
        {
            "email": "manager@example.com",
            "username": "manager",
            "password": "manager123",
            "full_name": "Department Manager",
            "roles": ["manager"]
        },
        {
            "email": "agent1@example.com",
            "username": "agent1",
            "password": "agent123",
            "full_name": "Support Agent 1",
            "roles": ["agent"]
        },
        {
            "email": "agent2@example.com",
            "username": "agent2",
            "password": "agent123",
            "full_name": "Support Agent 2",
            "roles": ["agent"]
        },
        {
            "email": "user1@example.com",
            "username": "user1",
            "password": "user123",
            "full_name": "Regular User 1",
            "roles": ["user"]
        },
        {
            "email": "user2@example.com",
            "username": "user2",
            "password": "user123",
            "full_name": "Regular User 2",
            "roles": ["user"]
        }
    ]
    
    for user_data in users:
        user = db.query(User).filter(User.email == user_data["email"]).first()
        if not user:
            # Create new user without department_id
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                hashed_password=get_password_hash(user_data["password"]),
                full_name=user_data["full_name"],
                is_active=True
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