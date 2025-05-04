from nova_act import NovaAct

with NovaAct(starting_page="https://www.amazon.com") as nova:
	nova.act("search for a coffee maker")
	


"""

First workflow output.

# export api key, replace with your own
(llm-312) user-2:nova-act user$ export NOVA_ACT_API_KEY=12345-abcd-1234-abcd-1234567890

# run workflow, 
# a browser will open automatically, create a session
# search coffee maker on www.amazon.com
(llm-312) user-2:nova-act user$ python workflow_1.py 

start session 11112222-68ae-4e88-bd3b-1234567890 on https://www.amazon.com logs dir /var/folders/l1/xxxxxx/T/tmp123456ab_nova_act_logs/11112222-68ae-4e88-bd3b-1234567890

75e8> act("search for a coffee maker")
..........................
75e8> think("I am on the amazon homepage. My task is to search for a coffee maker. I see a search field, but it is empty. I need to type 'coffee maker' into the search field.");
>> agentType("coffee maker", "<box>10,396,48,1154</box>");
....................
75e8> think("The search field now contains 'coffee maker', meaning my last action was successful. The search has not been initiated. I see a search button to the right of the search field. I need to click the search button to initiate the search.");
>> agentClick("<box>10,1154,48,1196</box>");
...................
75e8> think("I am now on the search results page for coffee makers, meaning my last action was successful. I have searched for a coffee maker. The task is complete, and I was not asked to provide any information, so I will simply return.");
>> return;
.........
end session


"""