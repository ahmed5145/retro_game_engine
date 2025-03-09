"""Basic game loop example."""
import sys
from pathlib import Path

import pygame

# Add the root directory to Python path
root_dir = str(Path(__file__).parent.parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.core.game_loop import GameLoop, GameLoopConfig


class GameLoopExample:
    """Example game using the game loop."""

    def __init__(self) -> None:
        """Initialize the game."""
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Game Loop Example")
        self.font = pygame.font.Font(None, 36)

        # Create game loop config
        self.config = GameLoopConfig(
            fps=60,
            fixed_time_step=1.0 / 50.0,  # 50Hz physics updates
            max_frame_time=0.25,
            fps_sample_size=60,
        )

        # Create game loop
        self.game_loop = GameLoop(
            update_func=self.update, render_func=self.render, config=self.config
        )

    def update(self, dt: float) -> None:
        """Update game state.

        Args:
            dt: Time delta in seconds
        """
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_loop.stop()

    def render(self) -> None:
        """Render game state."""
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Draw FPS counter
        fps = int(self.game_loop.average_fps)
        text = self.font.render(f"FPS: {fps}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        # Update display
        pygame.display.flip()

    def run(self) -> None:
        """Run the game loop."""
        self.game_loop.run()
        pygame.quit()


def main() -> None:
    """Run the game loop example."""
    game = GameLoopExample()
    game.run()


if __name__ == "__main__":
    main()
