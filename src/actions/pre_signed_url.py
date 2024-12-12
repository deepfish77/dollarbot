import json
import boto3
import os
from botocore.exceptions import ClientError

def generate_presigned_url(bucket_name, file_name, expiration=3600):
    """
    Generate a pre-signed URL to share an S3 object for download.

    Args:
        bucket_name (str): The name of the S3 bucket.
        file_name (str): The name of the file to be downloaded.
        expiration (int): Time in seconds for the pre-signed URL to remain valid.

    Returns:
        str: Pre-signed URL as a string. None if error.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': file_name},
            ExpiresIn=expiration
        )
        return response
    except ClientError as e:
        print(f"Error generating pre-signed URL: {e}")
        return None
