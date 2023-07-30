# guidance role tag, using chat based model 
# 1. Role setting, "Assumign the role of xyz, advise me on ..."
# 2. Step by step (train/chain of thoughts)

import random    
from dotenv import load_dotenv 
import guidance

load_dotenv()

# change from text based model "text-davinci-003" to 
# chat based model "gpt-3.5-turbo", this has better performance 

# llm to control the whole program 
guidance.llm = guidance.llms.OpenAI("gpt-3.5-turbo")

# define another llm for chat only, can be different
chat = guidance.llms.OpenAI("gpt-3.5-turbo")

# use huggingface open source model 
# guidance.llm = guidance.llms.Transformers(
#     "stabilityai/stablelm-base-alpha-3b", device="cpu"   
# or  7b "stabilityai/stablelm-base-alpha-7b"
# )

# in the context of role tag based model 
program =  guidance(
    """
    {{#system}} You are a CS professor teaching {{os}} systems administration to your students.
    {{/system}}

    {{#user~}}
    What are the some of the most common commands used in the {{os}} operating system? Provide a one-liner description.
    List the commands and their descriptions one per lne.  Number them starting from 1.
    {{~/user}}

    {{#assistant}}
    {{gen 'commands' max_tokens=100}}
    {{/assistant}}

    {{#user}}
    Which among these commands are beginners most likely to get wrong? Explain why the command might be confusing.
    {{/user}}

    {{#assistant}}
    {{gen 'confusing_commands' max_tokens=60}}
    {{/assistant}}
    """,
    llm=chat,
)

result = program(os='Linux')
print(result)

