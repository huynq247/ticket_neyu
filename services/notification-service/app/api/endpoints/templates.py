from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Body
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId

from app.api.deps import security, get_current_user
from app.models.template import create_template, get_template, update_template, delete_template, list_templates, count_templates
from app.schemas.template import TemplateCreate, TemplateUpdate, TemplateList, Template

router = APIRouter()


@router.post("/", response_model=Template, status_code=status.HTTP_201_CREATED)
async def create_template_endpoint(
    template_data: TemplateCreate,
    current_user = Depends(get_current_user)
):
    """
    Create a new notification template
    """
    # Check if template with this name already exists
    existing_templates = list_templates(name=template_data.name)
    if existing_templates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Template with name '{template_data.name}' already exists"
        )
    
    # Create template in database
    template = create_template(template_data)
    
    # Convert ObjectId to string
    template["_id"] = str(template["_id"])
    
    return template


@router.get("/{template_id}", response_model=Template)
async def get_template_endpoint(
    template_id: str = Path(...),
    current_user = Depends(get_current_user)
):
    """
    Get template by ID
    """
    template = get_template(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Convert ObjectId to string
    template["_id"] = str(template["_id"])
    
    return template


@router.get("/", response_model=TemplateList)
async def list_templates_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    name: Optional[str] = Query(None),
    template_type: Optional[str] = Query(None),
    current_user = Depends(get_current_user)
):
    """
    List templates with filtering options
    """
    # Get templates from database
    templates = list_templates(skip, limit, name, template_type)
    total = count_templates(name, template_type)
    
    # Convert ObjectId to string
    for template in templates:
        template["_id"] = str(template["_id"])
    
    return TemplateList(total=total, templates=templates)


@router.put("/{template_id}", response_model=Template)
async def update_template_endpoint(
    template_data: TemplateUpdate,
    template_id: str = Path(...),
    current_user = Depends(get_current_user)
):
    """
    Update an existing template
    """
    # Check if template exists
    template = get_template(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Update template in database
    updated = update_template(template_id, template_data)
    
    # Convert ObjectId to string
    updated["_id"] = str(updated["_id"])
    
    return updated


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template_endpoint(
    template_id: str = Path(...),
    current_user = Depends(get_current_user)
):
    """
    Delete a template
    """
    # Check if template exists
    template = get_template(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Delete template from database
    delete_template(template_id)
    
    return None