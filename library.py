import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

def scan_music(folder="Music"):
    songs = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".mp3"):
                path = os.path.join(root, file)
                try:
                    tags = ID3(path)
                    title  = str(tags.get("TIT2", os.path.splitext(file)[0]))
                    artist = str(tags.get("TPE1", "Unknown Artist"))
                    audio  = MP3(path)
                    duration = int(audio.info.length)
                except Exception:
                    title    = os.path.splitext(file)[0]
                    artist   = "Unknown Artist"
                    duration = 0
                songs.append({
                    "path":     path,
                    "title":    title,
                    "artist":   artist,
                    "duration": duration
                })
    return songs

if __name__ == "__main__":
    results = scan_music()
    if results:
        for s in results:
            print(f"{s['title']} — {s['artist']} ({s['duration']}s)")
    else:
        print("No MP3 files found in Music folder.")