"""
Simple script to test database connections
"""
import sys
import os
import pymongo
import psycopg2
import traceback

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_mongodb_connection():
    """Test connection to MongoDB"""
    try:
        # Get MongoDB connection info from env file
        from dotenv import load_dotenv
        load_dotenv("config/database.env")
        
        mongodb_uri = os.getenv("MONGODB_URI")
        print(f"Connecting to MongoDB: {mongodb_uri}")
        
        # Connect to MongoDB
        client = pymongo.MongoClient(mongodb_uri)
        
        # Verify connection
        info = client.server_info()
        print(f"MongoDB connection successful!")
        print(f"MongoDB version: {info.get('version')}")
        print(f"Available databases: {client.list_database_names()}")
        
        return True
    except Exception as e:
        print(f"MongoDB connection error: {str(e)}")
        traceback.print_exc()
        return False

def test_postgres_connection():
    """Test connection to PostgreSQL"""
    try:
        # Get PostgreSQL connection info from env file
        from dotenv import load_dotenv
        load_dotenv("config/database.env")
        
        postgres_host = os.getenv("POSTGRES_HOST")
        postgres_port = os.getenv("POSTGRES_PORT")
        postgres_user = os.getenv("POSTGRES_USER")
        postgres_password = os.getenv("POSTGRES_PASSWORD")
        postgres_db = os.getenv("POSTGRES_DATABASE")
        
        print(f"Connecting to PostgreSQL: {postgres_host}:{postgres_port}/{postgres_db}")
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=postgres_host,
            port=postgres_port,
            user=postgres_user,
            password=postgres_password,
            database=postgres_db
        )
        
        # Verify connection
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print("PostgreSQL connection successful!")
        print(f"PostgreSQL version: {version}")
        
        # Get list of tables
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print(f"Available tables: {[table[0] for table in tables]}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"PostgreSQL connection error: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing database connections...")
    print("\n" + "="*50)
    mongo_ok = test_mongodb_connection()
    print("="*50 + "\n")
    
    postgres_ok = test_postgres_connection()
    print("="*50 + "\n")
    
    if mongo_ok and postgres_ok:
        print("All database connections are working!")
        sys.exit(0)
    else:
        print("Some database connections failed!")
        sys.exit(1)