## Setup local speech to text using whisper.cpp

## Quick Start

```bash
# make a new directory, and go inside
mkdir local-whispercpp
cd local-whispercpp

# clone whisper.cpp, go inside, compile(make), check executable "main"
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
make 
ls -l main

Output:
./main -h

usage: ./main [options] file0.wav file1.wav ...

# download speech model 
bash ./models/download-ggml-model.sh base.en
ls -ltr ./models

# test using provided JFK sample speech
./main -m models/ggml-base.en.bin -f samples/jfk.wav

output:
main: processing 'samples/jfk.wav' (176000 samples, 11.0 sec), 4 threads, 1 processors, lang = en, task = transcribe, timestamps = 1 ...
...
[00:00:00.000 --> 00:00:11.000]   And so my fellow Americans, ask not what your country can do for you, ask what you can do for your country.

# On MacOs, create a wav file, test it, .wav must "read_wav file must be 16 kHz"
say -o test.aiff "AI will probably most likely lead to the end of the world, but in the meantime, there'll be great companies."
afplay test.aiff
ffmpeg -i test.aiff -acodec pcm_s16le -ar 16000 test.wav
./main -m models/ggml-base.en.bin -f ./test.wav

Output:  # "I", should be "AI", the first word needs to update
[00:00:00.000 --> 00:00:05.480]   I will probably most likely lead to the end of the world, but in the meantime, there will
[00:00:05.480 --> 00:00:06.720]   be great companies.

```

## To convert *.mp3 to *.wav file, you can also run below python program 

Convert single mp3.file  
python convert_mp3_file_folder_to_wav.py a.mp3 

Convert multiple mp3.file  
python convert_mp3_file_folder_to_wav.py a.mp3 b.mp3

Convert all *.mp3 files in a current folder  
python convert_mp3_file_folder_to_wav.py ./

## For stream

```bash 
make stream 

# if error ./examples/common-sdl.h:3:10: fatal error: 'SDL2/SDL.h' file not found, do this
brew install sdl2

# if error Error: Could not symlink include/SDL2/SDL_ttf.h, do this
brew link --overwrite sdl2

./stream -m ./models/ggml-base.en.bin -t 8 --step 500 --length 5000

Output:
$ ./stream -m ./models/ggml-base.en.bin -t 8 --step 500 --length 5000
init: found 2 capture devices:
init:    - Capture device #0: 'External Microphone'
init:    - Capture device #1: 'MacBook Pro Microphone'
init: attempt to open default capture device ...
init: obtained spec for input device (SDL Id = 2):
...
whisper_init_from_file_no_state: loading model from './models/ggml-base.en.bin'
..

main: processing 8000 samples (step = 0.5 sec / len = 5.0 sec / keep = 0.2 sec), 8 threads, lang = en, task = transcribe, timestamps = 0 ...
main: n_new_line = 9, no_context = 1

 [BLANK_AUDIO]
 A long time. I don't know. 
 [BLANK_AUDIO]
 [Music]
 (upbeat music)
```