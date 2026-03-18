import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from werkzeug.utils import secure_filename
import secrets

def init_cloudinary():
    """Initialize Cloudinary configuration"""
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    if not all([cloud_name, api_key, api_secret]):
        raise Exception("Cloudinary environment variables not set properly")
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )

def upload_to_cloudinary(file, folder="hostelconnect", resource_type="auto"):
    """
    Upload file to Cloudinary

    Args:
        file: File object from Flask request
        folder: Cloudinary folder name
        resource_type: auto, image, video, raw

    Returns:
        dict: Upload result with secure_url, public_id, etc.
    """
    try:
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{secrets.token_hex(8)}_{filename}"

        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file,
            folder=folder,
            public_id=unique_filename.rsplit('.', 1)[0],  # Remove extension for public_id
            resource_type=resource_type,
            # Additional options for optimization
            quality="auto",
            fetch_format="auto"
        )

        return {
            'success': True,
            'url': upload_result['secure_url'],
            'public_id': upload_result['public_id'],
            'filename': filename,
            'size': upload_result.get('bytes', 0),
            'format': upload_result.get('format', '')
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def delete_from_cloudinary(public_id, resource_type="image"):
    """
    Delete file from Cloudinary

    Args:
        public_id: Cloudinary public ID
        resource_type: image, video, raw

    Returns:
        dict: Deletion result
    """
    try:
        result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        return {
            'success': True,
            'result': result
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_cloudinary_url(public_id, transformation=None):
    """
    Generate Cloudinary URL for a public ID

    Args:
        public_id: Cloudinary public ID
        transformation: Optional transformation parameters

    Returns:
        str: Cloudinary URL
    """
    if transformation:
        return cloudinary.utils.cloudinary_url(public_id, **transformation)[0]
    else:
        return cloudinary.utils.cloudinary_url(public_id)[0]