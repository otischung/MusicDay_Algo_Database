import eyed3
import glob
import os

from tqdm import tqdm

label_filename = "label.csv"
folder_list = glob.glob("./Music/*")
folder_list.sort()
music_list = []
for i in folder_list:
    tmp = glob.glob(f"{i}/*")
    tmp.sort()
    music_list.append(tmp)

with open(label_filename, "w+") as f:
    f.write('Title,Artist,Album,File Path,Cover Path,Lowest Pitch,First Quartile Pitch,Medium Pitch,Third Quartile Pitch,Highest Pitch\n')
    for folder in tqdm(music_list):
        write_cover = True
        for music in folder:
            if os.path.splitext(music)[1] == ".jpg":
                continue
            metadata = eyed3.load(music)
            cover_path = f"{os.path.dirname(music)}/cover.jpg"
            title = metadata.tag.title
            artist = metadata.tag.artist
            album = metadata.tag.album
            if write_cover:
                if metadata.tag.images:
                    cover_bin_data = metadata.tag.images[0].image_data
                    with open(cover_path, "wb") as fcover:
                        fcover.write(cover_bin_data)
                    write_cover = False
            f.write(f'"{title}","{artist}","{album}","{music}","{cover_path}"\n')
