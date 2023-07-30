# just openai api example 

import webbrowser
import openai 

# Create our completion 
completion = openai.Completion.create(model="ada", prmpt="Once upon a time")
print(completion.choices[0].text)

# Image generation with dalll-e 2
image_gen = openai.Image.create(
    prompt="a dog on a boat, cartoon",
    n=2, size="512x512"
)

for img in image_gen.data:
    webbrowser.open_new_tab(img.url)

# Audio 
audio = open("audio/myaudio.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio)
print(transcript)