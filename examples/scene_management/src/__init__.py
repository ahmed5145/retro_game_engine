"""Demo showcasing scene management and transitions."""
import sys
from typing import Optional

import pygame

from src.core import Window, WindowConfig
from src.core.ecs import World
from src.core.ecs.components import Transform
from src.core.scene import Scene
from src.core.scene_manager import SceneManager
from src.core.vector2d import Vector2D


class MenuScene(Scene):
    """Main menu scene."""

    def __init__(self) -> None:
        """Initialize the menu scene."""
        super().__init__("menu")
        self.font: Optional[pygame.font.Font] = None
        self.selected_option = 0
        self.options = ["Start Game", "Settings", "Exit"]

    def initialize(self) -> None:
        """Initialize scene resources."""
        super().initialize()
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

    def update(self, dt: float) -> None:
        """Update the menu scene.

        Args:
            dt: Delta time in seconds
        """
        super().update(dt)

        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not self.get_environment_variable(
            "key_pressed", False
        ):
            self.selected_option = (self.selected_option - 1) % len(self.options)
            self.set_environment_variable("key_pressed", True)
        elif keys[pygame.K_DOWN] and not self.get_environment_variable(
            "key_pressed", False
        ):
            self.selected_option = (self.selected_option + 1) % len(self.options)
            self.set_environment_variable("key_pressed", True)
        elif keys[pygame.K_RETURN] and not self.get_environment_variable(
            "key_pressed", False
        ):
            self.handle_selection()
            self.set_environment_variable("key_pressed", True)
        elif not any([keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_RETURN]]):
            self.set_environment_variable("key_pressed", False)

    def handle_selection(self) -> None:
        """Handle menu option selection."""
        if self.options[self.selected_option] == "Start Game":
            # Switch to game scene
            game_scene = GameScene()
            self.set_environment_variable("next_scene", ("switch", game_scene))
        elif self.options[self.selected_option] == "Settings":
            # Push settings scene
            settings_scene = SettingsScene()
            self.set_environment_variable("next_scene", ("push", settings_scene))
        elif self.options[self.selected_option] == "Exit":
            self.set_environment_variable("quit", True)

    def render(self, surface: pygame.Surface) -> None:
        """Render the menu scene.

        Args:
            surface: Surface to render to
        """
        surface.fill((0, 0, 0))  # Black background

        if not self.font:
            return

        # Draw title
        title = self.font.render("Scene Management Demo", True, (255, 255, 255))
        surface.blit(title, (400 - title.get_width() // 2, 100))

        # Draw options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.font.render(option, True, color)
            surface.blit(text, (400 - text.get_width() // 2, 250 + i * 50))


class GameScene(Scene):
    """Simple game scene with a moving square."""

    def __init__(self) -> None:
        """Initialize the game scene."""
        super().__init__("game")
        self.square_pos = Vector2D(400, 300)
        self.square_vel = Vector2D(100, 100)
        self.font: Optional[pygame.font.Font] = None

    def initialize(self) -> None:
        """Initialize scene resources."""
        super().initialize()
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)

    def update(self, dt: float) -> None:
        """Update the game scene.

        Args:
            dt: Delta time in seconds
        """
        super().update(dt)

        # Move square
        self.square_pos += self.square_vel * dt

        # Bounce off edges
        if self.square_pos.x < 0 or self.square_pos.x > 800:
            self.square_vel.x *= -1
        if self.square_pos.y < 0 or self.square_pos.y > 600:
            self.square_vel.y *= -1

        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and not self.get_environment_variable(
            "key_pressed", False
        ):
            self.set_environment_variable("next_scene", ("pop", None))
            self.set_environment_variable("key_pressed", True)
        elif not keys[pygame.K_ESCAPE]:
            self.set_environment_variable("key_pressed", False)

    def render(self, surface: pygame.Surface) -> None:
        """Render the game scene.

        Args:
            surface: Surface to render to
        """
        surface.fill((0, 0, 128))  # Dark blue background

        # Draw square
        pygame.draw.rect(
            surface,
            (0, 255, 0),
            (int(self.square_pos.x - 20), int(self.square_pos.y - 20), 40, 40),
        )

        if self.font:
            # Draw instructions
            text = self.font.render(
                "Press ESC to return to menu", True, (255, 255, 255)
            )
            surface.blit(text, (10, 10))


class SettingsScene(Scene):
    """Settings scene."""

    def __init__(self) -> None:
        """Initialize the settings scene."""
        super().__init__("settings")
        self.font: Optional[pygame.font.Font] = None
        self.selected_option = 0
        self.options = ["Volume: 100%", "Fullscreen: Off", "Back"]

    def initialize(self) -> None:
        """Initialize scene resources."""
        super().initialize()
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

    def update(self, dt: float) -> None:
        """Update the settings scene.

        Args:
            dt: Delta time in seconds
        """
        super().update(dt)

        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not self.get_environment_variable(
            "key_pressed", False
        ):
            self.selected_option = (self.selected_option - 1) % len(self.options)
            self.set_environment_variable("key_pressed", True)
        elif keys[pygame.K_DOWN] and not self.get_environment_variable(
            "key_pressed", False
        ):
            self.selected_option = (self.selected_option + 1) % len(self.options)
            self.set_environment_variable("key_pressed", True)
        elif keys[pygame.K_RETURN] and not self.get_environment_variable(
            "key_pressed", False
        ):
            if self.options[self.selected_option] == "Back":
                self.set_environment_variable("next_scene", ("pop", None))
            self.set_environment_variable("key_pressed", True)
        elif not any([keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_RETURN]]):
            self.set_environment_variable("key_pressed", False)

    def render(self, surface: pygame.Surface) -> None:
        """Render the settings scene.

        Args:
            surface: Surface to render to
        """
        surface.fill((32, 32, 32))  # Dark gray background

        if not self.font:
            return

        # Draw title
        title = self.font.render("Settings", True, (255, 255, 255))
        surface.blit(title, (400 - title.get_width() // 2, 100))

        # Draw options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.font.render(option, True, color)
            surface.blit(text, (400 - text.get_width() // 2, 250 + i * 50))


def main() -> None:
    """Run the scene management demo."""
    # Initialize pygame and create window
    pygame.init()
    config = WindowConfig(
        title="Scene Management Demo", width=800, height=600, scale=1, vsync=True
    )
    window = Window(config)

    # Create scene manager and register scenes
    scene_manager = SceneManager()
    menu_scene = MenuScene()
    scene_manager.register_scene(menu_scene)
    scene_manager.push_scene(menu_scene)

    # Main game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update current scene
        dt = clock.tick(60) / 1000.0
        if current_scene := scene_manager.current_scene:
            current_scene.update(dt)

            # Handle scene transitions
            if next_scene := current_scene.get_environment_variable("next_scene"):
                action, scene = next_scene
                if action == "push":
                    scene_manager.push_scene(scene)
                elif action == "pop":
                    scene_manager.pop_scene()
                elif action == "switch":
                    scene_manager.switch_scene(scene)
                current_scene.set_environment_variable("next_scene", None)

            # Handle quit
            if current_scene.get_environment_variable("quit"):
                running = False

            # Render current scene
            window.clear()
            current_scene.render(window.surface)
            window.present()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
