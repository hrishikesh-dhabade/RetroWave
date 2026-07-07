"""
buttons.py — Virtual button abstraction layer for the RetroWave Player.

Keyboard bindings (current, for Windows/desktop testing):
    SPACE       → play / pause
    RIGHT arrow → next track
    LEFT arrow  → previous track
    UP arrow    → up (volume / menu)
    DOWN arrow  → down (volume / menu)

Raspberry Pi GPIO pin mapping (future — swap check() body for RPi.GPIO reads):
    GPIO17 → Up
    GPIO27 → Down
    GPIO22 → Left  (prev)
    GPIO23 → Right (next)
    GPIO24 → Center (play/pause)
"""

import pygame


class ButtonHandler:
    """
    Translates low-level input events into named button callbacks.

    Register a handler with e.g. handler.on_play_pause(player.toggle),
    then call handler.check(events) once per frame inside the display loop.
    To port to GPIO later, replace the body of check() — the rest of the
    codebase stays untouched.
    """

    def __init__(self):
        self._play_pause_cb = None
        self._next_cb       = None
        self._prev_cb       = None
        self._up_cb         = None
        self._down_cb       = None

    # ------------------------------------------------------------------ #
    # Callback registration                                                 #
    # ------------------------------------------------------------------ #

    def on_play_pause(self, callback):
        """Register a callable invoked when the play/pause button fires."""
        self._play_pause_cb = callback

    def on_next(self, callback):
        """Register a callable invoked when the next button fires."""
        self._next_cb = callback

    def on_prev(self, callback):
        """Register a callable invoked when the prev button fires."""
        self._prev_cb = callback

    def on_up(self, callback):
        """Register a callable invoked when the up button fires."""
        self._up_cb = callback

    def on_down(self, callback):
        """Register a callable invoked when the down button fires."""
        self._down_cb = callback

    # ------------------------------------------------------------------ #
    # Input polling — keyboard implementation (swap for GPIO on Pi)        #
    # ------------------------------------------------------------------ #

    def check(self, events):
        """
        Process a list of pygame events and fire any matching callbacks.

        Parameters
        ----------
        events : list[pygame.event.Event]
            The event list returned by pygame.event.get() each frame.
            Passing them in (rather than calling get() here) keeps the
            display loop's QUIT handling intact and avoids consuming events
            twice.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._fire(self._play_pause_cb)
                elif event.key == pygame.K_RIGHT:
                    self._fire(self._next_cb)
                elif event.key == pygame.K_LEFT:
                    self._fire(self._prev_cb)
                elif event.key == pygame.K_UP:
                    self._fire(self._up_cb)
                elif event.key == pygame.K_DOWN:
                    self._fire(self._down_cb)

    # ------------------------------------------------------------------ #
    # Internal helpers                                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _fire(callback):
        """Call callback if it has been registered (not None)."""
        if callback is not None:
            callback()
