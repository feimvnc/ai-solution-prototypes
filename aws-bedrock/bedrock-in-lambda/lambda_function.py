# source: https://www.youtube.com/watch?v=7PK4zdUgAt0

import json 
import boto3 

bedrock_runtime = boto3.client("bedrock-runtime", "us-east-1")

def lambda_handler(event, context):

    prompt = "Write an article about the fiction planet Foobar"

    kwargs = {
        "modified": "anthropic.claude-v2",
        "contentType": "application/json",
        "accept": "*/*",
        "body": "{\"prompt\":\"Human: " + prompt + "\\nAssistant:\", \"max_tokens_to_sample\": 200}"
    }

    resp = bedrock_runtime.invoke_model(**kwargs)

    resp_json = json.loads(resp.get('body').read())

    return {
        'statusCode': 200, 
        'body': json.dumps(resp_json)
    }