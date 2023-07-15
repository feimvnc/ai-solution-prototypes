import requests
import json

url = "http://localhost:8080/completion"
data = {"prompt": "what is the meaning of life?"}
response = requests.post(url, data=json.dumps(data))

if response.status_code == 200:
    completion_list = response.json()["content"]
    print("content:", completion_list)
else:
    print("Failed to get response from server")