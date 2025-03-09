import sys
from typing import List, Tuple

import pygame

from src.core import Window, WindowConfig
from src.core.game_loop import GameLoop, GameLoopConfig
from src.core.input import InputManager


class Game:
    def __init__(self) -> None:
        # Initialize window
        window_config = WindowConfig(
            title="Input System Example", width=640, height=480, scale=1, vsync=True
        )
        self.window = Window(window_config)

        # Initialize input manager
        self.input = InputManager()
        self._setup_input()

        # Game state
        self.player_pos: List[float] = [320.0, 240.0]  # Center of screen
        self.player_vel: List[float] = [0.0, 0.0]
        self.player_size = 50
        self.move_speed = 300.0  # Pixels per second
        self.jump_force = -500.0  # Negative is up
        self.gravity = 1000.0
        self.on_ground = False

        # Colors
        self.player_color = (255, 0, 0)  # Red
        self.background_color = (0, 0, 0)  # Black
        self.text_color = (255, 255, 255)  # White
        self.ground_color = (0, 255, 0)  # Green

        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)  # Default font, size 24

        # Initialize game loop with callbacks
        loop_config = GameLoopConfig(fps=60)
        self.game_loop = GameLoop(
            update_func=self.update, render_func=self.render, config=loop_config
        )

    def _setup_input(self) -> None:
        """Set up input actions and bindings."""
        # Register actions
        self.input.register_action("MOVE_LEFT")
        self.input.register_action("MOVE_RIGHT")
        self.input.register_action("JUMP", buffer_time=0.1)  # 100ms jump buffer
        self.input.register_action("QUIT")

        # Set up key bindings
        self.input.bind_key("MOVE_LEFT", pygame.K_LEFT)
        self.input.bind_key("MOVE_LEFT", pygame.K_a)
        self.input.bind_key("MOVE_RIGHT", pygame.K_RIGHT)
        self.input.bind_key("MOVE_RIGHT", pygame.K_d)
        self.input.bind_key("JUMP", pygame.K_SPACE)
        self.input.bind_key("JUMP", pygame.K_w)
        self.input.bind_key("JUMP", pygame.K_UP)
        self.input.bind_key("QUIT", pygame.K_ESCAPE)

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_loop.stop()
            # Pass events to input manager
            self.input.process_event(event)

    def update(self, dt: float) -> None:
        """Update game state.

        Args:
            dt: Time delta in seconds
        """
        self.handle_events()

        # Check for quit
        if self.input.is_pressed("QUIT"):
            self.game_loop.stop()

        # Apply physics
        # Handle horizontal movement
        move_dir = 0.0
        if self.input.is_held("MOVE_LEFT"):
            move_dir -= 1.0
        if self.input.is_held("MOVE_RIGHT"):
            move_dir += 1.0

        self.player_vel[0] = move_dir * self.move_speed

        # Handle jumping
        if self.on_ground and (
            self.input.is_pressed("JUMP") or self.input.is_buffered("JUMP")
        ):
            self.player_vel[1] = self.jump_force
            self.on_ground = False

        # Apply gravity
        if not self.on_ground:
            self.player_vel[1] += self.gravity * dt

        # Update position
        self.player_pos[0] += self.player_vel[0] * dt
        self.player_pos[1] += self.player_vel[1] * dt

        # Handle ground collision
        ground_y = self.window.height - self.player_size
        if self.player_pos[1] > ground_y:
            self.player_pos[1] = ground_y
            self.player_vel[1] = 0
            self.on_ground = True

        # Handle wall collisions
        if self.player_pos[0] < 0:
            self.player_pos[0] = 0
            self.player_vel[0] = 0
        elif self.player_pos[0] > self.window.width - self.player_size:
            self.player_pos[0] = self.window.width - self.player_size
            self.player_vel[0] = 0

    def render(self) -> None:
        """Render the current frame."""
        # Clear screen
        self.window.surface.fill(self.background_color)

        # Draw ground
        ground_rect = pygame.Rect(0, self.window.height - 10, self.window.width, 10)
        pygame.draw.rect(self.window.surface, self.ground_color, ground_rect)

        # Draw player
        player_rect = pygame.Rect(
            int(self.player_pos[0]),
            int(self.player_pos[1]),
            self.player_size,
            self.player_size,
        )
        pygame.draw.rect(self.window.surface, self.player_color, player_rect)

        # Draw input state
        y = 10
        for action in ["MOVE_LEFT", "MOVE_RIGHT", "JUMP"]:
            text = f"{action}: Pressed={self.input.is_pressed(action)}, Held={self.input.is_held(action)}"
            if action == "JUMP":
                text += f", Buffered={self.input.is_buffered(action)}"
            surface = self.font.render(text, True, self.text_color)
            self.window.surface.blit(surface, (10, y))
            y += 30

        # Update display
        pygame.display.flip()


def main() -> None:
    game = Game()
    game.game_loop.run()


if __name__ == "__main__":
    main()
