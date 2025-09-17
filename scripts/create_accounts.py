import psycopg2
import sys
from passlib.context import CryptContext
from datetime import datetime

# Database connection parameters
db_params = {
    'host': '14.161.50.86',
    'port': '25432',
    'database': 'ticket_db',
    'user': 'admin',
    'password': 'Mypassword123'
}

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_users():
    """Create users from accounts.txt file"""
    try:
        # Connect to the database
        print(f"Connecting to database {db_params['database']} on {db_params['host']}:{db_params['port']}...")
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Check if departments table exists, create if not
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'departments')")
        if not cursor.fetchone()[0]:
            print("Creating departments table...")
            cursor.execute("""
                CREATE TABLE departments (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    description VARCHAR(255),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """)
            conn.commit()
        
        # Check if roles table exists, create if not
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'roles')")
        if not cursor.fetchone()[0]:
            print("Creating roles table...")
            cursor.execute("""
                CREATE TABLE roles (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    description VARCHAR(255),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """)
            conn.commit()
        
        # Check if users table exists, create if not
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
        if not cursor.fetchone()[0]:
            print("Creating users table...")
            cursor.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    hashed_password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255),
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE,
                    department_id INTEGER REFERENCES departments(id)
                )
            """)
            conn.commit()
        
        # Check if user_role table exists, create if not
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'user_role')")
        if not cursor.fetchone()[0]:
            print("Creating user_role table...")
            cursor.execute("""
                CREATE TABLE user_role (
                    user_id INTEGER REFERENCES users(id),
                    role_id INTEGER REFERENCES roles(id),
                    PRIMARY KEY (user_id, role_id)
                )
            """)
            conn.commit()
        
        # Process the accounts.txt file
        print("Processing accounts.txt file...")
        with open('D:/NeyuProject/services/user-service/accounts.txt', 'r') as f:
            lines = f.readlines()
            # Skip header
            for i, line in enumerate(lines[1:], 1):
                parts = line.strip().split('\t')
                if len(parts) < 5:
                    print(f"Skipping line {i+1}: Invalid format")
                    continue
                
                username, password, email, roles_str, department = parts
                
                # Create department if it doesn't exist
                cursor.execute(
                    "SELECT id FROM departments WHERE name = %s",
                    (department,)
                )
                dept_result = cursor.fetchone()
                if not dept_result:
                    print(f"Creating department: {department}")
                    cursor.execute(
                        "INSERT INTO departments (name) VALUES (%s) RETURNING id",
                        (department,)
                    )
                    dept_id = cursor.fetchone()[0]
                else:
                    dept_id = dept_result[0]
                
                # Hash password
                hashed_password = get_password_hash(password)
                
                # Check if user already exists
                cursor.execute(
                    "SELECT id FROM users WHERE email = %s OR username = %s",
                    (email, username)
                )
                user_result = cursor.fetchone()
                
                if user_result:
                    print(f"Updating user: {username} ({email})")
                    cursor.execute(
                        """
                        UPDATE users 
                        SET hashed_password = %s, full_name = %s, department_id = %s
                        WHERE id = %s
                        """,
                        (hashed_password, username, dept_id, user_result[0])
                    )
                    user_id = user_result[0]
                else:
                    print(f"Creating user: {username} ({email})")
                    cursor.execute(
                        """
                        INSERT INTO users (username, email, hashed_password, full_name, department_id)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (username, email, hashed_password, username, dept_id)
                    )
                    user_id = cursor.fetchone()[0]
                
                # Process roles
                roles = [r.strip() for r in roles_str.split(',')]
                for role_name in roles:
                    # Create role if it doesn't exist
                    cursor.execute(
                        "SELECT id FROM roles WHERE name = %s",
                        (role_name,)
                    )
                    role_result = cursor.fetchone()
                    
                    if not role_result:
                        print(f"Creating role: {role_name}")
                        cursor.execute(
                            "INSERT INTO roles (name) VALUES (%s) RETURNING id",
                            (role_name,)
                        )
                        role_id = cursor.fetchone()[0]
                    else:
                        role_id = role_result[0]
                    
                    # Assign role to user
                    cursor.execute(
                        "SELECT 1 FROM user_role WHERE user_id = %s AND role_id = %s",
                        (user_id, role_id)
                    )
                    
                    if not cursor.fetchone():
                        print(f"Assigning role {role_name} to user {username}")
                        cursor.execute(
                            "INSERT INTO user_role (user_id, role_id) VALUES (%s, %s)",
                            (user_id, role_id)
                        )
            
            conn.commit()
            print("All users processed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback() if 'conn' in locals() else None
    finally:
        cursor.close() if 'cursor' in locals() else None
        conn.close() if 'conn' in locals() else None

if __name__ == "__main__":
    create_users()