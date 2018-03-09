import boto3
import json
import os

from collections import defaultdict

bucket = os.getenv('CONFIG_S3_BUCKET')
key = os.getenv('CONFIG_S3_KEY')
config = None
if bucket and key:
    resp = boto3.client('s3').get_object(Bucket=bucket, Key=key)
    config = json.load(resp['Body'])
else:
    mode = os.environ['MODE'] if 'MODE' in os.environ else 'local'
    config_file_location = defaultdict(lambda: 'config/local.config.json')
    config_file_location = {
        'test': 'config/test.config.json',
        'development': 'config/development.config.json',
        'staging': 'config/staging.config.json',
        'production': 'config/production.config.json',
        'local': 'config/local.config.json',
    }[mode]
    with open(os.path.join(os.getcwd(), config_file_location)) as f:
        config = json.load(f)
