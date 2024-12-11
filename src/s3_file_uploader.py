import os
import base64
import boto3
import json
from botocore.exceptions import ClientError

s3 = boto3.client("s3")


def create_folder_and_generate_upload_url(bucket_name, original_folder, new_folder):
    """
    Create a new folder under an original folder in S3 and return the upload URL.

    Args:
        bucket_name (str): The name of the S3 bucket.
        original_folder (str): The name of the original folder.
        new_folder (str): The name of the new folder to create under the original folder.

    Returns:
        tuple: (bool, str) A tuple where the first value indicates success and the second value is the upload URL.
    """
    try:
        # Construct the new folder path
        if not original_folder.endswith("/"):
            original_folder += "/"
        if not new_folder.endswith("/"):
            new_folder += "/"
        new_folder_path = f"{original_folder}{new_folder}"

        # Create the new folder in S3 by uploading an empty object
        s3.put_object(Bucket=bucket_name, Key=new_folder_path)

        # Generate the upload URL
        upload_url = f"https://{bucket_name}.s3.amazonaws.com/{new_folder_path}"

        return True, upload_url
    except Exception as e:
        print(f"Error: {e}")
        return False, None


def upload_file_to_s3(bucket_name, file_content, file_name, content_type=None):
    """
    Uploads a file to an S3 bucket, handling various file types including images and videos.

    Args:
        bucket_name (str): The S3 bucket name.
        file_content (str): Base64 encoded content of the file.
        file_name (str): The desired name of the file in S3.
        content_type (str): The MIME type of the file (e.g., 'image/png', 'video/mp4'). Optional.

    Returns:
        tuple: (bool, dict) A tuple where the first value indicates success, and the second value contains the S3 response or None.
    """
    try:
        # Decode the Base64 content
        decoded_file = base64.b64decode(file_content)

        # S3 upload options
        upload_args = {"Bucket": bucket_name, "Key": file_name, "Body": decoded_file}

        # Add ContentType if provided
        if content_type:
            upload_args["ContentType"] = content_type

        # Upload the file to S3
        s3_response = s3.put_object(**upload_args)

        return True, s3_response

    except ClientError as e:
        print(f"ClientError: {e}")
        return False, None
    except base64.binascii.Error as e:
        print(f"Base64 decoding error: {e}")
        return False, None
    except Exception as e:
        print(f"General error: {e}")
        return False, None
