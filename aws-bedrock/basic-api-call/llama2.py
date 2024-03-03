import boto3 
import json 

PROMPT_DATA = """
    Act as Charles Darwin and write a phrase on artifitial intelligence evolution.
    """
MODEL_ID = "meta.lllama2-70b-chat-v1"    
MAX_GEN_LEN = 128
TEMP = 0.5   # 0.1 more deterministic output (vs random)
TOP_P = 0.5   # 0.1, only top 10% probability mass are considered

def llama2_chat() -> None:
    bedrock = boto3.client(
        service_name = "bedrock-runtime",
        region_name = "us-east-1"
        )
    payload = {
        "prompt": "[INST]" + PROMPT_DATA + "[/INST]",
        "max_gen_len": MAX_GEN_LEN,
        "temperature": TEMP,
        "top_p": TOP_P
    }

    body = json.dumps(payload)

    response = bedrock.invoke_model(
        body = body,
        model_id = MODEL_ID,
        accept = "application/json",
        contentType = "application/json"
    )

    response_body = json.loads(response.get("body").read())
    response_text = response_body['generation']
    print(response_text)

def main() -> None: 
    llama2_chat()

if __name__ == "__main__":
    main()


