import os
import sys

from tqdm import tqdm

path = "./Music"
allFileList = os.listdir(path)
allFileList.sort()
for file in tqdm(allFileList):
    album_path = os.path.join(path, file)
    music_list = os.listdir(album_path)
    music_list.sort()
    for music in music_list:
        if os.path.splitext(music)[1] == ".mp3":
            music_path = os.path.join(album_path, music)
            music_path = "\"" + music_path + "\""
            output_path = os.path.join(os.getcwd(), album_path)
            output_path = "\"" + output_path + "\""
            print(music_path, file=sys.stderr)
            os.system(f"python -m spleeter separate -p spleeter:2stems -o {output_path} {music_path}")
