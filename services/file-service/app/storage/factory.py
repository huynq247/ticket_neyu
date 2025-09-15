from app.core.config import settings
from app.storage.base import StorageBackend
from app.storage.local import LocalStorageBackend

def get_storage_backend() -> StorageBackend:
    """Factory function to get the configured storage backend"""
    storage_type = settings.STORAGE_TYPE.lower()
    
    if storage_type == "local":
        return LocalStorageBackend()
    elif storage_type == "s3":
        # For future implementation
        # return S3StorageBackend()
        raise NotImplementedError("S3 storage backend not implemented yet")
    elif storage_type == "gridfs":
        # For future implementation
        # return GridFSStorageBackend()
        raise NotImplementedError("GridFS storage backend not implemented yet")
    else:
        raise ValueError(f"Unknown storage type: {storage_type}")

# Initialize the storage backend
storage = get_storage_backend()