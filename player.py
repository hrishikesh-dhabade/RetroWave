import pygame

# Initialise the mixer once at import time so it's ready before any playback.
# frequency=44100, 16-bit signed, stereo, 2048-sample buffer.
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)


class Player:
    def __init__(self):
        self.songs         = []
        self.current_index = 0
        self.playing       = False
        self.elapsed       = 0
        self.shuffle       = False
        self.repeat        = False

    def load(self, songs):
        self.songs         = songs
        self.current_index = 0

    def current(self):
        if self.songs:
            return self.songs[self.current_index]
        return None

    def play(self):
        """Load the current song into the mixer and start playback from the top."""
        song = self.current()
        if song:
            pygame.mixer.music.stop()               # ensure previous audio is fully stopped
            pygame.mixer.music.load(song['path'])
            pygame.mixer.music.play()
            self.playing = True
            self.elapsed = 0

    def stop(self):
        """Fully stop playback (used when changing tracks)."""
        pygame.mixer.music.stop()
        self.playing = False

    def toggle(self):
        """
        Pause / unpause without restarting the song.
        Uses pygame.mixer.music.pause() / unpause() so playback
        resumes exactly where it left off.
        """
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False
        else:
            pygame.mixer.music.unpause()
            self.playing = True

    def next(self):
        """Stop current audio completely, advance index, play new song."""
        if self.songs:
            pygame.mixer.music.stop()               # hard stop — no overlap
            self.current_index = (self.current_index + 1) % len(self.songs)
            self.play()

    def prev(self):
        """Stop current audio completely, step back index, play new song."""
        if self.songs:
            pygame.mixer.music.stop()               # hard stop — no overlap
            self.current_index = (self.current_index - 1) % len(self.songs)
            self.play()


if __name__ == "__main__":
    import time
    from library import scan_music

    songs = scan_music()
    if not songs:
        print("No songs found.")
    else:
        p = Player()
        p.load(songs)
        p.play()
        print(f"Playing: {p.current()['title']}")
        time.sleep(5)
        p.toggle()
        print("Paused.")
        time.sleep(2)
        p.toggle()
        print("Resumed.")
        time.sleep(5)
        p.stop()
        print("Stopped.")