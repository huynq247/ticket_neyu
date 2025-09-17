"""
Check Database Structure
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
        
        # Get list of tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cursor.fetchall()
        print("\nExisting tables:")
        for table in tables:
            print(f"- {table[0]}")
        
        # Get column information for users table
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        
        print("\nUsers table structure:")
        for column in columns:
            print(f"- {column[0]}: {column[1]}, Nullable: {column[2]}, Default: {column[3]}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_table_structure()