"""
Direct Database Initialization Script for User Service
This script creates test users directly in the database without using ORM models.
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

# Function to hash a password
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
        
        # Check if tables exist, if not create them
        cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'users')")
        if not cursor.fetchone()[0]:
            print("Creating users table...")
            cursor.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR UNIQUE NOT NULL,
                    username VARCHAR UNIQUE NOT NULL,
                    hashed_password VARCHAR NOT NULL,
                    full_name VARCHAR,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """)
            print("Users table created successfully")
        
        cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'roles')")
        if not cursor.fetchone()[0]:
            print("Creating roles table...")
            cursor.execute("""
                CREATE TABLE roles (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR UNIQUE NOT NULL,
                    description VARCHAR,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """)
            print("Roles table created successfully")
        
        cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'user_role')")
        if not cursor.fetchone()[0]:
            print("Creating user_role table...")
            cursor.execute("""
                CREATE TABLE user_role (
                    user_id INTEGER REFERENCES users(id),
                    role_id INTEGER REFERENCES roles(id),
                    PRIMARY KEY (user_id, role_id)
                )
            """)
            print("User_role table created successfully")
        
        # Insert roles if they don't exist
        roles = [
            ("admin", "Administrator with all privileges"),
            ("manager", "Department manager with elevated privileges"),
            ("agent", "Support agent with ticket management capabilities"),
            ("user", "Regular user who can submit tickets")
        ]
        
        role_ids = {}
        for role_name, role_desc in roles:
            cursor.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
            result = cursor.fetchone()
            
            if result:
                role_ids[role_name] = result[0]
                print(f"Role already exists: {role_name}")
            else:
                cursor.execute(
                    "INSERT INTO roles (name, description) VALUES (%s, %s) RETURNING id",
                    (role_name, role_desc)
                )
                role_id = cursor.fetchone()[0]
                role_ids[role_name] = role_id
                print(f"Created role: {role_name}")
        
        # Insert test users
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
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (user_data["email"],))
            result = cursor.fetchone()
            
            if result:
                user_id = result[0]
                print(f"User already exists: {user_data['username']}")
            else:
                # Create new user
                cursor.execute(
                    "INSERT INTO users (email, username, hashed_password, full_name) VALUES (%s, %s, %s, %s) RETURNING id",
                    (user_data["email"], user_data["username"], hash_password(user_data["password"]), user_data["full_name"])
                )
                user_id = cursor.fetchone()[0]
                
                # Add user roles
                for role_name in user_data["roles"]:
                    cursor.execute(
                        "INSERT INTO user_role (user_id, role_id) VALUES (%s, %s)",
                        (user_id, role_ids[role_name])
                    )
                
                print(f"Created user: {user_data['username']} with roles: {', '.join(user_data['roles'])}")
        
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