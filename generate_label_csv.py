import eyed3
import glob
import os
import reference_pitch
import sys
import shutil

from tqdm import tqdm

# Parameters
label_filename = "label.csv"
cover_dir = "./Cover"
folder_list = glob.glob("./Music/*")
folder_list.sort()

# Create Cover Directory
if os.path.isdir(cover_dir):
    shutil.rmtree(cover_dir)  # This script will ALWAYS recreate the directory.
os.mkdir(cover_dir)

# Bulid Music List
music_list = []
for i in folder_list:
    tmp = glob.glob(f"{i}/*")
    tmp.sort()
    music_list.append(tmp)

cnt = 0
with open(label_filename, "w+") as f:
    f.write('ID,Title,Artist,Album,File_Path,Cover_Path,First_Comment,Lowest_Pitch,First_Quartile_Pitch,Medium_Pitch,Third_Quartile_Pitch,Highest_Pitch\n')
    for folder in tqdm(music_list):
        write_cover = True
        for music in folder:
            if os.path.isdir(music):
                continue
            basename_full = os.path.basename(music)
            basename = os.path.splitext(basename_full)[0]
            ext = os.path.splitext(music)[1]
            if ext == ".jpg":
                continue

            vocal_path = os.path.join(os.path.splitext(music)[0], "vocals.wav")
            # Reference Pitch List
            ref = reference_pitch.ref_pitch(vocal_path)

            # Get Metadata
            metadata = eyed3.load(music)
            title = metadata.tag.title
            artist = metadata.tag.artist
            album = metadata.tag.album
            comment = metadata.tag.comments
            cover_path = f"{cover_dir}/{album}.jpg"
            if write_cover:
                if metadata.tag.images:
                    cover_bin_data = metadata.tag.images[0].image_data
                    with open(cover_path, "wb") as fcover:
                        fcover.write(cover_bin_data)
                    write_cover = False
            if title is None or artist is None or album is None or comment is None:
                print(f"\nError, the file {music} has no information.\n", file=sys.stderr)
                comment = None
            else:
                comment = metadata.tag.comments[0].text
            f.write(f'{cnt},"{title}","{artist}","{album}","{music}","{cover_path}","{comment}",{ref[0]},{ref[1]},{ref[2]},{ref[3]},{ref[4]}\n')
            f.flush()
            cnt += 1
