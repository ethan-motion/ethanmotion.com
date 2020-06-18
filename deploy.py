import os
import sys
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

cloudfront_client = boto3.client('cloudfront',
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key
)

def main():
    source = input("Local or Git: ")
    environment = input("Dev or Prod: ")
    if environment.lower() == "prod":
        bucket_name = 'ethanmotion.com'
        distribution = 'EM30Y9BEWP31R'
    else:
        bucket_name = 'dev.ethanmotion.com'
        distribution = 'E2N0SDO3M868R'

    if source.lower() == "local":
        logger.info("Using local")
        os.chdir('website')
    else:
        logger.info("Can't use git master yet")
        sys.exit()
        # make a tmp dir, and clean up after
        # logging.info(f"Cloning master from {repo}")
        # os.system("git clone " + repo)
        # os.chdir('./ethanmotion.com/website')

    # Delete everything from bucket
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

    # Invalidate CloudFront cached files
    logger.info(f"Invalidating cache for distribution {distribution}")
    cloudfront_client.create_invalidation(
        DistributionId=distribution,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': [
                    '/*'
                ]
            },
            'CallerReference': 'it_me'
        }
    )


if __name__ == '__main__':
    main()
