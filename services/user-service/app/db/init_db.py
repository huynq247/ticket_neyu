import alembic.config
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from app.core.config import settings
from app.db.session import Base

def create_tables() -> None:
    """
    Create database tables using SQLAlchemy
    """
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    # Create database if it doesn't exist
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Created database: {settings.POSTGRES_DATABASE}")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

def init_admin_user() -> None:
    """
    Create initial admin user and roles
    """
    from app.db.session import SessionLocal
    from app.models.user import User, Role, Department
    from app.core.security import get_password_hash
    
    db = SessionLocal()
    
    # Check if admin role exists
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        admin_role = Role(
            name="admin",
            description="Administrator with all privileges"
        )
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)
        print("Created admin role")
    
    # Check if user role exists
    user_role = db.query(Role).filter(Role.name == "user").first()
    if not user_role:
        user_role = Role(
            name="user",
            description="Regular user"
        )
        db.add(user_role)
        db.commit()
        db.refresh(user_role)
        print("Created user role")
    
    # Check if IT department exists
    it_department = db.query(Department).filter(Department.name == "IT").first()
    if not it_department:
        it_department = Department(
            name="IT",
            description="Information Technology Department"
        )
        db.add(it_department)
        db.commit()
        db.refresh(it_department)
        print("Created IT department")
    
    # Check if admin user exists
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin_user:
        admin_user = User(
            email="admin@example.com",
            username="admin",
            hashed_password=get_password_hash("admin"),
            full_name="Admin User",
            is_active=True,
            department_id=it_department.id
        )
        admin_user.roles.append(admin_role)
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Created admin user")
    
    db.close()

def main() -> None:
    """
    Initialize the database
    """
    print("Initializing database...")
    create_tables()
    init_admin_user()
    print("Database initialization completed.")

if __name__ == "__main__":
    main()