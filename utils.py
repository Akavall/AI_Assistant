
import os

def get_artist_songs(directory_path):
    songs = []
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if os.path.splitext(file_name)[1] in (".mp3", ".wav"):
                full_path = root + "/" + file_name
                songs.append(full_path)

    return songs
