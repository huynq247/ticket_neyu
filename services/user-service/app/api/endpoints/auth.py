from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.schemas.token import Token, RefreshToken, LoginRequest
from app.models.user import User
from app.db.session import get_db

router = APIRouter()


@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # Check username/email
    user = db.query(User).filter(
        (User.username == form_data.username) | (User.email == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(user.id, expires_delta=access_token_expires),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/login/email", response_model=Token)
def login_with_email(
    db: Session = Depends(get_db), login_data: LoginRequest = Body(...)
) -> Any:
    """
    Email and password login, get an access token for future requests
    """
    # Check email - using explicit string parameters to avoid SQLAlchemy binding issues
    email = login_data.email
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(user.id, expires_delta=access_token_expires),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
def refresh_token(
    db: Session = Depends(get_db), refresh_token: RefreshToken = Body(...)
) -> Any:
    """
    Refresh token endpoint
    """
    try:
        from jose import jwt, JWTError
        from app.core.security import ALGORITHM
        
        payload = jwt.decode(
            refresh_token.refresh_token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid token")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=400, detail="User not found or inactive")
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        return {
            "access_token": create_access_token(user.id, expires_delta=access_token_expires),
            "refresh_token": create_refresh_token(user.id),
            "token_type": "bearer",
        }
    
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid refresh token")