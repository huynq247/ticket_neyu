import os
import shutil
import aiofiles
from typing import BinaryIO, Optional

from app.core.config import settings
from app.storage.base import StorageBackend


class LocalStorageBackend(StorageBackend):
    """Implementation of storage backend using local filesystem"""
    
    def __init__(self):
        """Initialize the storage backend with the configured base path"""
        self.base_path = settings.LOCAL_STORAGE_PATH
        os.makedirs(self.base_path, exist_ok=True)
    
    async def save(self, file_id: str, file_obj: BinaryIO, content_type: str) -> str:
        """Save a file to local filesystem"""
        # Create path with first two chars of file_id as subdirectory to distribute files
        subdir = file_id[:2]
        dir_path = os.path.join(self.base_path, subdir)
        os.makedirs(dir_path, exist_ok=True)
        
        file_path = os.path.join(subdir, file_id)
        full_path = os.path.join(self.base_path, file_path)
        
        # Save the file
        async with aiofiles.open(full_path, 'wb') as out_file:
            # Read and write in chunks to handle large files
            chunk_size = 1024 * 1024  # 1MB chunks
            while True:
                chunk = file_obj.read(chunk_size)
                if not chunk:
                    break
                await out_file.write(chunk)
        
        return file_path
    
    async def get(self, file_path: str) -> Optional[BinaryIO]:
        """Retrieve a file from local filesystem"""
        full_path = os.path.join(self.base_path, file_path)
        
        if not os.path.exists(full_path):
            return None
        
        return open(full_path, 'rb')
    
    async def delete(self, file_path: str) -> bool:
        """Delete a file from local filesystem"""
        full_path = os.path.join(self.base_path, file_path)
        
        if not os.path.exists(full_path):
            return False
        
        try:
            os.remove(full_path)
            return True
        except Exception:
            return False
    
    def get_download_url(self, file_id: str, file_path: str) -> str:
        """Get a URL for downloading the file"""
        return f"{settings.API_V1_STR}/files/{file_id}/download"