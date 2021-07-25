import os
import sys
import mimetypes
import boto3
import requests
import shutil
import zipfile
import time
import io
from pathlib import Path

aws_access_key_id = input("Access key: ")
aws_secret_access_key = input("Secret key: ")
master_zip_url = "https://github.com/ethan-motion/ethanmotion.com/archive/refs/heads/master.zip"

s3_resource = boto3.resource("s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

s3_client = boto3.client("s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

cloudfront_client = boto3.client("cloudfront",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)


def main():
    source = input("Source - Local or Master: ").lower()
    if source not in ["local", "master"]:
        print("Source must be 'Local' or 'Master'")
        sys.exit()

    env = input("Environment - Dev or Prod: ").lower()
    if env not in ["dev", "prod"]:
        print("Environment must be 'Dev' or 'Prod'")
        sys.exit()

    if env == "prod":
        bucket_name = "ethanmotion.com"
        distribution = "EM30Y9BEWP31R"
    else:
        bucket_name = "dev.ethanmotion.com"
        distribution = "E2N0SDO3M868R"

    if source == "master":
        print("Using Github master")
        r = requests.get(master_zip_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall("temp")
        os.chdir("temp/ethanmotion.com-master/website")
    else:
        print("Using local")
        os.chdir("website")

    # Delete everything from bucket
    print(f"Deleting objects from {bucket_name}")
    bucket = s3_resource.Bucket(bucket_name)
    bucket.objects.delete()

    # Upload files to bucket(s)
    for file in Path().rglob("*.*"):
        content_type = mimetypes.guess_type(file)
        print(f"Uploading {file} {content_type[0]}")
        content = open(file, "rb")
        s3_client.put_object(
            Bucket=bucket_name,
            Body=content,
            Key=str(file.as_posix()),
            ContentType=str(content_type[0]),
        )
        content.close()

    # Delete temp files for Master deployment
    if source == "master":
        os.chdir("..\\..\\..\\")
        print("Deleting temp cloned Master files")
        shutil.rmtree("temp")

    # Invalidate CloudFront cached files
    print(f"Invalidating cache for distribution {distribution}")
    cloudfront_client.create_invalidation(
        DistributionId=distribution,
        InvalidationBatch={
            "Paths": {"Quantity": 1, "Items": ["/*"]},
            "CallerReference": "it_me",
        },
    )


if __name__ == "__main__":
    main()
