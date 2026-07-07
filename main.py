import sys

from library import scan_music
from player import Player
from display import run_display


def main():
    songs = scan_music("Music")

    if not songs:
        print("No MP3 files found in the Music folder. "
              "Add some .mp3 files and try again.")
        sys.exit(0)

    print(f"Found {len(songs)} song(s).")

    player = Player()
    player.load(songs)
    # Start paused — user presses Space in the UI to begin playback

    run_display(player)


if __name__ == "__main__":
    main()
