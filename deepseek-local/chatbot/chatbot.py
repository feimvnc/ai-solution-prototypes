import requests, json 

if __name__ == "__main__":
    conversation = []
    while (prompt := input(">: ")) != "exit":
        conversation.append({"role": "user", "content": prompt})
        
        # data to api
        data = {
            "model": "deepseek-r1:1.5b",
            "messages": conversation, 
            "stream": False
        }

        # define local api endpoint
        url = "http://localhost:11434/api/chat"
        response = requests.post(url, json=data)
        response_json = json.loads(response.text)
        print(response_json)
        answer = response_json["message"]["content"]
        conversation.append({"role": "assistant", "content": answer})
        print(answer)