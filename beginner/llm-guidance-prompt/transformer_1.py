# local run guidance without api 
import guidance

# open source model to run local llm instance 
guidance.llm = guidance.llms.Transformers(
    "stabilityai/stablelm-base-alpha-3b", device="cpu"
    # "stabilityai/stablelm-base-alpha-7b"    # the other model 
)

program = guidance('''The link is <a href="http:{{gen max_tokens=10 token_healing=False}}''')
result = program(echo=True)
print(result)


''' Output: it takes few seconds to load model at runtime
$ python transformer_1.py 
Loading checkpoint shards: 100%|█████████████████████████████████████████████████████████████| 2/2 [00:36<00:00, 18.12s/it]
The link is <a href="http: //www.google.com/search?q
'''

# change token size and healing to True
program = guidance('''The link is <a href="http:{{gen max_tokens=100 token_healing=True}}''')
result = program(echo=True)
print(result)

"""Output:  Note the url is not available.
$ python transformer_1.py 
Loading checkpoint shards: 100%|█████████████████████████████████████████████████████████████| 2/2 [00:35<00:00, 17.70s/it]
The link is <a href="http://www.youtube.com/v/s_N9zUuJgQ?version=3&amp;amp;hl=en_US" target="_blank"&gt;http://www.youtube.com/v/s_N9zUuJgQ?version=3&amp;amp;hl=en_US &amp;amp;context=5</a&gt; brought to you by <a href="http://www.youtube

"""