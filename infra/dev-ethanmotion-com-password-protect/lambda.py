import json
from base64 import b64encode
import boto3


ssm = boto3.client("ssm", region_name="us-east-1")
encoding = "utf-8"
unauthorized_response = {
    "status": 401,
    "statusDescription": "Unauthorized",
    "body": "Unauthorized",
    "headers": {"www-authenticate": [{"key": "WWW-Authenticate", "value": "Basic"}]},
}


def b64encode_and_stringify(input):
    input_as_bytes = input.encode(encoding)
    input_b64encoded_as_bytes = b64encode(input_as_bytes)
    input_b64encoded_as_string = input_b64encoded_as_bytes.decode(encoding)
    return input_b64encoded_as_string


def get_parameter(name):
    parameter = ssm.get_parameter(Name=name, WithDecryption=True)
    return parameter["Parameter"]["Value"]


def lambda_handler(event, context):
    request = event["Records"][0]["cf"]["request"]
    headers = request["headers"]

    if "authorization" not in headers:
        print("No username/password submitted.")
        return unauthorized_response

    users = get_parameter("dev-ethanmotion-com-users").split(",")
    password = get_parameter("dev-ethanmotion-com-password")

    auth_strings = []
    for user in users:
        credentials_to_encode = f"{user}:{password}"
        auth_string = f"Basic {b64encode_and_stringify(credentials_to_encode)}"
        auth_strings.append(auth_string)

    if headers["authorization"][0]["value"] in auth_strings:
        print("User and password match.")
        return request

    else:
        print("Username or password incorrect.")
        return unauthorized_response
