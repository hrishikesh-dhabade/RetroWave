import pygame
import time
import math
import os
from buttons import ButtonHandler
from settings import Settings

WIDTH, HEIGHT = 128, 160
FPS = 30

BLACK      = (0,   0,   0  )
WHITE      = (255, 255, 255)
CYAN       = (0,   229, 255)
PINK       = (255, 63,  108)
YELLOW     = (255, 225, 77 )
DARK_GREY  = (20,  20,  35 )
MID_GREY   = (50,  50,  80 )
DIM        = (80,  80,  120)

def draw_disc(surface, cx, cy, radius, angle, playing):
    pygame.draw.circle(surface, MID_GREY, (cx, cy), radius)
    for r in range(radius-2, radius-10, -3):
        pygame.draw.circle(surface, DARK_GREY, (cx, cy), r, 1)
    if playing:
        colors = [PINK, YELLOW, CYAN]
        for i, color in enumerate(colors):
            start = math.radians(angle + i * 120)
            end   = math.radians(angle + i * 120 + 80)
            points = [(cx, cy)]
            steps = 20
            for s in range(steps + 1):
                a = start + (end - start) * s / steps
                x = cx + int((radius - 2) * math.cos(a))
                y = cy + int((radius - 2) * math.sin(a))
                points.append((x, y))
            if len(points) > 2:
                pygame.draw.polygon(surface, color, points)
    pygame.draw.circle(surface, BLACK, (cx, cy), 8)
    pygame.draw.circle(surface, DIM,   (cx, cy), 8, 1)

def draw_text(surface, text, x, y, font, color, center=False):
    rendered = font.render(text, True, color)
    if center:
        x = x - rendered.get_width() // 2
    surface.blit(rendered, (x, y))

def fmt_time(seconds):
    m = seconds // 60
    s = seconds % 60
    return f"{m}:{s:02d}"

def run_display(player):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RetroWave Player")
    clock = pygame.time.Clock()

    font_small  = pygame.font.SysFont("monospace", 7)
    font_medium = pygame.font.SysFont("monospace", 9)
    font_title  = pygame.font.SysFont("monospace", 9, bold=True)

    # Session settings (shuffle / repeat / EQ)
    settings = Settings()

    # Wire up button callbacks — swap ButtonHandler internals for GPIO later
    buttons = ButtonHandler()
    buttons.on_play_pause(player.toggle)
    buttons.on_next(player.next)
    buttons.on_prev(player.prev)

    angle = 0.0
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    settings.toggle_shuffle()
                elif event.key == pygame.K_r:
                    settings.cycle_repeat()
                elif event.key == pygame.K_e:
                    settings.cycle_eq()
        buttons.check(events)

        if player.playing:
            angle = (angle + 2.5) % 360

        screen.fill(BLACK)

        song = player.current()
        if song:
            title    = song['title'][:16]
            artist   = song['artist'][:16]
            duration = song['duration']
            elapsed  = min(player.elapsed, duration)
            progress = elapsed / duration if duration > 0 else 0

            # --- Status bar: time | battery | shuffle | repeat ---
            shuf_icon   = "S" if settings.get_shuffle() else "."
            repeat_lbl  = settings.get_repeat().upper()       # OFF / ONE / ALL
            draw_text(screen, "10:42",      2,   2, font_small, DIM)
            draw_text(screen, "78%",        78,  2, font_small, DIM)
            draw_text(screen, shuf_icon,    98,  2, font_small, CYAN  if settings.get_shuffle() else DIM)
            draw_text(screen, repeat_lbl,  107,  2, font_small, YELLOW if settings.get_repeat() != "off" else DIM)

            draw_disc(screen, WIDTH//2, 58, 38, angle, player.playing)

            draw_text(screen, title,  WIDTH//2, 102, font_title,  WHITE,  center=True)
            draw_text(screen, artist, WIDTH//2, 113, font_medium, DIM,    center=True)

            bar_x, bar_y = 8, 126
            bar_w = WIDTH - 16
            pygame.draw.rect(screen, MID_GREY, (bar_x, bar_y, bar_w, 3))
            pygame.draw.rect(screen, CYAN,     (bar_x, bar_y, int(bar_w * progress), 3))

            draw_text(screen, fmt_time(elapsed),  bar_x,          132, font_small, DIM)
            draw_text(screen, fmt_time(duration), bar_x + bar_w - 20, 132, font_small, DIM)

            # EQ preset label above the bars
            eq_label = settings.get_eq()
            draw_text(screen, eq_label, WIDTH // 2, 138, font_small, DIM, center=True)

            eq_heights = [6, 10, 5, 12, 8, 7, 11]
            eq_x = (WIDTH - len(eq_heights) * 5) // 2
            for i, h in enumerate(eq_heights):
                if player.playing:
                    h = max(3, int(h * (0.5 + 0.5 * math.sin(angle * 0.1 + i))))
                pygame.draw.rect(screen, PINK,
                    (eq_x + i * 5, 155 - h, 3, h))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    from library import scan_music
    from player import Player

    songs = scan_music()
    p = Player()
    p.load(songs)
    p.play()

    run_display(p)