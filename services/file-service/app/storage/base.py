from abc import ABC, abstractmethod
from typing import BinaryIO, Optional

class StorageBackend(ABC):
    """Abstract base class for storage backends"""
    
    @abstractmethod
    async def save(self, file_id: str, file_obj: BinaryIO, content_type: str) -> str:
        """
        Save a file to storage
        
        Args:
            file_id: Unique identifier for the file
            file_obj: File-like object to save
            content_type: MIME type of the file
            
        Returns:
            Path or identifier where the file is stored
        """
        pass
    
    @abstractmethod
    async def get(self, file_path: str) -> Optional[BinaryIO]:
        """
        Retrieve a file from storage
        
        Args:
            file_path: Path or identifier where the file is stored
            
        Returns:
            File-like object if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def delete(self, file_path: str) -> bool:
        """
        Delete a file from storage
        
        Args:
            file_path: Path or identifier where the file is stored
            
        Returns:
            True if deleted successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def get_download_url(self, file_id: str, file_path: str) -> str:
        """
        Get a URL for downloading the file
        
        Args:
            file_id: Unique identifier for the file
            file_path: Path or identifier where the file is stored
            
        Returns:
            URL for downloading the file
        """
        pass