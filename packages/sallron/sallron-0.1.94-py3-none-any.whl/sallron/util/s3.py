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
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_ID
        ).resource("s3", region_name=settings.AWS_REGION)
        return s3.Bucket(settings.LOGGING_BUCKET)

    else:
        print('AWS credentials not set.')
        return None

def send_to_s3(obj_paths):
    """
    Utility function to send objects to S3

    Args:
        aws_auth (bool): Boolean indicating whether AWS settings were set or not
        obj_path (str): Path to object to be sent
    """

    bucket = get_bucket()

    for obj_path in obj_paths:
        # ensure everything needed is set
        if os.path.exists(obj_path):

            try:
                # note it expects a obj_path following path/to/obj.txt format!
                # gets the last name of this sequence
                bucket.upload_file(obj_path, obj_path.split('/')[-1])
                # remove the current log file
                os.remove(obj_path)
                print('Files successfully sent to S3.')
            except Exception as e:
                print(e)
                print(obj_path)
                pass

        else:
            print('File path not found.')
            pass