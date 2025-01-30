#!/usr/bin/env python3
import curses
import math
import random
import time

LOGO_LINES = [
    r"╭─┐ Moodle Mate ┌────────────────────────────────────────────────────────╮",
    r"│       __  ___             ____    __  ___     __        ,-------,      │",
    r"│      /  |/  /__  ___  ___/ / /__ /  |/  /__ _/ /____   /       / |     │",
    r"│     / /|_/ / _ \/ _ \/ _  / / -_) /|_/ / _ `/ __/ -_) /______ /  /     │",
    r"│    /_/  /_/\___/\___/\_,_/_/\__/_/  /_/\_,_/\__/\__/ |___/___/  /      │",
    r"│     -—--–=¤=—--–-- - -  EvickaStudio  - - --–--—=¤=--|__..___|.'- -    │",
    r"│                                                        //              │",
    r"╰────────────────────────────────────────────────────────────────────────╯",
]

# Base animation parameters
DELAY = 0.04  # Speed between frames
WAVE_SPEED_X = 2.0  # Horizontal wave speed
WAVE_SPEED_Y = 3.0  # Vertical wave speed
BASE_AMPLITUDE_X = 2.0
BASE_AMPLITUDE_Y = 1.0

# Prepare random offsets so each line has a slightly different amplitude
RANDOM_AMPLITUDES = [random.uniform(0.8, 1.2) for _ in LOGO_LINES]


def draw_logo(stdscr, start_row, start_col, frame, color_pairs):
    """
    Draws the logo with a "double wave" (vertical jiggle + horizontal sway).
    Each line also cycles colors for extra flair.
    """
    height, width = stdscr.getmaxyx()

    for i, line in enumerate(LOGO_LINES):
        # For each line, we combine:
        #   wave_offset_x = horizontal displacement
        #   wave_offset_y = vertical displacement
        # to create a "double wave".
        amp_factor = RANDOM_AMPLITUDES[i]

        wave_offset_x = int(
            BASE_AMPLITUDE_X * amp_factor * math.sin((frame / WAVE_SPEED_X) + i)
        )
        wave_offset_y = int(
            BASE_AMPLITUDE_Y * amp_factor * math.sin((frame / WAVE_SPEED_Y) + i + 1)
        )

        # Determine row and column with the wave offsets
        row = start_row + i + wave_offset_y
        col = start_col + wave_offset_x

        # Ensure the text won't go off-screen horizontally
        # Adjust so partial line is visible if it extends beyond width
        if 0 <= row < height:
            cropped_line = line
            if col < 0:
                # Trim off the left part if wave pushes into negative columns
                cropped_line = cropped_line[-col:]
                col = 0
            elif col + len(cropped_line) > width:
                # Trim on the right if it extends beyond screen width
                cropped_line = cropped_line[: width - col]

            # Cycle the color pair based on (i + frame)
            color_index = (i + frame) % len(color_pairs)
            color_pair = color_pairs[color_index]

            # Draw line
            if col < width and cropped_line:
                stdscr.addstr(row, col, cropped_line, curses.color_pair(color_pair))


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.timeout(0)  # Non-blocking getch()

    curses.start_color()
    curses.use_default_colors()

    # We'll create a cycle of color pairs to rotate through
    # Note: Depending on your terminal, you can define more than 8 if it supports 256 colors.
    available_colors = [
        curses.COLOR_RED,
        curses.COLOR_GREEN,
        curses.COLOR_YELLOW,
        curses.COLOR_BLUE,
        curses.COLOR_MAGENTA,
        curses.COLOR_CYAN,
        curses.COLOR_WHITE,
    ]

    # Initialize color pairs and store their IDs in a list
    color_pairs = []
    for idx, fg_col in enumerate(available_colors, start=1):
        curses.init_pair(idx, fg_col, -1)  # -1 => keep default bg
        color_pairs.append(idx)

    frame = 0
    while True:
        stdscr.erase()

        # Center the logo
        start_row = max(0, (curses.LINES - len(LOGO_LINES)) // 2)
        longest_line_length = max(len(line) for line in LOGO_LINES)
        start_col = max(0, (curses.COLS - longest_line_length) // 2)

        draw_logo(stdscr, start_row, start_col, frame, color_pairs)
        stdscr.refresh()

        # Exit if 'q' is pressed
        ch = stdscr.getch()
        if ch == ord("q"):
            break

        frame += 1
        time.sleep(DELAY)


if __name__ == "__main__":
    curses.wrapper(main)
