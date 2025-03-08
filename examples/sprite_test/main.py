"""Example demonstrating the sprite system features."""
import os
import math
import pygame
from src.core import (
    Window, WindowConfig,
    GameLoop, GameLoopConfig,
    InputManager,
    Sprite, SpriteSheet, SpriteFrame, SpriteConfig,
    SpriteRenderer
)

class Game:
    def __init__(self) -> None:
        # Initialize window
        window_config = WindowConfig(
            title="Sprite System Example",
            width=640,
            height=480,
            scale=1,
            vsync=True
        )
        self.window = Window(window_config)

        # Initialize game loop
        loop_config = GameLoopConfig(
            target_fps=60,
            fixed_update_fps=50
        )
        self.game_loop = GameLoop(loop_config)

        # Initialize input
        self.input = InputManager()
        self._setup_input()

        # Set up game loop callbacks
        self.game_loop.update = self.update
        self.game_loop.fixed_update = self.fixed_update
        self.game_loop.render = self.render

        # Load sprite sheet
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        sprite_sheet = SpriteSheet(os.path.join(assets_dir, "character.png"))
        sprite_sheet.add_frames_grid(32, 32)  # 32x32 character frames

        # Create sprite renderer
        self.sprite_renderer = SpriteRenderer()

        # Create test sprites
        self.sprites = []

        # Background sprite (z-index 0)
        bg_config = SpriteConfig(
            x=0, y=0,
            scale_x=20, scale_y=15,  # Scale to fill screen
            z_index=0
        )
        bg_sprite = Sprite(sprite_sheet, bg_config)
        bg_sprite.set_frame(0)  # Use first frame as background
        self.sprite_renderer.add_sprite(bg_sprite)
        self.sprites.append(bg_sprite)

        # Character sprites (z-index 1)
        for i in range(4):
            config = SpriteConfig(
                x=160 + i * 100,
                y=240,
                z_index=1
            )
            sprite = Sprite(sprite_sheet, config)
            sprite.set_frame(i + 1)  # Use different frames
            self.sprite_renderer.add_sprite(sprite)
            self.sprites.append(sprite)

        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)

        # Animation state
        self.time = 0.0

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

    def update(self) -> None:
        """Variable timestep update."""
        self.handle_events()

        if self.input.is_pressed("QUIT"):
            self.game_loop.stop()

    def fixed_update(self) -> None:
        """Fixed timestep update."""
        dt = self.game_loop.fixed_delta_time
        self.time += dt

        # Animate sprites
        for i, sprite in enumerate(self.sprites[1:], 1):  # Skip background
            # Different effects for each sprite
            if i == 1:  # First sprite: rotate
                sprite.config.rotation = int(self.time * 90) % 360
            elif i == 2:  # Second sprite: scale
                scale = 1 + 0.5 * abs(math.sin(self.time * 2))
                sprite.config.scale_x = scale
                sprite.config.scale_y = scale
            elif i == 3:  # Third sprite: fade
                alpha = int(127 + 127 * math.sin(self.time * 2))
                sprite.config.alpha = alpha
            elif i == 4:  # Fourth sprite: flip
                sprite.config.flip_x = int(self.time) % 2 == 0

    def render(self) -> None:
        """Render the current frame."""
        # Clear the screen
        self.window.clear((0, 0, 0))

        # Render all sprites
        self.sprite_renderer.render(self.window.surface)

        # Draw FPS
        fps_text = self.font.render(
            f"FPS: {self.game_loop.metrics.fps:.1f}",
            True,
            (255, 255, 255)
        )
        self.window.surface.blit(fps_text, (10, 10))

        # Present the frame
        self.window.present()

def main() -> None:
    game = Game()
    game.game_loop.run()

if __name__ == "__main__":
    main()
