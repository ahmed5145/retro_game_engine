import sys
from typing import List, Tuple

import pygame

from src.core import Window, WindowConfig


def main() -> None:
    # Initialize pygame
    pygame.init()

    # Create window configuration
    config = WindowConfig(
        title="Retro Game Engine - Basic Window Example",
        width=320,
        height=240,
        scale=2,
        vsync=True,
    )

    # Create window
    window = Window(config)

    # Main game loop
    running = True
    colors: List[Tuple[int, int, int]] = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
    ]  # Red, Green, Blue
    current_color = 0

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Cycle through colors
                    current_color = (current_color + 1) % len(colors)
                elif event.key == pygame.K_f:
                    window.toggle_fullscreen()

        # Clear window with current color
        window.clear(colors[current_color])

        # Present the frame
        window.present()

    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
