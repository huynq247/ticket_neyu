import psycopg2
import sys
from tabulate import tabulate

# Database connection parameters
db_params = {
    'host': '14.161.50.86',
    'port': '25432',
    'database': 'ticket_db',
    'user': 'admin',
    'password': 'Mypassword123'
}

def check_users():
    """Check and display users in the database"""
    try:
        # Connect to the database
        print(f"Connecting to database {db_params['database']} on {db_params['host']}:{db_params['port']}...")
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Query to get users
        print("Fetching users...")
        cursor.execute("""
            SELECT id, username, email, full_name, is_active 
            FROM users
            ORDER BY id
        """)
        
        users = cursor.fetchall()
        
        # Display users in a table
        if users:
            headers = ["ID", "Username", "Email", "Full Name", "Active"]
            print("\nUsers in the database:")
            print(tabulate(users, headers=headers, tablefmt="pretty"))
            print(f"\nTotal users: {len(users)}")
        else:
            print("\nNo users found in the database.")
            
        # Check if admin@example.com exists
        cursor.execute("""
            SELECT id, username, email
            FROM users
            WHERE email = 'admin@example.com'
        """)
        admin_user = cursor.fetchone()
        
        if admin_user:
            print(f"\nFound admin@example.com user with ID {admin_user[0]}, username: {admin_user[1]}")
        else:
            print("\nNo user found with email admin@example.com")
        
        # Query to get roles
        print("\nFetching roles...")
        cursor.execute("""
            SELECT id, name, description
            FROM roles
            ORDER BY id
        """)
        
        roles = cursor.fetchall()
        
        if roles:
            headers = ["ID", "Name", "Description"]
            print("\nRoles in the database:")
            print(tabulate(roles, headers=headers, tablefmt="pretty"))
        else:
            print("\nNo roles found in the database.")
        
        # Query to get permissions
        print("\nFetching permissions...")
        cursor.execute("""
            SELECT id, name, category
            FROM permissions
            ORDER BY category, id
        """)
        
        permissions = cursor.fetchall()
        
        if permissions:
            headers = ["ID", "Name", "Category"]
            print("\nPermissions in the database:")
            print(tabulate(permissions, headers=headers, tablefmt="pretty"))
            print(f"\nTotal permissions: {len(permissions)}")
        else:
            print("\nNo permissions found in the database.")
            
        # Close connection
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    try:
        # Install tabulate if not available
        import importlib
        if importlib.util.find_spec("tabulate") is None:
            print("Installing tabulate package...")
            import pip
            pip.main(["install", "tabulate"])
            print("Tabulate installed successfully.")
    except:
        print("Could not install tabulate. Tables might not display correctly.")
    
    success = check_users()
    
    if success:
        print("\nDatabase check completed successfully.")
    else:
        print("\nDatabase check failed.")
        sys.exit(1)