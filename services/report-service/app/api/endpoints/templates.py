from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from typing import Optional, List, Dict, Any

from app.api.deps import get_current_user
from app.models.template import (
    create_template,
    get_template,
    update_template,
    list_templates,
    count_templates,
    delete_template
)
from app.schemas.report import (
    ReportTemplateCreate,
    ReportTemplateUpdate,
    ReportTemplate,
    ReportTemplateList,
    ReportType
)

router = APIRouter()


@router.post("/", response_model=ReportTemplate, status_code=status.HTTP_201_CREATED)
async def create_new_template(
    template_data: ReportTemplateCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a new report template
    """
    template = create_template(template_data, current_user["id"])
    if not template:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Template with this name already exists"
        )
    
    return template


@router.get("/{template_id}", response_model=ReportTemplate)
async def get_template_by_id(
    template_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get a template by ID
    """
    template = get_template(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return template


@router.put("/{template_id}", response_model=ReportTemplate)
async def update_template_by_id(
    template_data: ReportTemplateUpdate,
    template_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update a template
    """
    existing = get_template(template_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Check if user has access to this template
    if existing["created_by"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this template"
        )
    
    updated = update_template(template_id, template_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update template"
        )
    
    return updated


@router.get("/", response_model=ReportTemplateList)
async def get_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    report_type: Optional[ReportType] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get templates with filtering
    """
    templates = list_templates(
        skip=skip,
        limit=limit,
        report_type=report_type
    )
    
    total = count_templates(report_type=report_type)
    
    return {
        "total": total,
        "templates": templates
    }


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template_by_id(
    template_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Delete a template
    """
    existing = get_template(template_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Check if user has access to this template
    if existing["created_by"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this template"
        )
    
    success = delete_template(template_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting template"
        )
    
    return None