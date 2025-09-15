#!/usr/bin/env python
"""
Database connection tester script.
This script checks connections to all configured databases.
"""

import sys
import os

# Add parent directory to path to import config module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import test_connections

def main():
    """
    Test connections to all databases and print results.
    """
    print("Testing database connections...")
    status = test_connections()
    
    for db, status_msg in status.items():
        print(f"{db.upper()}: {status_msg}")
    
    # Check if all connections were successful
    if all(status.startswith("Connected") for status in status.values()):
        print("\nAll database connections successful!")
        return 0
    else:
        print("\nSome database connections failed. Please check your configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())