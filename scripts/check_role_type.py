"""
Check Database Structure in detail
"""
import os
import psycopg2

# Database connection settings
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Mypassword123")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "14.161.50.86")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "25432")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "postgres")

def check_table_structure():
    # Connect to the database
    conn_string = f"host={POSTGRES_HOST} port={POSTGRES_PORT} dbname={POSTGRES_DATABASE} user={POSTGRES_USER} password={POSTGRES_PASSWORD}"
    
    try:
        # Connect to the database
        print(f"Connecting to database: {conn_string}")
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        print("Connected to database successfully")
        
        # Get detailed info about the role column
        cursor.execute("""
            SELECT column_name, udt_name, data_type, character_maximum_length
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'role'
        """)
        role_info = cursor.fetchone()
        print(f"\nRole column details: {role_info}")
        
        # If the role is an enum, get its values
        if role_info and role_info[1].startswith('_'):
            enum_type = role_info[1][1:]  # Remove leading underscore
            cursor.execute(f"SELECT enumlabel FROM pg_enum WHERE enumtypid = '{enum_type}'::regtype::oid")
            enum_values = cursor.fetchall()
            print(f"\nEnum values for {enum_type}: {[v[0] for v in enum_values]}")
        
        # Get a sample of existing users to see role values
        cursor.execute("SELECT id, username, email, role FROM users LIMIT 5")
        users = cursor.fetchall()
        print("\nSample users:")
        for user in users:
            print(f"- ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_table_structure()