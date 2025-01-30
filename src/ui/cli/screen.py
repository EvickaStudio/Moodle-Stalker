import os
import time

from src.core.version import __version__

# ANSI escape codes for colors and effects
COLOR_BORDER = "\033[38;5;240m"
COLOR_MOODLE = "\033[38;5;9m"
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_FADE = "\033[2m"

# Define the logo lines
logo_lines = [
    f"{COLOR_BORDER}╭─┐ {COLOR_RESET}{COLOR_BOLD}Moodle Mate {COLOR_MOODLE}{__version__:>8}{COLOR_RESET} {COLOR_BORDER}┌{'─'*47}╮{COLOR_RESET}",  # noqa: E501
    f"{COLOR_BORDER}│       {COLOR_MOODLE}__  ___             ____    {COLOR_RESET}__  ___     __        ,-------,      {COLOR_BORDER}│{COLOR_RESET}",  # noqa: E501
    f"{COLOR_BORDER}│      {COLOR_MOODLE}/  |/  /__  ___  ___/ / /__ {COLOR_RESET}/  |/  /__ _/ /____   /       / |     {COLOR_BORDER}│{COLOR_RESET}",  # noqa: E501
    f"{COLOR_BORDER}│     {COLOR_MOODLE}/ /|_/ / _ \\/ _ \\/ _  / / -_){COLOR_RESET} /|_/ / _ `/ __/ -_) /______ /  /     {COLOR_BORDER}│{COLOR_RESET}",  # noqa: E501
    f"{COLOR_BORDER}│    {COLOR_MOODLE}/_/  /_/\\___/\\___/\\_,_/_/\\__/{COLOR_RESET}_/  /_/\\_,_/\\__/\\__/ |___/___/  /      {COLOR_BORDER}│{COLOR_RESET}",  # noqa: E501
    f"{COLOR_BORDER}│     {COLOR_RESET}-—--–=¤=—--–-- - -  {COLOR_BOLD}EvickaStudio{COLOR_RESET}  - - --–--—=¤=--|__..___|.'- -    {COLOR_BORDER}│{COLOR_RESET}",  # noqa: E501
    f"{COLOR_BORDER}│                                                        {COLOR_RESET}//              {COLOR_BORDER}│{COLOR_RESET}",  # noqa: E501
    f"{COLOR_BORDER}╰{'─'*72}╯{COLOR_RESET}",
]


def clear_screen() -> None:
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def animate_logo(logo: list) -> None:
    """Animates the logo by printing it line by line with a delay."""
    for line in logo:
        print(line)
        time.sleep(0.05)  # Adjust the sleep time for animation speed


def loading_animation(duration: float) -> None:
    """Displays a simple loading animation."""
    animation = "|/-\\"
    idx = 0
    end_time = time.time() + duration
    while time.time() < end_time:
        print(
            f"\r{COLOR_BOLD}Loading {animation[idx % len(animation)]}{COLOR_RESET}",
            end="",
        )
        idx += 1
        time.sleep(0.1)
    print("\r" + " " * 20 + "\r", end="")  # Clear the loading line


if __name__ == "__main__":
    clear_screen()
    loading_animation(1)  # Display loading animation for 2 seconds
    animate_logo(logo_lines)
    # Keep the console open if script is run directly
    input(f"\n{COLOR_FADE}Press Enter to continue...{COLOR_RESET}")
