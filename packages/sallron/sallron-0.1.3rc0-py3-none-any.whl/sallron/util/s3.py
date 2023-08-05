"""Core module for AWS S3 related operations"""
from sallron.util import settings
from functools import wraps
import pickle
import boto3
import os

def _aws_auth(f):

    @wraps(f)
    def decorator(*args, **kwargs):

        if not (settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY_ID and settings.AWS_REGION and settings.LOGGING_BUCKET):
            auth = False
        else:
            auth = True

        return f(auth, *args, **kwargs)
    
    return decorator

@_aws_auth
def get_bucket(aws_auth):
    if aws_auth:
        s3 = boto3.session.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_ID,
            region_name=settings.AWS_REGION,
        ).resource("s3")
        return s3.bucket(settings.LOGGING_BUCKET)
    else:
        print('AWS credentials not set.')
        return None

def send_to_s3(obj_path):
    """
    Utility function to send objects to S3

    Args:
        aws_auth (bool): Boolean indicating whether AWS settings were set or not
        obj_path (str): Path to object to be sent
    """

    # ensure everything needed is set
    if os.path.exists(obj_path):

        bucket = get_bucket()

        try:
            # note it expects a obj_path following path/to/obj.txt format!
            # gets the last name of this sequence
            bucket.upload_file(obj_path, obj_path.split('/')[-1])

            # remove the current log file
            os.remove(obj_path)

    else:
        print('File path not found.')
        pass