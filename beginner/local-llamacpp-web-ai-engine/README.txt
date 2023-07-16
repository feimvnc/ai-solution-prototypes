# Project Title  
  
Run local AI webserver using llama.cpp with vicuna model, without GPU nor internet.
  
## Description  
  
To develop AI application, we need a local development environment.
llama.cpp is an open source program running on CPU hardware.
vicuna 13b model match 90% of GPT-4
Let's build this local ai engine on your local PC.  
  
## Getting Started  
  
To help the program running properly on local MacOS or PC, it is recommended to have a large RAM, enough disk space, multiple core CPUs.  Low hardware configuration will slow the program performance.  Time is money, think about an upgrade if required.

## CPU, RAM, Nvidia GPU, Internet, OpenAI
The programs tested on following hardware. When asked AI to answer questions, you will hear machine fans play noises, this is normal because AI is working hard to compute and find best answers for you.

MacBookPro: 2018
macOS Monterey Version: 12.4   
CPU: 6 cores  (No Nvidia GPU)
RAM: 32 GB 

Nvidia GPU (cuda), Internet, OpenAI are not required.

## uname -a   
Darwin user-2.local 21.5.0 Darwin Kernel Version 21.5.0: Tue Apr 26 21:08:22 PDT 2022;   
root:xnu-8020.121.3~4/RELEASE_X86_64 x86_64  
  
## create a new folder for the program
cd ~/Document
mkdir vicuna-local  
cd vicuna-local

## download llama.cpp source code, you can open link to see details 
git clone https://github.com/ggerganov/llama.cpp.git    
cd llama.cpp/
$ git branch 
* master    # check master branch is active 

## compile source code  
If error, please follow message and google to install dependencies and librares
Ignore warning 

$ make 

Check server binary is created
$ ls -l server 
-rwxr-xr-x  1 user  staff  1399024 26 Jun 23:16 server

## create a folder to save model files 
llama.cpp only load ggml model files ending ".bin", other models files do not work, e.g. pytorch.

Download vicuna models, this works well on cpu, inferencing time is acceptable or good if you have 16GB or 32GB RAM.

## select the model to download
https://huggingface.co/vicuna/ggml-vicuna-13b-1.1/tree/main  

mkdir models   ## create new folder inside llama.cpp folder, where compiled "main" is created.
cd models   # download language model  
wget https://huggingface.co/vicuna/ggml-vicuna-13b-1.1/resolve/main/ggml-vic13b-q4_0.bin  
    
## run ai web engine 
In the same llama.cpp folder, let's check server run options 
$ ./server -h
usage: ./server [options]

options:
  -h, --help            show this help message and exit
  -c N, --ctx-size N    size of the prompt context (default: 512)
  -m FNAME, --model FNAME
                        model path (default: models/7B/ggml-model.bin)
  --host                ip address to listen (default  (default: 127.0.0.1)
  --port PORT           port to listen (default  (default: 8080)
  -to N, --timeout N    server read/write timeout in seconds (default: 600)
  --embedding           enable embedding vector output (default: disabled)
...


## Start AI web engine, we use default values to make it simple 
./server -m models/ggml-vic13b-q4_0.bin -c 4096

Or 

Create a script to include above command line 
$ cat <<EOF > run.sh
./server -m models/ggml-vic13b-q4_0.bin -c 4096
EOF

$ ./run_vicuna_web.sh 
{"timestamp":1689445846,"level":"INFO","function":"main","line":797,"message":"build info","build":748,"commit":"c824d2e"}
...
{"timestamp":1689445846,"level":"INFO","function":"main","line":968,"message":"HTTP server listening","hostname":"127.0.0.1","port":8080}


## let's make api calls 

curl is a command line which can interact with web server api endpoints using HTTP GET, POST, PUT, DELETE.

Health check.
We need to open another terminal, check server is running and responding.
$ curl http://localhost:8080
<h1>llama.cpp server works</h1>

On web server terminal, we can see request logs.
{"timestamp":1689446038,"level":"INFO","function":"log_server_request","line":775,"message":"request","remote_addr":"127.0.0.1","remote_port":59009,"status":200,"path":"/","request":"","response":"<h1>llama.cpp server works</h1>"}

Let's include a question.  
curl --request POST \
     --url http://localhost:8080/completion \
     --data '{"prompt": "Will AI replace human jobs?","n_predict": 128}'   

Output:
$ curl --request POST \
>      --url http://localhost:8080/completion \
>      --data '{"prompt": "Will AI replace human jobs?","n_predict": 128}' 
{"content":" Yes, it will. But not all jobs are equally susceptible to automation, and some may even become more valuable in a world where machines can do many tasks that are currently performed by humans.\n\nSome estimates suggest that as much as 40 percent of the workforce could be displaced by robots and artificial intelligence over the next few decades. However, this is not a foregone conclusion. The speed at which AI will displace jobs depends on many factors, such as government policies, technological advancements, and the availability of cheap labor in certain industries.\n\nIt","generation_settings":{"frequency_penalty":0.0,"ignore_eos":false,"logit_bias":[],"mirostat":0,"mirostat_eta":0.10000000149011612,"mirostat_tau":5.0,"n_keep":0,"n_predict":128,"penalize_nl":true,"presence_penalty":0.0,"repeat_last_n":64,"repeat_penalty":1.100000023841858,"seed":-1,"stop":[],"stream":false,"temp":0.800000011920929,"tfs_z":1.0,"top_k":40,"top_p":0.949999988079071,"typical_p":1.0},"model":"models/ggml-vic13b-q4_0.bin","prompt":" Will AI replace human jobs?","stop":true,"stopped_eos":false,"stopped_limit":true,"stopped_word":false,"stopping_word":"","tokens_predicted":128,"truncated":false}

## Note: 

Becuase above curl does not use stream mode, it may take some time to see response all at once.  On my MacOS it took 35-40 seconds to receive full response all at once.


curl --request POST \
      --silent \
      --no-buffer \
      --header "Content-Type: application/json" \
      --url http://localhost:8080/completion \
      --data-raw '{"prompt": "Will AI replace human jobs?","n_predict": 128, "stream": true}'  


## a better curl script from llama.cpp repo 
https://github.com/ggerganov/llama.cpp/tree/master/examples/server

download chat.sh 
chmod 755 chat.sh
./chat.sh   # make sure web ai engine server is running

$ ./chat.sh 
> what is number 42?
 In mathematics and science fiction, 42 is often used as an arbitrary or significant number. However, it has no inherent meaning or significance beyond what we assign to it.

> why elon musk still work even he is the richest person in the world
 Elon Musk is a highly driven and ambitious entrepreneur who is passionate about his work. He has stated publicly that he believes work is the most important aspect of life, and he enjoys the process of creating new things and solving problems. Additionally, he has a number of long-term goals and projects that he is working on, such as colonizing Mars and reducing the world's dependence on fossil fuels, which keep him motivated. Finally, it's worth noting that wealth alone does not necessarily bring happiness or fulfillment, and many people find meaning and purpose in their work regardless of their financial situation.