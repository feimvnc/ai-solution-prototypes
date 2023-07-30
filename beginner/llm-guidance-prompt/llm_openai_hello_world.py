from dotenv import load_dotenv 
import guidance 

load_dotenv()

# tell guidance what llm to use
# guidance.llm = guidance.llms.OpenAI("text-davince-003")
guidance.llm = guidance.llms.Transformers(
    "stabilityai/stablelm-base-alpha-3b", device="cpu"
    # "stabilityai/stablelm-base-alpha-7b"    # the other model 
)

program = guidance(
    """
    What are the top ten most common commands used in the {{os}} operating system
    """

)

result = program(os="Linux")    # use templating handle bar {{ }}
print(result)