import random 
from dotenv import load_dotenv 
import guidance

load_dotenv()

# open source model 
guidance.llm = guidance.llms.Transformers(
    "stabilityai/stablelm-base-alpha-3b", device="cpu"
    # "stabilityai/stablelm-base-alpha-7b"    # the other model 
)

program = guidance('''The link is <a href="http:{{gen max_tokens=10 token_healing=False}}''')
result = program(echo=True)
print(result)

# program = guidance("""This is a sentence about {{gen "completion" stop="."}}""")
# executed_program = program(echo=True)
# print(executed_program)



# use chat for partial question and answers 
# chat = guidance.llms.Transformers("stabilityai/stablelm-base-alpha-3b", device="cpu")
# guidance.llm = chat 

# use OpenAI for chat and performance 
# guidance.llm = guidance.llms.OpenAI("gpt-3.5-turbo")

# guidance uses two approaches, role based and steps based 

# chat based model , specify role
# ~ sign to remove spaces 

# program = guidance(
#     """
#     {{#system}} You are a CS professor teaching {{os}} systems administration to your students
#     {{/system}}

#     {{#user~}}
#     What are some of the most common commands in the {{os}} operating system? Provide a one-liner description.
#     List the commands and their description one per line.  Number them starting from 1.
#     {{~/user}}

#     {{#assistant~}}
#     {{gen 'commands' max_tokens=100}}
#     {{~/assistant}}

#     {{#user~}}
#     Which among these commands are beginngers most likely to get wrong? Explain why the command might be confusing?
#     {{~/user}}

#     {{#assistant~}}
#     {{gen 'confusing_commands' max_tokens=60}}
#     {{~/assistant}}
#     """
# )

# result = program(os="Linux", echo=True)
print(result)

