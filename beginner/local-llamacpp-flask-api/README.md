# Project Title    
    
Run local AI engine and python flask API server   
    
## Description    
    
Here we introduce a middle tier API server which connects to AI engine.  
The API server servers API calls.  
All are built on your local PC.    
    
## Getting Started    
  
Reference information, API like OAI  
https://github.com/ggerganov/llama.cpp/tree/master/examples/server  
  
Above page has good information.  
Butt detailed steps are explained here to help you set up.  
  
## Pre-requisite, New llama.cpp commit is used to included the latest new functionaliy added   
Local llama.cpp builds are required to run as backend AI engine.  
llama.cpp   
  
## New model used - vicuna/ggml-vic13b-uncensored-q5_0.bin   
https://huggingface.co/vicuna/ggml-vicuna-13b-1.1/tree/main  
ggml-vic13b-uncensored-q5_0.bin	   
size: 8.95GB  
  
This models is able to answer date, time correctly, better than ggml-vic13b-q4_0.bin, like to give it a try.  
  
mkdir -p models/13B   ## create new folder inside llama.cpp folder, where compiled "main" is created.  
cd models/13B   # download language model    
wget https://huggingface.co/vicuna/ggml-vicuna-13b-1.1/tree/main/ggml-vic13b-uncensored-q5_0.bin	  
  
-rw-r--r--@ 1 user  staff  8950236288 15 Jul 23:22 ggml-vic13b-uncensored-q5_0.bin  
  
Please insall "wget" if you have "no wget found" message.  
  
# New llama.cpp clone and build on MacOS terminal (as of 16 July 2023)  
$cd ~   # you can change this to any other folder if you like, here to make it easy to learn  
$mkdir vicuna-local  
$git clone https://github.com/ggerganov/llama.cpp.git  
$git reflog  # output below, you can see the commit hash  
6e7cca4 (HEAD -> master, tag: master-6e7cca4, origin/master, origin/HEAD) HEAD@{0}: clone: from https://github.com/ggerganov/llama.cpp.git  
$ git pull  
Already up to date.  
  
Build the code   
$pwd    # check curren path   
/Users/user/vicuna-local/llama.cpp  
  
$make -v    # make version  
GNU Make 3.81  
Copyright (C) 2006  Free Software Foundation, Inc.  
This program built for i386-apple-darwin11.3.0  
  
$make clean   # clean previous build if you like  
$make    # let's build, ignore warnings for now  
  
$ls -ltr     # check compiled executables, look for 2 files we need  
-rw-r--r--   1 user  staff      123 16 Jul 08:33 build-info.h  
-rw-r--r--   1 user  staff   540904 16 Jul 08:33 ggml.o        
-rw-r--r--   1 user  staff   209560 16 Jul 08:33 llama.o  
-rw-r--r--   1 user  staff    56208 16 Jul 08:33 common.o  
-rw-r--r--   1 user  staff    42912 16 Jul 08:33 k_quants.o  
-rwxr-xr-x   1 user  staff   740680 16 Jul 08:33 main     # -> main program, we need   
-rwxr-xr-x   1 user  staff   685328 16 Jul 08:33 quantize  
-rwxr-xr-x   1 user  staff   781256 16 Jul 08:33 quantize-stats  
-rwxr-xr-x   1 user  staff   723448 16 Jul 08:33 perplexity  
-rwxr-xr-x   1 user  staff   722896 16 Jul 08:33 embedding  
-rwxr-xr-x   1 user  staff   507784 16 Jul 08:34 vdot  
-rwxr-xr-x   1 user  staff   780760 16 Jul 08:34 train-text-from-scratch  
-rwxr-xr-x   1 user  staff   722800 16 Jul 08:34 simple  
-rwxr-xr-x   1 user  staff  1481032 16 Jul 08:34 server     # -> ai web engine, we need   
-rwxr-xr-x   1 user  staff   707912 16 Jul 08:34 libembdinput.so  
-rwxr-xr-x   1 user  staff   722960 16 Jul 08:34 embd-input-test  

  
There is a script already provided, let use it.  
cd examples    # change the folder   
cp chat-13B.sh chat-13B.sh.bak     # make a backup   
open chat-13B.sh, change line 7 like below, make sure you have   

$diff  chat-13B.sh chat-13B.sh.bak  
7c7  
< MODEL="${MODEL:-./models/13B/ggml-vic13b-uncensored-q5_0.bin}"  
---  
> MODEL="${MODEL:-./models/13B/ggml-model-q4_0.bin}"  
  
## What is new?   
llama.cpp code and build (new features)  
model is used ./models/13B/ggml-vic13b-uncensored-q5_0.bin  (can answer today's date and time)  
prompt template is used (provide more context to improve answer quality, user experience)  
user_name, ai_name are used (personal customization)  
token context size (defaul 2048, half size of A4 paper)  
out of box script, to have colorful output (ready to use, color output)  
  
## run ai engine to test build   
Because of new features, model, prompt context, it takes 1 minute to load and for you to type question.  You should see the following.  
  
/Users/user/vicuna-local/llama.cpp/examples  
bash-5.1$ ./chat-13B.sh  
main: build = 843 (6e7cca4)  
main: seed  = 1689494956  
llama.cpp: loading model from ./models/13B/ggml-vic13b-uncensored-q5_0.bin  
...  
USER: Name a color.  
ChatLLaMa: Blue.  
USER: What time is it?  
ChatLLaMa: It is 09:09.     # current time, dynamic content, not static content   
USER:     # -> enter your question here   
  
USER: what is today's currency exchange between u.s. dollar against pound  
ChatLLaMa: As of March 26th, 2023, one US Dollar (USD) is equal to 0.74 Pounds (GBP).  
### we can see the data used to train the model was March 26th, 2023  
  
USER: when did elon musk announced x.ai company?  
ChatLLaMa: Elon Musk founded X.ai, an artificial intelligence startup that focuses on scheduling meetings and appointments, in May 2018.     
### Answer is wrong, the date should be July 12, 2023 (7+12+23=42, answer to universe)  
  
Test is completed, Ctrl+C to terminate the program.  
  
If above works, let's move to setup ai api engine and flask.  
  
## Setup backend ai engine   
open a new MacOS terminal   
$cd llama.cpp    # inside the root folder, run below command   
$./server -m models/13B/ggml-vic13b-uncensored-q5_0.bin   
...  
llama server listening at http://127.0.0.1:8080    # ai web engine is up   
  
Do a health check on another terminal  
$ curl http://127.0.0.1:8080   
<html>  
...  
  <title>llama.cpp - chat</title>    # client received data   
  
On ai web engine terminal, you see 200 status code (success)  
{"timestamp":1689496295,"level":"INFO","function":"log_server_request","line":1076,"message":"request","remote_addr":"127.0.0.1","remote_port":60411,"status":200,"method":"GET","path":"/","params":{}}  
  
  
## Setup API Flask server  
This python Flask server connects to backend ai web engine, and use API calls to interact with questions and answers.  
This API Flask server runs on different port 8081.  
  
Leave the ai web engine terminal open and let it running, this is required.  
change to below direcory  
$cd llama.cpp/examples/server  
  
Run below command   
$python api_like_OAI.py     
 * Serving Flask app 'api_like_OAI'  
...  
 * Running on http://127.0.0.1:8081    # -> api server running on port 8081  
  
Do health check, open another terminal.  
You should have 3 terminals now  
1. ai web engine on port 8080  
2. Flask api server on port 8081  
3. to run curl    # we run commands here now  
  
We will use OpenAI API to test   
Open this link, copy the "Create chat completion", "Example request"  
https://platform.openai.com/docs/api-reference/chat/create  
  
### Don't run it, below command fails and it connects to openai with openai_api_key  
curl https://api.openai.com/v1/chat/completions \     # -> change https and hostname  
  -H "Content-Type: application/json" \  
  -H "Authorization: Bearer $OPENAI_API_KEY" \  
  -d '{  
    "model": "gpt-3.5-turbo",  
    "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}]  
  }'  
  
### Below first line changed, we replaced with local api server - http://localhost:8081  
Run it on the third terminal  
  
curl http://localhost:8081/v1/chat/completions \  
  -H "Content-Type: application/json" \  
  -H "Authorization: Bearer $OPENAI_API_KEY" \  
  -d '{  
    "model": "gpt-3.5-turbo",  
    "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}]  
  }'    
  
Output:  
  
{"choices":[{"finish_reason":"stop","index":0,"message":{"content":" Hello! How can I assist you today?","role":"assistant"}}],"created":1689500544,"id":"chatcmpl","model":"LLaMA_CPP","object":"chat.completion","truncated":false,"usage":{"completion_tokens":10,"prompt_tokens":50,"total_tokens":60}}  
  
Try again and ask what is today's weather  
  
$ curl http://localhost:8081/v1/chat/completions \  
>   -H "Content-Type: application/json" \  
>   -H "Authorization: Bearer $OPENAI_API_KEY" \  
>   -d '{  
>     "model": "gpt-3.5-turbo",  
>     "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is the current time in San Franscisco"}] }'  
  
Output   
  
{"choices":[{"finish_reason":"stop","index":0,"message":{"content":" As of my records, it is 13:00 (Pacific Time) in San Francisco.","role":"assistant"}}],"created":1689501185,"id":"chatcmpl","model":"LLaMA_CPP","object":"chat.completion","truncated":false,"usage":{"completion_tokens":24,"prompt_tokens":59,"total_tokens":83}}  
  
### issues you may face  
build llama.cpp failed, try google and find solutions to install, upgrade libraries  
api server not responding, make sure   
  1) ai web engine running on port 8080  
  2) python flask api server running on port 8081  
change openai api curl command to connect to http://localhost:8081  
curl command failed, often due to new line char at end of line, try put all in one line  
no additional change is required following above command  
trust yourself, use your own skills to try and fx issue  
  
## Summary  
clone llama.cpp latest repo  
download new model   
started ai web engine using compiled program "server"  
started example/server/api_like_OAI.py as flask api server   
use curl to test api request   
  
Keep this env setup, we will use it in future solutions.  
  
