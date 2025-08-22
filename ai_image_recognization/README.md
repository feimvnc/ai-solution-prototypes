```
bash
ollma pull llava:7b

pip install ollama

# code 
import ollama 
res = ollama.chat(
    model = 'llava:7b',
    messages = [
        {
            'role': 'user',
            'content': 'Describe this image in one sentence',
            'images': ['./image1.jpg']
        }
    ]
)

print(res['message']['content'])

robloc 640776 5579
7554540000

drive innovation and modern approach
user centric approach
solve core problem (consistent architecture designing, validation standars)
discovery of information

ax - tools, modern tools, catalog, 
built natively
c4 modeling prnciples diagrams
l1, how system contacts , interact with outside world
l2, breakdown down to individual container part, interact with itself 
l3, container interactive itself, 1:1 mapping, application module in seal
l4, code 
context, component, container, code, small parts of the component
architecture dsl
allow us to ensure arch diagram is correct,and reflect the data
discoverd diagram
l1. application interact with other app api
l2. container, micro interact self serivices
l3. component level, container itself interactive 
logical group containers

