from dotenv import load_dotenv 
import guidance 

load_dotenv()

# tell guidance what llm to use
# guidance.llm = guidance.llms.OpenAI("text-davinci-003")
guidance.llm = guidance.llms.Transformers(
    "stabilityai/stablelm-base-alpha-3b", device="cpu"
    # "stabilityai/stablelm-base-alpha-7b"    # the other model 
)

program = guidance(
    """
    What are the top ten most common commands used in the {{os}} operating system

    Here is a common command: '{{gen 'commands' stop='"' n=5 temperature=0.7}}
    """
)

result = program(os="Linux")    # use templating handle bar {{ }}
print(result["commands"])    # "commands" is key


'''
program = guidance(
    """
    What are the top ten most common commands used in the {{os}} operating system

    Here are the top five most common commands:
    '{{gen 'commands' stop='\\6.' n=1 temperature=0.7}}
    """
) 
'''