import os
import base64
import boto3
import json
import mimetypes
from botocore.exceptions import ClientError
from src.s3_file_uploader import upload_file_to_s3


def upload_file_to_s3_handler(event, _):
    """
    AWS Lambda handler to handle file uploads via API Gateway.
    """
    try:
        # Retrieve the bucket name from environment variables
        bucket_name = os.environ["BUCKET_NAME"]

        # Parse the request body
        body = json.loads(event.get("body", "{}"))
        file_content = body.get("fileContent")  # Base64 encoded file content
        file_name = body.get("fileName")  # Desired file name in S3

        if not file_content or not file_name:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"error": "Missing fileContent or fileName in the request body"}
                ),
            }

        # Determine content type automatically (optional)
        content_type, _ = mimetypes.guess_type(file_name)

        # Upload the file to S3
        success, response = upload_file_to_s3(
            bucket_name, file_content, file_name, content_type
        )

        if success:
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {"message": "File uploaded successfully", "fileName": file_name}
                ),
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps(
                    {"error": "File upload failed", "details": response}
                ),
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)}),
        }


