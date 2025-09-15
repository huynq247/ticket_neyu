from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import Role
from app.schemas.user import Role as RoleSchema, RoleCreate, RoleUpdate
from app.db.session import get_db

router = APIRouter()


@router.get("/", response_model=List[RoleSchema])
def read_roles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve roles.
    """
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles


@router.post("/", response_model=RoleSchema)
def create_role(
    *,
    db: Session = Depends(get_db),
    role_in: RoleCreate,
    current_user: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new role.
    """
    # Check if role with this name already exists
    role = db.query(Role).filter(Role.name == role_in.name).first()
    if role:
        raise HTTPException(
            status_code=400,
            detail="A role with this name already exists",
        )
    
    # Create new role
    db_role = Role(**role_in.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@router.get("/{role_id}", response_model=RoleSchema)
def read_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get role by ID.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )
    return role


@router.put("/{role_id}", response_model=RoleSchema)
def update_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    role_in: RoleUpdate,
    current_user: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a role.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )
    
    # Check if trying to update role name that already exists
    if role_in.name and role_in.name != role.name:
        exists = db.query(Role).filter(Role.name == role_in.name).first()
        if exists:
            raise HTTPException(
                status_code=400,
                detail="Role name already exists",
            )
    
    # Update role
    for key, value in role_in.dict(exclude_unset=True).items():
        setattr(role, key, value)
    
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.delete("/{role_id}", response_model=RoleSchema)
def delete_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    current_user: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a role.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )
    
    # Check if role has users
    if role.users:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete role with associated users",
        )
    
    db.delete(role)
    db.commit()
    return role