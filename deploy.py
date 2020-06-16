import os
import mimetypes
import boto3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

aws_access_key_id = input("Access key: ")
aws_secret_access_key = input("Secret key: ")
repo = "https://github.com/ethan-motion/ethanmotion.com.git"

s3_resource = boto3.resource('s3',
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key
)

s3_client = boto3.client('s3',
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key
)

def main():
    source = input("Local or Git: ")
    environment = input("Dev or Prod: ")
    if environment.lower() == "prod":
        buckets = ['ethanmotion.com', 'www.ethanmotion.com']
    else:
        buckets = ['dev.ethanmotion.com']

    if source.lower() == "local":
        logger.info("Using local")
        os.chdir('website')
    else:
        logger.info("Using git master")
        # make a tmp dir, and clean up after
        # logging.info(f"Cloning master from {repo}")
        # os.system("git clone " + repo)
        # os.chdir('./ethanmotion.com/website')

    # Delete everything from bucket(s)
    for bucket_name in buckets:
        logger.info(f"Deleting objects from {bucket_name}")
        bucket = s3_resource.Bucket(bucket_name)
        bucket.objects.delete()

    # Upload files to bucket(s)
        for file in Path().rglob('*.*'):
            content_type = mimetypes.guess_type(file)
            logger.info(f"Uploading {file} {content_type[0]}")
            content = open(file, 'rb')
            s3_client.put_object(
                Bucket=bucket_name,
                Body=content,
                Key=str(file.as_posix()),
                ContentType=str(content_type[0])
            )

if __name__ == '__main__':
    main()
