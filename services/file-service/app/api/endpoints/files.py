from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query, Path
from fastapi.responses import StreamingResponse
from typing import List, Optional
import json

from app.api.deps import security, get_current_user
from app.models.file import create_file, get_file, update_file, delete_file, list_files, count_files
from app.schemas.file import FileCreate, FileUpdate, FileList, File as FileSchema
from app.storage.factory import storage
from app.utils.service import check_file_permission

router = APIRouter()


@router.post("/", response_model=FileSchema, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    ticket_id: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    current_user = Depends(get_current_user)
):
    """
    Upload a new file
    """
    # Check file size
    file_size = 0
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Seek back to start
    
    from app.core.config import settings
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )
    
    # Prepare file data
    file_data = FileCreate(
        filename=file.filename,
        content_type=file.content_type,
        size=file_size,
        description=description,
        owner_id=current_user["id"],
        ticket_id=ticket_id,
        tags=json.loads(tags) if tags else []
    )
    
    # Save file
    from bson import ObjectId
    file_id = str(ObjectId())
    file_path = await storage.save(file_id, file.file, file.content_type)
    
    # Create record in database
    db_file = create_file(file_data, file_path)
    
    # Convert ObjectId to string
    db_file["_id"] = str(db_file["_id"])
    
    # Add download URL
    result = FileSchema(
        **db_file,
        download_url=storage.get_download_url(db_file["_id"], db_file["path"])
    )
    
    return result


@router.get("/{file_id}", response_model=FileSchema)
async def get_file_by_id(
    file_id: str = Path(...),
    current_user = Depends(get_current_user)
):
    """
    Get file metadata by ID
    """
    db_file = get_file(file_id)
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check permission
    is_owner = db_file["owner_id"] == current_user["id"]
    has_ticket_access = await check_file_permission(current_user["id"], db_file.get("ticket_id"))
    
    if not (is_owner or has_ticket_access or current_user.get("is_admin", False)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Convert ObjectId to string
    db_file["_id"] = str(db_file["_id"])
    
    # Add download URL
    result = FileSchema(
        **db_file,
        download_url=storage.get_download_url(db_file["_id"], db_file["path"])
    )
    
    return result


@router.get("/{file_id}/download")
async def download_file(
    file_id: str = Path(...),
    current_user = Depends(get_current_user)
):
    """
    Download a file
    """
    db_file = get_file(file_id)
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check permission
    is_owner = db_file["owner_id"] == current_user["id"]
    has_ticket_access = await check_file_permission(current_user["id"], db_file.get("ticket_id"))
    
    if not (is_owner or has_ticket_access or current_user.get("is_admin", False)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get file from storage
    file_obj = await storage.get(db_file["path"])
    if not file_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found in storage"
        )
    
    # Return file as streaming response
    return StreamingResponse(
        iter([file_obj.read()]),
        media_type=db_file["content_type"],
        headers={"Content-Disposition": f"attachment; filename={db_file['filename']}"}
    )


@router.get("/", response_model=FileList)
async def list_files_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    owner_id: Optional[str] = Query(None),
    ticket_id: Optional[str] = Query(None),
    filename: Optional[str] = Query(None),
    current_user = Depends(get_current_user)
):
    """
    List files with filtering options
    """
    # Only admins can see all files, others can only see their own files or files of tickets they have access to
    is_admin = current_user.get("is_admin", False)
    
    if not is_admin and owner_id and owner_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to view other users' files"
        )
    
    # If not admin and no owner specified, only show user's files
    if not is_admin and not owner_id:
        owner_id = current_user["id"]
    
    # Check ticket access if filter by ticket
    if ticket_id and not is_admin and owner_id != current_user["id"]:
        has_access = await check_file_permission(current_user["id"], ticket_id)
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to view files of this ticket"
            )
    
    # Get files from database
    files = list_files(skip, limit, owner_id, ticket_id, filename)
    total = count_files(owner_id, ticket_id, filename)
    
    # Convert ObjectId to string and add download URL
    result = []
    for file in files:
        file["_id"] = str(file["_id"])
        result.append(
            FileSchema(
                **file,
                download_url=storage.get_download_url(file["_id"], file["path"])
            )
        )
    
    return FileList(total=total, files=result)


@router.patch("/{file_id}", response_model=FileSchema)
async def update_file_endpoint(
    update_data: FileUpdate,
    file_id: str = Path(...),
    current_user = Depends(get_current_user)
):
    """
    Update file metadata
    """
    db_file = get_file(file_id)
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Only owner or admin can update file
    is_owner = db_file["owner_id"] == current_user["id"]
    is_admin = current_user.get("is_admin", False)
    
    if not (is_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update file
    updated_file = update_file(file_id, update_data)
    if not updated_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Convert ObjectId to string
    updated_file["_id"] = str(updated_file["_id"])
    
    # Add download URL
    result = FileSchema(
        **updated_file,
        download_url=storage.get_download_url(updated_file["_id"], updated_file["path"])
    )
    
    return result


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file_endpoint(
    file_id: str = Path(...),
    current_user = Depends(get_current_user)
):
    """
    Delete a file
    """
    db_file = get_file(file_id)
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Only owner or admin can delete file
    is_owner = db_file["owner_id"] == current_user["id"]
    is_admin = current_user.get("is_admin", False)
    
    if not (is_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Delete file from storage
    deleted_from_storage = await storage.delete(db_file["path"])
    if not deleted_from_storage:
        # Log error but continue to delete from database
        print(f"Failed to delete file {file_id} from storage")
    
    # Delete from database
    deleted_from_db = delete_file(file_id)
    if not deleted_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found in database"
        )
    
    return None