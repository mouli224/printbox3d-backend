"""
S3 Service — PrintBox3D
Centralises all AWS S3 interactions.

Usage:
    from api.services.s3_service import S3Service
    url = S3Service.generate_presigned_upload_url('products', 'planter.jpg', 'image/jpeg')
"""

import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from django.conf import settings

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Allowed file types per upload category
# --------------------------------------------------------------------------
ALLOWED_TYPES = {
    'products': {
        'image/jpeg', 'image/jpg', 'image/png', 'image/webp',
    },
    'categories': {
        'image/jpeg', 'image/jpg', 'image/png', 'image/webp',
    },
    'testimonials': {
        'image/jpeg', 'image/jpg', 'image/png',
    },
    'custom_orders': {
        'image/jpeg', 'image/jpg', 'image/png',
        'application/octet-stream',          # STL / OBJ / 3MF
        'model/stl', 'model/obj',
        'application/pdf',
    },
}

# Max file sizes in bytes per category
MAX_SIZES = {
    'products':     5 * 1024 * 1024,    # 5 MB
    'categories':   2 * 1024 * 1024,    # 2 MB
    'testimonials': 2 * 1024 * 1024,    # 2 MB
    'custom_orders': 25 * 1024 * 1024,  # 25 MB
}


def _get_client():
    """Return a boto3 S3 client configured from Django settings."""
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )


class S3Service:
    """Utility class for all S3 operations."""

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    @staticmethod
    def validate_file_type(content_type: str, folder: str) -> bool:
        """
        Validate a MIME type against the whitelist for a given folder.

        Args:
            content_type: MIME type string (e.g. 'image/jpeg')
            folder: S3 sub-folder / upload category ('products', 'custom_orders' …)

        Returns:
            True if allowed, False otherwise
        """
        allowed = ALLOWED_TYPES.get(folder, set())
        return content_type.lower().strip() in allowed

    @staticmethod
    def validate_file_size(file_size_bytes: int, folder: str) -> bool:
        """
        Validate a file size against the limit for a given folder.

        Args:
            file_size_bytes: File size in bytes
            folder: S3 sub-folder / upload category

        Returns:
            True if within limit, False otherwise
        """
        max_size = MAX_SIZES.get(folder, 5 * 1024 * 1024)
        return file_size_bytes <= max_size

    # ------------------------------------------------------------------
    # Core S3 operations
    # ------------------------------------------------------------------

    @staticmethod
    def generate_presigned_upload_url(
        folder: str,
        file_name: str,
        content_type: str,
        expiry_seconds: int = 300,
    ) -> dict:
        """
        Generate a presigned POST URL so the FRONTEND can upload directly
        to S3 without routing the file bytes through the backend.

        The workflow is:
            1. Frontend calls  POST /api/s3/presigned-upload/
            2. Backend validates type/size meta and returns a presigned URL
            3. Frontend uploads the file directly to S3 in the browser
            4. Frontend sends the final S3 URL back to the backend
            5. Backend stores that URL in the database

        Args:
            folder:   Destination sub-folder (e.g. 'products', 'custom_orders')
            file_name: Sanitised filename (e.g. 'planter.jpg')
            content_type: MIME type of the file
            expiry_seconds: How long the presigned URL is valid

        Returns:
            {
                'upload_url': str,       # PUT directly here
                'file_url':   str,       # Public S3 URL to store in DB
                's3_key':     str,       # Key used in S3
            }

        Raises:
            ValueError: if file type is not allowed
            RuntimeError: if presigned URL generation fails
        """
        if not S3Service.validate_file_type(content_type, folder):
            raise ValueError(
                f"File type '{content_type}' is not allowed for folder '{folder}'. "
                f"Allowed types: {ALLOWED_TYPES.get(folder, set())}"
            )

        import uuid
        import os
        ext = os.path.splitext(file_name)[-1].lower()
        unique_name = f"{uuid.uuid4().hex}{ext}"
        s3_key = f"{folder}/{unique_name}"

        bucket = settings.AWS_STORAGE_BUCKET_NAME
        region = settings.AWS_S3_REGION_NAME

        try:
            client = _get_client()
            upload_url = client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': bucket,
                    'Key': s3_key,
                    'ContentType': content_type,
                },
                ExpiresIn=expiry_seconds,
            )

            file_url = (
                f"https://{bucket}.s3.{region}.amazonaws.com/{s3_key}"
            )

            logger.info(f"[S3] Presigned upload URL generated → {s3_key}")

            return {
                'upload_url': upload_url,
                'file_url': file_url,
                's3_key': s3_key,
            }

        except NoCredentialsError:
            logger.error("[S3] AWS credentials not configured")
            raise RuntimeError("AWS credentials are not configured on the server")

        except ClientError as e:
            logger.error(f"[S3] Failed to generate presigned URL: {e}")
            raise RuntimeError(f"Failed to generate upload URL: {e}")

    @staticmethod
    def generate_presigned_read_url(s3_key: str, expiry_seconds: int = 3600) -> str:
        """
        Generate a presigned GET URL for reading a private S3 object.

        Use this for objects that should NOT be publicly accessible
        (e.g. custom order design files).

        Args:
            s3_key: The key of the S3 object
            expiry_seconds: URL validity period

        Returns:
            Presigned GET URL string
        """
        try:
            client = _get_client()
            url = client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': s3_key,
                },
                ExpiresIn=expiry_seconds,
            )
            return url
        except ClientError as e:
            logger.error(f"[S3] Failed to generate presigned read URL for {s3_key}: {e}")
            raise RuntimeError(f"Failed to generate read URL: {e}")

    @staticmethod
    def delete_file(s3_key: str) -> bool:
        """
        Delete a file from S3.

        Args:
            s3_key: The S3 object key to delete

        Returns:
            True on success, False on failure
        """
        try:
            client = _get_client()
            client.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=s3_key,
            )
            logger.info(f"[S3] Deleted object: {s3_key}")
            return True
        except ClientError as e:
            logger.error(f"[S3] Failed to delete {s3_key}: {e}")
            return False

    @staticmethod
    def is_configured() -> bool:
        """Return True if S3 credentials are present in settings."""
        return bool(
            getattr(settings, 'AWS_ACCESS_KEY_ID', '') and
            getattr(settings, 'AWS_SECRET_ACCESS_KEY', '') and
            getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '')
        )
