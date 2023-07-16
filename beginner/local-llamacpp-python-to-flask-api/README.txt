# Project Title    
    
Run python API to call local API web server and local ai engine 
    
## Description    
    
Write a python program to call local AI API server.  
Use similalr openai API.  
All are built and run on your local PC.  
No open api key, no gpu, no internet is required.
    
## Getting Started    

We will use the env built from local-llamacpp-flask-api.

## Start local llama AI engine

Open a MacOS terminan 
# make sure build llama.cpp first, and you have "server" binary executable 

# make sure the models folder/file exist, and match the command below 
cd llama.cpp
./server -m models/13B/ggml-vic13b-uncensored-q5_0.bin 
# Output  
llama server listening at http://127.0.0.1:8080
{"timestamp":1689511914,"level":"INFO","function":"main","line":1323,"message":"HTTP server listening","hostname":"127.0.0.1","port":8080}


Open another MacOS terminal 

## Start Flask API server 
cd llama.cpp/examples/server

$ python api_like_OAI.py 
 * Serving Flask app 'api_like_OAI'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8081


## Write python script 
You can use visual studio code if you have, or vim other editors 
Python 3.10 or above is recommended, it has enhanced SyntaxError which helps troubleshooting 
(https://docs.python.org/3.10/whatsnew/3.10.html, search SyntaxError)


# make sure install openai, run this on terminal, in your env 
pip install openai
conda install -c conda-forge openai    # for conda  

# open visual studio code from the directory 
code .

# because of using venv, conda, different python versions, you may see message when "import open"
Import openai could not be resolved' error (pylance), in code studio 

Here is how I fixed.
$which python
/Users/user/opt/anaconda3/envs/gpt-local/bin/python

$ python -V
Python 3.11.4

$pip3.11 install openai

Open visual studio, press command+shift+P
enter "python interpreter", select above python path, or where openai is installed.

# create a python file to use 
local_web_api.py 

Code example 1, copy code from openai 

https://platform.openai.com/docs/api-reference/chat/create?lang=python

Note: code below default connects to openai API, just for reference.
```
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)
```

Code example 2, copy code from github openai-python 

https://github.com/openai/openai-python/blob/main/README.md#microsoft-azure-endpoints

We use this code and change openaii_api_key, openai.api_base

```
import openai
# openai.api_type = "azure"   
openai.api_key = "sk-42"      # -> change value
openai.api_base = "http://localhost:8081/"  # -> use http://localhost:8081
# openai.api_version = "2023-05-15"    

# create a chat completion
chat_completion = openai.ChatCompletion.create(deployment_id="deployment-name", model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])

# print the completion
print(openai.__version__)
print(chat_completion.choices[0].message.content)
```

## Complete run outputs, you need 3 terminals (or windows)

# 1. start local ai engine 
$ ./server -m models/13B/ggml-vic13b-uncensored-q5_0.bin 
{"timestamp":1689524727,"level":"INFO","function":"main","line":1103,"message":"build info","build":843,"commit":"6e7cca4"}
...
llama server listening at http://127.0.0.1:8080
...
{"timestamp":1689524727,"level":"INFO","function":"main","line":1323,"message":"HTTP server listening","hostname":"127.0.0.1","port":8080}
...
>>>> "/completion" path was called
{"timestamp":1689524758,"level":"INFO","function":"log_server_request","line":1076,"message":"request","remote_addr":"127.0.0.1","remote_port":61649,"status":200,"method":"POST","path":"/completion","params":{}}

# 2. start local api web server 
$ python local_api_like_OAI.py 
 * Serving Flask app 'local_api_like_OAI'
...
 * Running on http://127.0.0.1:8081
...
>>>> server started 
{'content': ' Hello! How can I help you today?', 'generation_settings': {'frequency_penalty': 0.0, 'ignore_eos': False, 'logit_bias': [], 'mirostat': 0, 'mirostat_eta': 0.10000000149011612, 'mirostat_tau': 5.0, 'model': 'models/13B/ggml-vic13b-uncensored-q5_0.bin', 'n_ctx': 512, 'n_keep': 34, 'n_predict': -1, 'n_probs': 0, 'penalize_nl': True, 'presence_penalty': 0.0, 'repeat_last_n': 64, 'repeat_penalty': 1.100000023841858, 'seed': 4294967295, 'stop': ['</s>'], 'stream': False, 'temp': 0.800000011920929, 'tfs_z': 1.0, 'top_k': 40, 'top_p': 0.949999988079071, 'typical_p': 1.0}, 'model': 'models/13B/ggml-vic13b-uncensored-q5_0.bin', 'prompt': ' A chat between a curious user and an artificial intelligence assistant. The assistant follows the given rules no matter what.\n\nUSER: Hello world\nASSISTANT:', 'stop': True, 'stopped_eos': True, 'stopped_limit': False, 'stopped_word': False, 'stopping_word': '', 'timings': {'predicted_ms': 3379.4230000000002, 'predicted_n': 9, 'predicted_per_second': 2.663176524513208, 'predicted_per_token_ms': 375.4914444444445, 'prompt_ms': 13902.862000000001, 'prompt_n': 9, 'prompt_per_second': 2.4455396306170627, 'prompt_per_token_ms': 408.90770588235296}, 'tokens_cached': 43, 'tokens_evaluated': 34, 'tokens_predicted': 10, 'truncated': False}

>>>> POST request received
127.0.0.1 - - [16/Jul/2023 17:25:58] "POST /engines/deployment-name/chat/completions HTTP/1.1" 200 -

# 3. run python program to call web api server 

$ python local_web_api.py 
>>>> output 
Calling local ai web api, using openai version: 0.27.8

 Hello! How can I help you today?    # response content

FullResponse: {    # full response
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": " Hello! How can I help you today?",
        "role": "assistant"
      }
    }
  ],
  "created": 1689524758,
  "id": "chatcmpl",
  "model": "LLaMA_CPP",
  "object": "chat.completion",
  "truncated": false,
  "usage": {
    "completion_tokens": 10,
    "prompt_tokens": 34,
    "total_tokens": 44
  }
}