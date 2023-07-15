# Project Title      
      
A local python program interacts local llama.cpp web api.  
      
## Description      
      
llama.cpp is a open source program to run llm application on cpu.   

Let's get the fist taste of AI and let AI help to code python.  

## Cost 

Totally Free (if you skip openai playground, which is used for comparison purpose)


## OpenAI Info 
OpenAI price has reduced 10x times in last 18 months (per Sam Altman from tour talk in July 2023).

OpenAI is the AI platform you should try and learn, below is openai pricing info.

https://openai.com/pricing


## Getting Started      
      
This helps to learn using python api to interact with local llm web server.

Two steps are involved on MacOS.

start web server  
run python script 
      
## open one terminal, run below program       
  
## check out llama.cpp    # download source code   
git clone https://github.com/ggerganov/llama.cpp.git        
# follow their README.md    
cd llama.cpp  
make    # important, compile to generate binary program to run   

make server   # important, compile to create web server       

## start web server, you see "server listening  ... 8080..."
./server -m models/ggml-vic13b-q4_0.bin -c 2048      
...      
{"timestamp":1687817876,"level":"INFO","function":"main","line":968,"message":"HTTP server listening","hostname":"127.0.0.1","port":8080}   

## open another terminal, test local curl request, --n-predict N: number of tokens      
      
curl --request POST --url http://localhost:8080/completion --data '{"prompt": "what is the meaning of life?","n_predict": 128}'  

Response
{"content":"\na) 42\nb) To seek happiness and fulfillment\nc) To be a good person and do good deeds\nd) All of the above\n\nAnswer: d) All of the above\n\nExplanation: The meaning of life is subjective, and different people may have different answers to this question. Some may believe that the purpose of life is to seek happiness and fulfillment, while others may think that being a good person and doing good deeds is the key to a fulfilling life. There is no one \"right\" answer to this question, but rather a range","generation_settings":{"frequency_penalty":0.0,"ignore_eos":false,"logit_bias":[],"mirostat":0,"mirostat_eta":0.10000000149011612,"mirostat_tau":5.0,"n_keep":0,"n_predict":128,"penalize_nl":true,"presence_penalty":0.0,"repeat_last_n":64,"repeat_penalty":1.100000023841858,"seed":-1,"stop":[],"stream":false,"temp":0.800000011920929,"tfs_z":1.0,"top_k":40,"top_p":0.949999988079071,"typical_p":1.0},"model":"models/ggml-vic13b-q4_0.bin","prompt":" what is the meaning of life?","stop":true,"stopped_eos":false,"stopped_limit":true,"stopped_word":false,"stopping_word":"","tokens_predicted":128,"truncated":false}  

## env is ready, we can write our python program using curl parameters 

Thought, let's use AI to help to write python code.

## 1 OpenAI (registration is required to use openai playground, it is not free, see https://community.openai.com/t/is-playground-free/18909/11, logankilpatrick
Developer Advocate (OpenAI Staff)), 

used here for comparison against local llama.cpp.

Let's ask OpenAI to write the program for us, so we can improve productivity

Open openai playground to get the python code
https://platform.openai.com/playground/p/default-fix-python-bugs  

SYSTEM: (enter below prompt)
write a python program to send url request to http://localhost:8080/completion and include json data of {"prompt": "what is the meaning of life?"}

Response:
import requests
import json

url = "http://localhost:8080/completion"
data = {"prompt": "what is the meaning of life?"}

response = requests.post(url, json=data)

print(response.text)


# let's add response to start.py and run it, while webserver still running

# Response received in raw format  

$ python start.py   # run script without json parsing

{"content":"\na) To be happy\nb) To serve others\nc) To find true love\nd) 42","generation_settings":{"frequency_penalty":0.0,"ignore_eos":false,"logit_bias":[],"mirostat":0,"mirostat_eta":0.10000000149011612,"mirostat_tau":5.0,"n_keep":0,"n_predict":-1,"penalize_nl":true,"presence_penalty":0.0,"repeat_last_n":64,"repeat_penalty":1.100000023841858,"seed":-1,"stop":[],"stream":false,"temp":0.800000011920929,"tfs_z":1.0,"top_k":40,"top_p":0.949999988079071,"typical_p":1.0},"model":"models/ggml-vic13b-q4_0.bin","prompt":" what is the meaning of life?","stop":true,"stopped_eos":true,"stopped_limit":false,"stopped_word":false,"stopping_word":"","tokens_predicted":26,"truncated":false}


## 2 local llama.cpp + ggml-vic13b-q4_0.bin
## Asked and received below response using command line 

llama.cpp user$ cat ./c
./main -i --interactive-first -r "### Human:" --temp 0 -c 2048 -n -1 --repeat_penalty 1.2 --instruct -m ./models/ggml-vic13b-q4_0.bin

./run_vicuna_i.sh 
... 
 
> write a python program to send url request to http://localhost:8080/completion and include json data of {"prompt": "what is the meaning of life?"}

Response:
The response from the server should be in JSON format, containing two elements: 1) A list of suggested completions for the given prompt (in this case, a list with one element: "42"), and 2) The rank of the best completion among all possible completions. If there are no possible completions or if none have a non-zero rank, then the response should contain an empty list and null as the rank value.
```python
import requests
import json

url = "http://localhost:8080/completion"
data = {"prompt": "what is the meaning of life?"}
response = requests.post(url, data=json.dumps(data))

if response.status_code == 200:
    completion_list = response.json()["suggestions"]
    best_completion_rank = response.json()["best_match_score"]
    print("Suggested completions:", completion_list)
    print("Best completion rank:", best_completion_rank)
else:
    print("Failed to get response from server")
```
> 

Comments: vicuna response included status.code and json.parsing examples, which is good information.  We need to change json key to "content".  

Created start_vicuna.py and add the code.

Below is the output from local llama.cpp using vicuna model, which is good.

$ python start_vicuna.py    # run python script

content: 
|
---|---

**Terence McKenna**: The meaning of life is to live in such a way that you are fulfilling your potential, using your unique gifts and talents to make a positive contribution to the world. It's about finding your purpose, following your bliss, and becoming the best version of yourself that you can be.

**Joseph Campbell**: The meaning of life is to discover and pursue your own personal path, and to find the inner resources and strength to overcome any obstacles along the way. It's about embracing your own unique journey, and using your experiences and challenges to grow and evolve as a person.

**Carl Jung**: The meaning of life is to discover and connect with your own deepest sense of self, and to find meaning and purpose in your life through that connection. It's about exploring the unconscious realms of mind and spirit, and using that knowledge to live a more authentic and fulfilling life.

**Alan Watts**: The meaning of life is to find balance and harmony within yourself and with the world around you. It's about recognizing the interconnectedness of all things, and living in a way that honors and respects the natural order of the universe.


## Summary, we used local AI and OpenAI to write a python script to uses api and connected to local llama.cpp vicuna model, result was good.