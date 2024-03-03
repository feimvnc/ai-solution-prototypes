from cmd import PROMPT
from genericpath import exists
import boto3 
import json 
import base64 
import os 

PROMPT_DATA = """
Provide an image of year 2050 when AI robots daning on Golden Gate Bridge 
"""

def main():
    prompt_template = [{"text": PROMPT_DATA, "weight": 1}]
    bedrock = boto3.client(service_name = "bedrock-runtime")
    payload = {
        "text_prompts": prompt_template,
        "cfg_scale": 7.0,    # classfier free guidance, higher number closed tied to text prompt (vs creativity)
        "seed": 0, 
        "steps": 32,
        "width": 512,
        "height": 512
    }

    body = json.dumps(payload)
    model_id = "stability.stable-diffusion-x1-v0"
    response = bedrock.invoke_model(
        body = body, 
        modelId = model_id, 
        accept = "application/json", 
        contentType = "application/json"
    )

    response_body = json.loads(response.get("body").read())
    print(response_body)
    artifact = response_body.get("artifacts")[0]
    image_encoded = artifact.get("base64").encode("utf-8")
    image_bytes = base64.b64decode(image_encoded)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    file_name = f"{output_dir}/generated-img.png"
    with open(file_name, "wb") as f: 
        f.write(image_bytes)


if __name__ == "__main__":
    main()