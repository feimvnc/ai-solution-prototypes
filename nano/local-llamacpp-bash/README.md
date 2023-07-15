# Project Title      
      
A bash program interacts local llama.cpp and vicuna.  
'bash' here means linux-like terminal script to run this python program.
      
## Description      
      
llama.cpp is a open source program to run llm application on cpu.   

We run a bash script to have a q&a session on terminal in interactive mode.

This can be a handy digital assistant who can answer general questions, and learn python on MacOS terminal.

## Cost 

Totally Free (no gpu nor internet is required)

## Getting Started      
      
Below commands are tested on MacOS.
      
## open one terminal, run below commands  
  
## check out llama.cpp    # download source code   
git clone https://github.com/ggerganov/llama.cpp.git        

## follow their README.md    
cd llama.cpp  
make    # important, compile to generate binary program to run   

Below are compiled files.
-rw-r--r--   1 user  staff      123 26 Jun 20:18 build-info.h
-rw-r--r--   1 user  staff   532264 26 Jun 20:18 ggml.o
-rw-r--r--   1 user  staff   213944 26 Jun 20:18 llama.o
-rw-r--r--   1 user  staff    52840 26 Jun 20:18 common.o
-rw-r--r--   1 user  staff    42912 26 Jun 20:18 k_quants.o
-rwxr-xr-x   1 user  staff   740776 26 Jun 20:18 main    # -> this is the to use
-rwxr-xr-x   1 user  staff   685904 26 Jun 20:18 quantize

## create models folder and copy model files there in same llama.cpp directory

Download models from this link
https://huggingface.co/vicuna/ggml-vicuna-13b-1.1/tree/main


mkdir models

# model files used in this script (q4 is 4-bit quantization to compress a pretrained language model, the small size uses less machine memory or RAM)

ls -ltr models
total 41317072
-rw-r--r--@ 1 user  staff  13831029888 26 Jun 20:21 ggml-vic13b-uncensored-q8_0.bin
-rw-r--r--@ 1 user  staff   7323305088 26 Jun 20:40 ggml-vic13b-q4_0.bin

# create a shell script to run as interactive mode

# filename

run_vicuna_i.sh 

# file content 

./main -i --interactive-first -r "### Human:" --temp 0 -c 2048 -n -1 --repeat_penalty 1.2 --instruct -m ./models/ggml-vic13b-q4_0.bin

# To see usage, run 
./main -h 

# output (the response in stream mode is good on my 32GB RAM MacOS)

bash-5.1$ ./run_vicuna_i.sh 
main: build = 748 (c824d2e)
main: seed  = 1689422247
llama.cpp: loading model from ./models/ggml-vic13b-q4_0.bin
llama_model_load_internal: format     = ggjt v3 (latest)
llama_model_load_internal: n_vocab    = 32000
llama_model_load_internal: n_ctx      = 2048
llama_model_load_internal: n_embd     = 5120
llama_model_load_internal: n_mult     = 256
llama_model_load_internal: n_head     = 40
llama_model_load_internal: n_layer    = 40
llama_model_load_internal: n_rot      = 128
llama_model_load_internal: ftype      = 2 (mostly Q4_0)
llama_model_load_internal: n_ff       = 13824
llama_model_load_internal: n_parts    = 1
llama_model_load_internal: model size = 13B
llama_model_load_internal: ggml ctx size =    0.09 MB
llama_model_load_internal: mem required  = 9031.70 MB (+ 1608.00 MB per state)
llama_new_context_with_model: kv self size  = 1600.00 MB

system_info: n_threads = 6 / 12 | AVX = 1 | AVX2 = 1 | AVX512 = 0 | AVX512_VBMI = 0 | AVX512_VNNI = 0 | FMA = 1 | NEON = 0 | ARM_FMA = 0 | F16C = 1 | FP16_VA = 0 | WASM_SIMD = 0 | BLAS = 1 | SSE3 = 1 | VSX = 0 | 
main: interactive mode on.
Reverse prompt: '### Human:'
Reverse prompt: '### Instruction:

'
sampling: repeat_last_n = 64, repeat_penalty = 1.200000, presence_penalty = 0.000000, frequency_penalty = 0.000000, top_k = 40, tfs_z = 1.000000, top_p = 0.950000, typical_p = 1.000000, temp = 0.000000, mirostat = 0, mirostat_lr = 0.100000, mirostat_ent = 5.000000
generate: n_ctx = 2048, n_batch = 512, n_predict = -1, n_keep = 2


== Running in interactive mode. ==
 - Press Ctrl+C to interject at any time.
 - Press Return to return control to LLaMa.
 - To return control without starting a new line, end your input with '/'.
 - If you want to submit another line, end your input with '\'.


> Your are an python expert, give 5 advices to a new university graduate who is eager to learn python and AI.
1. Start by learning the basics of Python programming language, including data types, control structures, functions, and modules. This will provide you with a solid foundation for building more advanced applications later on.
2. Learn about machine learning libraries such as scikit-learn, TensorFlow, Keras, etc. These libraries can help you to build intelligent systems that can learn from data and make predictions or decisions based on that data.
3. Practice coding regularly by working on small projects like building a simple web application, creating a script to automate a task, or building a machine learning model for a specific problem. This will help you to develop your skills and build confidence in using Python and AI techniques.
4. Join online communities such as Stack Overflow, Reddit's /r/learnpython community, or GitHub where you can ask questions, share knowledge, and collaborate with other developers. These communities are a great resource for learning new concepts and troubleshooting problems.
5. Stay up-to-date with the latest developments in Python and AI by reading blogs, attending conferences, and following relevant hashtags on Twitter. This will help you to stay current and be better prepared for new opportunities as they arise.


> write a working python snake game code 
Here is an example of a basic Python Snake Game using the Pygame library:
```python
import pygame
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 640, 480
FPS = 30
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
snake = {"x": 320, "y": 240}
direction = {"up": False, "down": False, "left": False, "right": False}
food = {"x": WIDTH // 2 - 15, "y": HEIGHT // 2 + 15}
game_over = False
snake_speed = 60

while not game_over:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            game_over = True
        
    keys = pygame.key.get_pressed()
    
    if keys[K_LEFT]:
        snake["x"] -= snake_speed
    elif keys[K_RIGHT]:
        snake["x"] += snake_speed
    elif keys[K_UP]:
        snake["y"] -= snake_speed
    elif keys[K_DOWN]:
        snake["y"] += snake_speed
    
    if direction["up"] and snake["y"] > 0:
        snake["y"] = 0
        food["y"] += snake_speed // 2
        
    if direction["down"] and snake["y"] < HEIGHT:
        snake["y"] = HEIGHT - 1
    
    if direction["left"] and snake["x"] > 0:
        snake["x"] = 0
        food["x"] -= snake_speed // 2
        
    if direction["right"] and snake["x"] < WIDTH - 15:
        snake["x"] += snake_speed // 2
    
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (snake["x"], snake["y"], 30, 30))
    pygame.draw.rect(screen, RED, (food["x"], food["y"], 15, 15))
    
    if game_over:
        screen.fill(BLACK)
        text = font.render("Game Over! Press Q to Quit.", True, BLACK)
        screen.blit(text, (200, 200))
        
    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()
```
>  




## copy the python code to a script snake.py, let's try 

pip install pygame   # install if not having it 

## diff between vicuna a4 model and fixed version 

$ diff snake_from_response.py  snake.py 
7a8
> RED = (255, 0, 0)
57c58,60
<         text = font.render("Game Over! Press Q to Quit.", True, BLACK)
---
>        #  text = font.render("Game Over! Press Q to Quit.", True, BLACK)
>         text = "Game Over! Press Q to Quit."
>         
63,64c66
< pygame.quit()
< 
---
> pygame.quit()
\ No newline at end of file


## diff between vicuna a8 model and fixed version 

$ diff snake_q8.py  snake_from_response_q8.py
54,71c54
<             pygame.draw.rect(SCREEN, (0, 0, 0), pos[0], (self.speed, self.direction))
< 
< 
< snake = Snake()
< snake.draw()            
< 
< 
< game_over = False
< snake_speed = 60
< 
< while not game_over:
<     for event in pygame.event.get():
<         if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
<             game_over = True
<     snake = Snake()
<     snake.draw()  
<         
<     pygame.display.update()
---
>             pygame.draw.rect(SCREEN, (0, 0, 0), pos[0], (self.speed, self.direction)
\ No newline at end of file


## Summary 
Running local MacOS shell script for llama.cpp with ggml-vic13b-* models in interactive mode, you have a handy digital assistant to learn and code python programs. Though the responses are not 100% perfect, but code template, structure, and flows are helpful.  

Just like OpenAI CEO Sam Altman said, "No one should trust him" and "AI".  AI is a tool to help us and our productivity, human makes decision.  

![Screenshot](no_trust_ai.png)  