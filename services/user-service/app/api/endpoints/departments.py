from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import Department
from app.schemas.user import Department as DepartmentSchema, DepartmentCreate, DepartmentUpdate
from app.db.session import get_db

router = APIRouter()


@router.get("/", response_model=List[DepartmentSchema])
def read_departments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve departments.
    """
    departments = db.query(Department).offset(skip).limit(limit).all()
    return departments


@router.post("/", response_model=DepartmentSchema)
def create_department(
    *,
    db: Session = Depends(get_db),
    department_in: DepartmentCreate,
    current_user: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new department.
    """
    # Check if department with this name already exists
    department = db.query(Department).filter(Department.name == department_in.name).first()
    if department:
        raise HTTPException(
            status_code=400,
            detail="A department with this name already exists",
        )
    
    # Create new department
    db_department = Department(**department_in.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@router.get("/{department_id}", response_model=DepartmentSchema)
def read_department(
    *,
    db: Session = Depends(get_db),
    department_id: int,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get department by ID.
    """
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )
    return department


@router.put("/{department_id}", response_model=DepartmentSchema)
def update_department(
    *,
    db: Session = Depends(get_db),
    department_id: int,
    department_in: DepartmentUpdate,
    current_user: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a department.
    """
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )
    
    # Check if trying to update department name that already exists
    if department_in.name and department_in.name != department.name:
        exists = db.query(Department).filter(Department.name == department_in.name).first()
        if exists:
            raise HTTPException(
                status_code=400,
                detail="Department name already exists",
            )
    
    # Update department
    for key, value in department_in.dict(exclude_unset=True).items():
        setattr(department, key, value)
    
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


@router.delete("/{department_id}", response_model=DepartmentSchema)
def delete_department(
    *,
    db: Session = Depends(get_db),
    department_id: int,
    current_user: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a department.
    """
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )
    
    # Check if department has users
    if department.users:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete department with associated users",
        )
    
    db.delete(department)
    db.commit()
    return department