"""
settings.py � In-memory session settings for the RetroWave Player.

Manages:
    shuffle     bool        False | True
    repeat      str         "off" -> "one" -> "all" -> "off" ...
    eq_preset   str         "FLAT" -> "BASS" -> "TREBLE" -> "VOCAL" -> "KARAOKE" -> "FLAT" ...

No file I/O � state lives only for the lifetime of the process.
"""


class Settings:
    _REPEAT_STATES = ("off", "one", "all")
    _EQ_PRESETS    = ("FLAT", "BASS", "TREBLE", "VOCAL", "KARAOKE")

    def __init__(self):
        self._shuffle    = False
        self._repeat_idx = 0          # index into _REPEAT_STATES
        self._eq_idx     = 0          # index into _EQ_PRESETS

    # ------------------------------------------------------------------ #
    # Shuffle                                                               #
    # ------------------------------------------------------------------ #

    def toggle_shuffle(self):
        """Flip shuffle on/off and return the new value."""
        self._shuffle = not self._shuffle
        return self._shuffle

    def get_shuffle(self):
        """Return current shuffle state."""
        return self._shuffle

    # ------------------------------------------------------------------ #
    # Repeat mode                                                           #
    # ------------------------------------------------------------------ #

    def cycle_repeat(self):
        """Advance to the next repeat mode and return it ('off'/'one'/'all')."""
        self._repeat_idx = (self._repeat_idx + 1) % len(self._REPEAT_STATES)
        return self.get_repeat()

    def get_repeat(self):
        """Return current repeat mode string."""
        return self._REPEAT_STATES[self._repeat_idx]

    # ------------------------------------------------------------------ #
    # EQ preset                                                             #
    # ------------------------------------------------------------------ #

    def cycle_eq(self):
        """Advance to the next EQ preset and return its name."""
        self._eq_idx = (self._eq_idx + 1) % len(self._EQ_PRESETS)
        return self.get_eq()

    def get_eq(self):
        """Return current EQ preset name."""
        return self._EQ_PRESETS[self._eq_idx]
