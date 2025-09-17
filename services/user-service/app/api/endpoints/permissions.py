from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import Permission
from app.schemas.user import Permission as PermissionSchema, PermissionCreate, PermissionUpdate
from app.db.session import get_db

router = APIRouter()


@router.get("/", response_model=List[PermissionSchema])
def read_permissions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve permissions.
    """
    permissions = db.query(Permission).offset(skip).limit(limit).all()
    return permissions


@router.post("/", response_model=PermissionSchema)
def create_permission(
    *,
    db: Session = Depends(get_db),
    permission_in: PermissionCreate,
    current_user: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new permission.
    """
    # Check if permission with this id already exists
    permission = db.query(Permission).filter(Permission.id == permission_in.id).first()
    if permission:
        raise HTTPException(
            status_code=400,
            detail="A permission with this id already exists",
        )
    
    # Create new permission
    db_permission = Permission(**permission_in.dict())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


@router.put("/{permission_id}", response_model=PermissionSchema)
def update_permission(
    *,
    db: Session = Depends(get_db),
    permission_id: str,
    permission_in: PermissionUpdate,
    current_user: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a permission.
    """
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )
    
    # Update permission fields
    for field, value in permission_in.dict(exclude_unset=True).items():
        setattr(permission, field, value)
    
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


@router.delete("/{permission_id}", response_model=PermissionSchema)
def delete_permission(
    *,
    db: Session = Depends(get_db),
    permission_id: str,
    current_user: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a permission.
    """
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )
    
    db.delete(permission)
    db.commit()
    return permission