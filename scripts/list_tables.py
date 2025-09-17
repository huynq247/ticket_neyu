import psycopg2
import sys

# Database connection parameters
DB_HOST = "14.161.50.86"
DB_PORT = "25432"
DB_NAME = "ticket_db"
DB_USER = "admin"
DB_PASS = "Mypassword123"

def list_tables():
    try:
        # Connect to the PostgreSQL database
        print(f"Connecting to database {DB_NAME} on {DB_HOST}:{DB_PORT}...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        
        # Create a cursor
        cur = conn.cursor()
        
        # Execute a query to list all tables
        print("Fetching all tables in the database...")
        cur.execute("""
            SELECT 
                table_schema, 
                table_name 
            FROM 
                information_schema.tables 
            WHERE 
                table_schema NOT IN ('pg_catalog', 'information_schema')
                AND table_type = 'BASE TABLE'
            ORDER BY 
                table_schema, 
                table_name;
        """)
        
        # Fetch the results
        tables = cur.fetchall()
        
        # Print the tables
        if tables:
            print("\nTables in the database:")
            print("------------------------")
            for schema, table in tables:
                print(f"{schema}.{table}")
        else:
            print("\nNo tables found in the database.")
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    list_tables()