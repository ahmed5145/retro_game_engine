"""Example demonstrating the sprite system features."""
import math
import os
from typing import List

import pygame

from src.core import (
    GameLoop,
    GameLoopConfig,
    InputManager,
    Sprite,
    SpriteConfig,
    SpriteFrame,
    SpriteRenderer,
    SpriteSheet,
    Window,
    WindowConfig,
)


class Game:
    def __init__(self) -> None:
        # Initialize window
        window_config = WindowConfig(
            title="Sprite System Example", width=640, height=480, scale=1, vsync=True
        )
        self.window = Window(window_config)

        # Initialize input
        self.input = InputManager()
        self._setup_input()

        # Load sprite sheet
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        sprite_sheet = SpriteSheet(os.path.join(assets_dir, "character.png"))

        # Create sprite renderer
        self.sprite_renderer = SpriteRenderer()
        self.sprites: List[Sprite] = []

        # Background sprites (z-index 0)
        for i in range(3):
            config = SpriteConfig(x=80 + i * 100, y=120, z_index=0)
            sprite = Sprite(sprite_sheet, config)
            sprite.set_frame(i)  # Use different frames
            self.sprite_renderer.add_sprite(sprite)
            self.sprites.append(sprite)

        # Character sprites (z-index 1)
        for i in range(4):
            config = SpriteConfig(x=160 + i * 100, y=240, z_index=1)
            sprite = Sprite(sprite_sheet, config)
            sprite.set_frame(i + 1)  # Use different frames
            self.sprite_renderer.add_sprite(sprite)
            self.sprites.append(sprite)

        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)

        # Animation state
        self.time = 0.0

        # Initialize game loop with callbacks
        loop_config = GameLoopConfig(fps=60)
        self.game_loop = GameLoop(
            update_func=self.update, render_func=self.render, config=loop_config
        )

    def _setup_input(self) -> None:
        """Set up input actions and bindings."""
        self.input.register_action("QUIT")
        self.input.bind_key("QUIT", pygame.K_ESCAPE)

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_loop.stop()
            self.input.process_event(event)

    def update(self, dt: float) -> None:
        """Update game state.

        Args:
            dt: Time delta in seconds
        """
        self.handle_events()

        # Update animation time
        self.time += dt

        # Animate sprites
        for i, sprite in enumerate(self.sprites):
            # Make sprites bob up and down
            amplitude = 10.0  # pixels
            frequency = 2.0  # Hz
            phase = i * 0.5  # offset each sprite
            y_offset = amplitude * math.sin(
                2.0 * math.pi * frequency * self.time + phase
            )
            sprite.config.y = 120 if i < 3 else 240  # Base Y position
            sprite.config.y += y_offset

            # Rotate sprites
            sprite.config.rotation = int(math.sin(self.time + i) * 30.0)  # ±30 degrees

            # Scale sprites
            base_scale = 1.0
            scale_amount = 0.2
            scale = base_scale + math.sin(self.time * 2.0 + i) * scale_amount
            sprite.config.scale_x = scale
            sprite.config.scale_y = scale

    def render(self) -> None:
        """Render the current frame."""
        # Clear screen
        self.window.surface.fill((100, 100, 100))  # Gray background

        # Render all sprites
        self.sprite_renderer.render(self.window.surface)

        # Draw FPS counter
        fps = int(self.game_loop.average_fps)
        fps_text = self.font.render(f"FPS: {fps}", True, (255, 255, 255))
        self.window.surface.blit(fps_text, (10, 10))

        # Update display
        pygame.display.flip()


def main() -> None:
    game = Game()
    game.game_loop.run()


if __name__ == "__main__":
    main()
