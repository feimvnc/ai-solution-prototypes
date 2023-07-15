import requests
import json

url = "http://localhost:8080/completion"
data = {"prompt": "what is the meaning of life?"}

response = requests.post(url, json=data)

print(response.text)