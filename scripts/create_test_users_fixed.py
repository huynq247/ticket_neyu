"""
Direct Database Initialization Script for User Service
This script creates test users directly in the database based on the actual database structure.
"""
import os
import psycopg2
from psycopg2 import sql
import hashlib
import secrets
import base64

# Database connection settings
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Mypassword123")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "14.161.50.86")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "25432")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "postgres")

# Function to hash a password (using a simple method for this demo)
def hash_password(password):
    """Simple password hashing for demo purposes"""
    salt = secrets.token_bytes(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return base64.b64encode(salt + pwdhash).decode('ascii')

def create_test_data():
    """Create test users directly in the database"""
    # Connect to the database
    conn_string = f"host={POSTGRES_HOST} port={POSTGRES_PORT} dbname={POSTGRES_DATABASE} user={POSTGRES_USER} password={POSTGRES_PASSWORD}"
    
    try:
        # Connect to the database
        print(f"Connecting to database: {conn_string}")
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        print("Connected to database successfully")
        
        # Insert test users with known role values
        users = [
            {
                "email": "admin@example.com",
                "username": "admin",
                "password": "admin123",
                "full_name": "Admin User",
                "role": "TEACHER",  # Based on existing roles in the database
                "is_active": True
            },
            {
                "email": "manager@example.com",
                "username": "manager",
                "password": "manager123",
                "full_name": "Department Manager",
                "role": "TEACHER",
                "is_active": True
            },
            {
                "email": "agent1@example.com",
                "username": "agent1",
                "password": "agent123",
                "full_name": "Support Agent 1",
                "role": "TEACHER",
                "is_active": True
            },
            {
                "email": "user1@example.com",
                "username": "user1",
                "password": "user123",
                "full_name": "Regular User 1",
                "role": "STUDENT",
                "is_active": True
            },
            {
                "email": "user2@example.com",
                "username": "user2",
                "password": "user123",
                "full_name": "Regular User 2",
                "role": "STUDENT",
                "is_active": True
            }
        ]
        
        for user_data in users:
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (user_data["email"],))
            result = cursor.fetchone()
            
            if result:
                user_id = result[0]
                print(f"User already exists: {user_data['username']}")
            else:
                # Create new user with the appropriate role
                cursor.execute(
                    "INSERT INTO users (email, username, hashed_password, full_name, role, is_active) VALUES (%s, %s, %s, %s, %s::userrole, %s) RETURNING id",
                    (
                        user_data["email"], 
                        user_data["username"], 
                        hash_password(user_data["password"]), 
                        user_data["full_name"],
                        user_data["role"],
                        user_data["is_active"]
                    )
                )
                user_id = cursor.fetchone()[0]
                print(f"Created user: {user_data['username']} with role: {user_data['role']}")
        
        conn.commit()
        print("Test data initialization completed successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_test_data()