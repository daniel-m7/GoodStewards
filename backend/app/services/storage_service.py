import boto3
from botocore.exceptions import ClientError
from typing import Optional
import uuid
from datetime import datetime, timedelta

from app.core.config import settings

class R2StorageService:
    """Service for Cloudflare R2 storage operations."""
    
    def __init__(self):
        # For development, use mock storage if R2 credentials are not configured
        if not settings.R2_ENDPOINT_URL or not settings.R2_ACCESS_KEY_ID or not settings.R2_SECRET_ACCESS_KEY:
            self.s3_client = None
            self.bucket_name = "mock-bucket"
            print("Using mock storage service for development")
        else:
            self.s3_client = boto3.client(
                's3',
                endpoint_url=settings.R2_ENDPOINT_URL,
                aws_access_key_id=settings.R2_ACCESS_KEY_ID,
                aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
                region_name='auto'  # R2 doesn't use regions like S3
            )
            self.bucket_name = settings.R2_BUCKET_NAME
    
    async def upload_image(self, image_data: bytes, content_type: str = "image/jpeg") -> Optional[str]:
        """
        Upload an image to R2 storage.
        
        Args:
            image_data: Raw image bytes
            content_type: MIME type of the image
            
        Returns:
            URL of the uploaded image if successful, None otherwise
        """
        try:
            # Generate unique filename
            file_extension = content_type.split('/')[-1]
            filename = f"receipts/{uuid.uuid4()}.{file_extension}"
            
            # For development, return mock URL if R2 is not configured
            if not self.s3_client:
                return f"https://mock-storage.example.com/{self.bucket_name}/{filename}"
            
            # Upload to R2
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=image_data,
                ContentType=content_type,
                ACL='private'  # Private by default for security
            )
            
            # Return the object URL
            return f"{settings.R2_ENDPOINT_URL}/{self.bucket_name}/{filename}"
            
        except ClientError as e:
            print(f"R2 upload failed: {str(e)}")
            return None
    
    async def generate_presigned_url(self, object_key: str, expires_in: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for temporary access to a private object.
        
        Args:
            object_key: The key of the object in R2
            expires_in: URL expiration time in seconds (default: 1 hour)
            
        Returns:
            Presigned URL if successful, None otherwise
        """
        try:
            # For development, return mock URL if R2 is not configured
            if not self.s3_client:
                return f"https://mock-storage.example.com/{self.bucket_name}/{object_key}?expires={expires_in}"
            
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=expires_in
            )
            return url
            
        except ClientError as e:
            print(f"Failed to generate presigned URL: {str(e)}")
            return None
    
    async def delete_image(self, object_key: str) -> bool:
        """
        Delete an image from R2 storage.
        
        Args:
            object_key: The key of the object to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            # For development, return success if R2 is not configured
            if not self.s3_client:
                print(f"Mock deletion of {object_key}")
                return True
            
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return True
            
        except ClientError as e:
            print(f"R2 deletion failed: {str(e)}")
            return False 