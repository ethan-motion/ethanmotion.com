import json
import os
import boto3
from pathlib import Path
from content_types import *

def lambda_handler(event, context):
    print(event['headers'])
    print(event['body'])
    try:
        if(event['headers']['X-GitHub-Event'] == 'release'): # Only action release events
            print("X-GitHub-Event is 'release'")
            if(event['body']['release']['prerelease'] == False): # Production website
                print("pre-release is false")
                buckets = ['ethanmotion.com', 'www.ethanmotion.com']
            elif(event['body']['release']['prerelease'] == True): # Dev website
                print("pre-release is true")
                buckets = ['dev.ethanmotion.com']
        else:
            return "Not a release event. Exiting."
    except Exception as e:
        print(e)
        return "Something went wrong getting the Github release info. Exiting."

    import requests
    owner_repo = 'ethan-motion/personal-website'            # TODO Make this an environment variable
    tree = 'master'                                         # TODO Make this an environment variable

    # Get list of all files in repo
    response = requests.get("https://api.github.com/repos/" + owner_repo + "/git/trees/" + tree + "?recursive=1")
    if(response.ok):
        websiteItems = json.loads(response.text or response.content)
    else:
        return "Failed to get 200 from 'https://api.github.com/repos/" + owner_repo + "/git/trees/" + tree + "?recursive=1'"

    count_total_files = 0
    count_uploaded_files = 0
    count_failed_files = 0
    for file in websiteItems['tree']: # For each file in the repo
        if file['path'].startswith("website"): # Ignore files in other directories
            if file['type'] == 'blob': # Ignore directories (only get files)
                print(' ')
                count_total_files += 1

                #   Get the file from Github into Lambda container /tmp/ dir
                url = "https://raw.githubusercontent.com/" + owner_repo + "/" + tree + "/"+ file['path']
                print("Getting file from: " + url)
                response = requests.get(url, allow_redirects=True)
                lambda_file_path = "/tmp/" + file['path']
                file_name = (os.path.basename(file['path']))
                os.makedirs(os.path.dirname(lambda_file_path), exist_ok=True) # mkdir in Lambda (Linux) if it doesn't exist
                with open(lambda_file_path, "wb") as f:
                    f.write(response.content)

                #   Get the file from Lambda container int S3
                try:
                    s3_path = file['path'].replace('website/','') # (remove 'website' directory for S3)
                    content_type = content_types[Path(lambda_file_path).suffix.lower()]
                    print("Content Type is " + content_type)
                    s3 = boto3.client('s3')
                    for bucket in buckets:
                        content = open(lambda_file_path, 'rb')
                        s3.put_object(
                            Bucket=bucket,
                            Body=content,
                            Key=s3_path,
                            ContentType=content_type
                        )

                    count_uploaded_files += 1
                    print("Uploaded: " + s3_path)
                except Exception as e:
                    count_failed_files += 1
                    print("Failed to upload " + s3_path)
                    print(e)

    return_message = "Uploaded " + str(count_uploaded_files) + "/" + str(count_total_files) + ". " + str(count_failed_files) + " failed."
    return {
        'statusCode': 200,
        'body': json.dumps(return_message)
    }
