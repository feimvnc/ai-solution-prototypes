# source from: https://github.com/openai/openai-python/tree/main#microsoft-azure-endpoints
# changed:
# openai.api_key = "sk-42"
# openai.api_base = "http://localhost:8081/"
# print(openai.__version__)
#
# openai api version: 0.27.8
#
# notes: chat_completion create() arguments must match routes defined in local_api_like_OAI.py
# route "/engines/deployment-name/chat/completions", otherwise you see 404 not found error 
# "POST /v1/chat/completions/engines/deployment-name/chat/completions HTTP/1.1" 404

import openai
# openai.api_type = "azure"   
openai.api_key = "sk-42"      # -> change value
openai.api_base = "http://localhost:8081/"  # -> use http://localhost:8081
# openai.api_version = "2023-05-15"    

print(f"Calling local ai web api, using openai version: {openai.__version__}\n")
# create a chat completion
chat_completion = openai.ChatCompletion.create(deployment_id="deployment-name", model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])

# print the completion
print(chat_completion.choices[0].message.content)

# print full response 
print(f"\nFullResponse: {chat_completion}")

chat_completion = openai.ChatCompletion.create(deployment_id="deployment-name", model="gpt-3.5-turbo", stream="True", messages=[{"role": "user", "content": "Who is Paul Graham? Summarize his book Painters and Hackers"}])

# print the completion
print(chat_completion.choices[0].message.content)

# print full response 
#print(f"\nFullResponse: {chat_completion}")