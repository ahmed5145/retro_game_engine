import sys
from typing import List, Tuple

import pygame

from src.core import Window, WindowConfig
from src.core.game_loop import GameLoop, GameLoopConfig


class Game:
    def __init__(self) -> None:
        # Initialize window
        window_config = WindowConfig(
            title="Game Loop Example - Bouncing Square",
            width=640,
            height=480,
            scale=1,
            vsync=True,
        )
        self.window = Window(window_config)

        # Initialize game loop
        loop_config = GameLoopConfig(
            target_fps=60, fixed_update_fps=50  # 50Hz for physics updates
        )
        self.game_loop = GameLoop(loop_config)

        # Set up game loop callbacks
        self.game_loop.update = self.update
        self.game_loop.fixed_update = self.fixed_update
        self.game_loop.render = self.render

        # Game state
        self.square_pos: List[float] = [320.0, 240.0]  # Center of screen
        self.square_vel: List[float] = [200.0, 150.0]  # Pixels per second
        self.square_size = 50

        # Colors
        self.square_color = (255, 0, 0)  # Red
        self.background_color = (0, 0, 0)  # Black
        self.text_color = (255, 255, 255)  # White

        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)  # Default font, size 24

        # Show metrics flag
        self.show_metrics = True

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_loop.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_loop.stop()
                elif event.key == pygame.K_SPACE:
                    # Reverse velocity on space
                    self.square_vel[0] *= -1
                    self.square_vel[1] *= -1
                elif event.key == pygame.K_m:
                    # Toggle metrics display
                    self.show_metrics = not self.show_metrics

    def update(self) -> None:
        """Variable timestep update - handle input."""
        self.handle_events()

    def fixed_update(self) -> None:
        """Fixed timestep update - update physics."""
        # Update position
        dt = self.game_loop.fixed_delta_time
        self.square_pos[0] += self.square_vel[0] * dt
        self.square_pos[1] += self.square_vel[1] * dt

        # Bounce off walls
        if self.square_pos[0] < 0:
            self.square_pos[0] = 0
            self.square_vel[0] *= -1
        elif self.square_pos[0] > self.window.width - self.square_size:
            self.square_pos[0] = self.window.width - self.square_size
            self.square_vel[0] *= -1

        if self.square_pos[1] < 0:
            self.square_pos[1] = 0
            self.square_vel[1] *= -1
        elif self.square_pos[1] > self.window.height - self.square_size:
            self.square_pos[1] = self.window.height - self.square_size
            self.square_vel[1] *= -1

    def render_metrics(self) -> None:
        """Render performance metrics."""
        if not self.show_metrics:
            return

        metrics = self.game_loop.metrics
        y = 10
        line_height = 20

        def render_line(text: str, y: int) -> None:
            surface = self.font.render(text, True, self.text_color)
            self.window.surface.blit(surface, (10, y))

        render_line(f"FPS: {metrics.fps:.1f}", y)
        y += line_height
        render_line(f"Frame Time: {metrics.frame_time*1000:.1f}ms", y)
        y += line_height
        render_line(f"Min Frame Time: {metrics.min_frame_time*1000:.1f}ms", y)
        y += line_height
        render_line(f"Max Frame Time: {metrics.max_frame_time*1000:.1f}ms", y)
        y += line_height
        render_line(f"Avg Frame Time: {metrics.avg_frame_time*1000:.1f}ms", y)
        y += line_height
        render_line(f"Fixed Update Time: {metrics.fixed_update_time*1000:.1f}ms", y)
        y += line_height
        render_line(f"Update Time: {metrics.update_time*1000:.1f}ms", y)
        y += line_height
        render_line(f"Render Time: {metrics.render_time*1000:.1f}ms", y)
        y += line_height
        render_line(f"Idle Time: {metrics.idle_time*1000:.1f}ms", y)

    def render(self) -> None:
        """Render the current game state."""
        # Clear the screen
        self.window.clear(self.background_color)

        # Draw the square
        pygame.draw.rect(
            self.window.surface,
            self.square_color,
            (
                int(self.square_pos[0]),
                int(self.square_pos[1]),
                self.square_size,
                self.square_size,
            ),
        )

        # Draw performance metrics
        self.render_metrics()

        # Present the frame
        self.window.present()


def main() -> None:
    game = Game()
    game.game_loop.run()


if __name__ == "__main__":
    main()
