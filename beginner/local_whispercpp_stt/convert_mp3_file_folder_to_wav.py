# Use python to convert mp3 to wav file in 16khz format
# enter multiple .mp3 file in command line 
# 
# convert individual file(s)
# python convert_mp3_to_wav.py  a.mp3 b.mp3
#
# convert all mp3 files in current  folder
# python convert_mp3_to_wav.py  ./
#
#
from pydub import AudioSegment
from tqdm import tqdm 
from typing import List, Any 
import sys, os 

def main(file_input_list: List) -> None: 
    
    mp3_files = []
    for f in file_input_list:
        if os.path.isdir(f):
            print(f)
            mp3_files.extend([x for x in os.listdir() if x.endswith(".mp3")])
        elif os.path.isfile(f):
            mp3_files.extend(f)

    print(mp3_files)
    for src in tqdm (mp3_files):
        des = src.replace('.mp3','.wav')
        try:
            sound = AudioSegment.from_mp3(src)
            sound.set_channels(1)
            sound = sound.set_frame_rate(16000)                
            sound = sound.set_channels(1)    
            sound.export(des, format="wav")

        except:
            print(src)
            continue

if __name__ == "__main__":
    main(sys.argv[1:])