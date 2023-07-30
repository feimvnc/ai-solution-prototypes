import random 
from dotenv import load_dotenv 
import guidance 

load_dotenv()

# tell guidance what llm to use
# guidance.llm = guidance.llms.OpenAI("text-davinci-003")
guidance.llm = guidance.llms.Transformers(
    "stabilityai/stablelm-base-alpha-3b", device="cpu"
    # "stabilityai/stablelm-base-alpha-7b"    # the other model 
)

quizFlavor = [
    "Quiz of the day",
    "Test your knowledge",
    "Here is a quiz",
    "You think you know unix?"
]


# hidden=True  # hide from output 
# geneach    # list
# @index    # index 
# this    # the list block 
# {{@index+1}}.  # prepend index 
program = guidance(
    """
    What are the top ten most common commands used in the {{os}} operating system? Provide a one liner description.
    {{#block hidden=True}}
    A few example commands would be:
    [1]: pwd prints the current working directory
    [2]: mv used to move or rename files 
    {{gen 'examples' n=2 stop='"' max_tokens=20 temperature=0.8}}
    {{/block}}

    Here are the common commands:is a common command: 
    {{#geneach 'commands' num_iterations=10}}
    [{{@index}}]: "{{gen 'this' stop='"'}}", Description: "{{gen 'description' stop='"'}}"
    {{/geneach}}
    
     '{{gen 'commands' stop='"' n=5 temperature=0.7}}

    {{select 'flavor' options=quizFlavor}}  ]
    Explain the following commands for {{randomPts}} points:
    {{#each (pickthree commands)}}
    {{@index+1}}. "{{this}}"
    {{/each}}

    Use the commands listedd above as input, genereate a valid JSON object that maps each command to its description.
    "{
        "{{os}}": [
            {{#geneach 'obj' num_iterations=1}}{{#unless @first}},{{/unless}}
            {{/geneacch}}
        ]
    }"

    """
)

# guidance tooling
# use templating handle bar {{ }}
# pickthree, "x" values from "commands"
result = program(os="Linux",
                pickthree=lambda x: list(set(x))[:3],
                randomPts=random.randint(1,5),
                quizFlavor=quizFlavor
)    

print(result["commands"])    # "commands" is key
print(result["examples"])

'''
program = guidance(
    """
    What are the top ten most common commands used in the {{os}} operating system

    Here are the top five most common commands:
    '{{gen 'commands' stop='\\6.' n=1 temperature=0.7}}
    """
) 
'''