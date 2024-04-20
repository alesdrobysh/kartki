import boto3

from config import config

def get_db():
    # local server + cloud db
    if config.AWS_ACCESS_KEY_ID and config.AWS_SECRET_ACCESS_KEY and config.AWS_REGION:
        return boto3.resource(
            'dynamodb',
            region_name=config.AWS_REGION,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )
    
    # cloud server
    return boto3.resource('dynamodb')
