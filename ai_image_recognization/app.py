import ollama

res = ollama.chat(
    model="llava:7b",
    messages=[
        {
            "role": "user",
            "content": "Can you compose a brand new song using the provided image as context?",
            # "content": "Describe this image",  # i  one sentence",
            # "content": "Extract exact words and sentences from the image. Explain the content on the image.",
            "images": ["./image1.png"],
        }
    ],
)

print(res["message"]["content"])
