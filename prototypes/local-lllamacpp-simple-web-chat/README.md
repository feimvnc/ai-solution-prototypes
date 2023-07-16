# Project Title        
        
A Local Simple Web Chat Running in Browser  
      
## Description        
        
Clone the open source llama.cpp source code, build, run it on local CPU.    
Download vicuna 13B model from huggingface    
Run your own local AI agent, help you explore the knowledge world.    
  
Original source and discussion - Simple web chat example: https://github.com/ggerganov/llama.cpp/pull/1998    
  
## Cost and Hardware    
  
Your own PC, minimum 16GB RAM is recommended, 32GB RAM will have better performance    
MacOS is preferred considering it is easy to run "make".    
No GPU, No Internet is required.    
No third party application registration, api keys, or email address is needed.    
  
## Getting Started        
  
First we need to check your PC hardware.  
Because AI inferencing uses lot of CPU to process data, enough RAM and CPU helps.  
  
Open a MacOS terminal, run below commands to check os version, RAM, cpu cores.  
  
A README.txt is available, if you think it is easy to copy and paste commands.

# macOS Monterey Version: 12.4         
$uname -a         
Darwin user-2.local 21.5.0 Darwin Kernel Version 21.5.0: Tue Apr 26 21:08:22 PDT 2022;         
root:xnu-8020.121.3~4/RELEASE_X86_64 x86_64        
  
Check memory   
$top  
PhysMem: 32G used  
  
Check number of cpu cores   
$ sysctl -n  hw.ncpu  
12  
  
  
## Clone the open source llama.cpp source code and build it.  
  
##create a new dir        
cd ~/     # change to home directory  
mkdir vicuna-local       # create a new directory   
cd vicuna-local     # go into the new directory   
  
## clone llama.cpp    # download source code         
git clone https://github.com/ggerganov/llama.cpp.git      
  
## read their README.md         
cd llama.cpp    
  
## check source code branch and logs   
$ git log --oneline  
672dda1 (HEAD -> master, origin/master, origin/HEAD) ggml : fixed runtime bugs and compile errors related to GGML_PERF and GGML_DEBUG (#2219)  
  
## git update new changes   
$ git pull  
  
## Build source code     
Read llama.cpp README.md for helpful information   
   
# check make version   
make -v  
GNU Make 3.81  
  
# build source code   
make   
  
Below are optional if you need.  
make -d   # print lots of debug messages when errors  
make -s   # silent, less messages   
make clean    # delete previously built files   
  
Output:  
...  
====  Run ./main -h for help.  ====  
  
# check newly built files   
-rwxr-xr-x   1 user  staff   740680 16 Jul 21:18 main  
-rwxr-xr-x   1 user  staff   685328 16 Jul 21:18 quantize  
-rwxr-xr-x   1 user  staff   781256 16 Jul 21:18 quantize-stats  
-rwxr-xr-x   1 user  staff   723448 16 Jul 21:18 perplexity  
-rwxr-xr-x   1 user  staff   722896 16 Jul 21:18 embedding  
-rwxr-xr-x   1 user  staff   507784 16 Jul 21:18 vdot  
-rwxr-xr-x   1 user  staff   780760 16 Jul 21:19 train-text-from-scratch  
-rwxr-xr-x   1 user  staff   722800 16 Jul 21:19 simple  
-rwxr-xr-x   1 user  staff  1481032 16 Jul 21:19 server    # -> this will be used  
-rwxr-xr-x   1 user  staff   707912 16 Jul 21:19 libembdinput.so  
-rwxr-xr-x   1 user  staff   722960 16 Jul 21:19 embd-input-test  
(base) user-2:llama.cpp user$   
  
  
## Create a new folder "models" and download vicuna model  
  
Inside llama.cpp root folder, run below commands   
  
mkdir models/13B    # use this to match what source repo uses   
cd model/13B  
  
# download vicuna model          
  
Use wget, which can be installed using brew, google it if you need.  
  
wget https://huggingface.co/vicuna/ggml-vicuna-13b-1.1/resolve/main/ggml-vic13b-uncensored-q5_1.bin        
  
# or manually download model from url, select the model to download         
https://huggingface.co/vicuna/ggml-vicuna-13b-1.1/tree/main        
        
Copy the model file to "models/13B" folder, like below fiile is 8.9GB  
  
$ ls -l models/13B/  
total 17500080  
-rw-r--r--@ 1 user  staff  8950236288 15 Jul 23:22 ggml-vic13b-uncensored-q5_0.bin  
  
# run program, in same llama.cpp root folder         
  
Check built program file   
$ ls -l server   
-rwxr-xr-x  1 user  staff  1481032 16 Jul 21:19 server  
  
Check html javascript files, used to load at server start   
$ ls -l examples/server/public/  
total 88  
-rw-r--r--  1 user  staff   4462 15 Jul 18:08 completion.js  
-rw-r--r--  1 user  staff  10752 15 Jul 18:08 index.html  
-rw-r--r--  1 user  staff  22174 15 Jul 18:08 index.js  
  
Read helpful options   
$ ./server -h  
usage: ./server [options]  
  
options:  
  --host                ip address to listen (default  (default: 127.0.0.1)  
  --port PORT           port to listen (default  (default: 8080)  
  --path PUBLIC_PATH    path from which to serve static files (default examples/server/public)  
  ...  
  
# Start the program   
./server -m models/13B/ggml-vic13b-uncensored-q5_0.bin --path examples/server/public/  
{"timestamp":1689541784,"level":"INFO","function":"main","line":1103,"message":"build info","build":843,"commit":"6e7cca4"}    # -> buildd info   
  
llama server listening at http://127.0.0.1:8080   # host and port  
...  
  
# Open a browser   
http://127.0.0.1:8080/  
  
You will see a webpage - llama.cpp  
  
Some hints:  
Don't trust AI answers, the answers are made up based on data and algorithms.  
You as a human still decide what is right and wrong.  
But there is an AI revolution now, and everyone should learn how to use it to assist us.  
  
Initial load may take little longer, this depends on your PC RAM, CPU speed  
Click Reset when response took long time or no response.  
Check logs on server terminal, segmentation fault may occur, just start the program again.  
Depending on your PC RAM and CPU, program runs and responses very differently.  
  
This is your own AI toy and friend, running on your PC, hassle free, enjoy.  
  
homepage screen - http://127.0.0.1:8080/   
  
![Screenshot](local-llama-simple-web-chat-homepage.png)    
  
chat answer 1  
  
![Screenshot](local-llama-simple-web-chat.png)    
  
chat answer 2  
  
![Screenshot](local-llama-simple-web-chat-2.png)    
