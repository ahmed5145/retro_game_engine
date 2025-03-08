"""Example demonstrating the tilemap system features."""
import os
import math
import pygame
from src.core import (
    Window, WindowConfig,
    GameLoop, GameLoopConfig,
    InputManager,
    SpriteSheet, SpriteFrame
)
from src.core.tilemap import Tilemap, TileConfig, TileLayerConfig

class Game:
    def __init__(self) -> None:
        # Initialize window
        window_config = WindowConfig(
            title="Tilemap System Example",
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

        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)

        # Camera position
        self.camera_x: float = 0.0
        self.camera_y: float = 0.0
        self.camera_speed = 200  # Pixels per second

        # Load tileset and create tilemap
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        self.tileset = SpriteSheet(os.path.join(assets_dir, "tileset.png"))
        self.tilemap = Tilemap(32, 32, self.tileset)
        self._setup_tileset()
        self._setup_tilemap()

    def _setup_input(self) -> None:
        """Set up input actions and bindings."""
        # Camera movement
        self.input.register_action("MOVE_LEFT")
        self.input.register_action("MOVE_RIGHT")
        self.input.register_action("MOVE_UP")
        self.input.register_action("MOVE_DOWN")
        self.input.register_action("QUIT")

        self.input.bind_key("MOVE_LEFT", pygame.K_LEFT)
        self.input.bind_key("MOVE_RIGHT", pygame.K_RIGHT)
        self.input.bind_key("MOVE_UP", pygame.K_UP)
        self.input.bind_key("MOVE_DOWN", pygame.K_DOWN)
        self.input.bind_key("QUIT", pygame.K_ESCAPE)

    def _setup_tileset(self) -> None:
        """Set up the tileset frames."""
        # Add frames in a 4x4 grid
        self.tileset.add_frames_grid(32, 32)

        # Configure animated water tiles
        water_config = TileConfig(
            animated=True,
            frames=[4, 5, 6, 7],  # Water animation frames
            frame_duration=0.2
        )
        self.tilemap.set_tile_config(4, water_config)

    def _setup_tilemap(self) -> None:
        """Set up the tilemap layers and tiles."""
        # Background layer (mountains, parallax scrolling)
        bg_config = TileLayerConfig(
            z_index=0,
            scroll_factor_x=0.5,
            scroll_factor_y=0.5
        )
        self.tilemap.add_layer("background", 40, 30, bg_config)  # Doubled size
        bg_layer = self.tilemap.get_layer("background")
        bg_layer.fill(0)  # Mountain tile

        # Water layer (animated)
        water_config = TileLayerConfig(z_index=1)
        self.tilemap.add_layer("water", 40, 30, water_config)  # Doubled size
        water_layer = self.tilemap.get_layer("water")

        # Add some water tiles in a more interesting pattern
        for x in range(40):
            for y in range(30):
                # Create a wavy water pattern
                if 5 <= y <= 20 and (3 <= x <= 36 or (x % 8 < 6)):
                    water_layer.set_tile(x, y, 4)  # Animated water tile

        # Ground layer
        ground_config = TileLayerConfig(z_index=2)
        self.tilemap.add_layer("ground", 40, 30, ground_config)  # Doubled size
        ground_layer = self.tilemap.get_layer("ground")

        # Add ground tiles in a more varied pattern
        for x in range(40):
            base_height = 20 + int(3 * math.sin(x * 0.5))  # Wavy ground
            for y in range(30):
                if y > base_height:
                    ground_layer.set_tile(x, y, 1)  # Ground tile
                elif y == base_height:
                    ground_layer.set_tile(x, y, 2)  # Ground top tile

        # Decoration layer (semi-transparent)
        deco_config = TileLayerConfig(
            z_index=3,
            opacity=192
        )
        self.tilemap.add_layer("decoration", 40, 30, deco_config)  # Doubled size
        deco_layer = self.tilemap.get_layer("decoration")

        # Add decorative tiles in a more interesting pattern
        for x in range(40):
            if x % 4 == 0:  # More frequent trees
                tree_y = 19 + int(3 * math.sin(x * 0.5))  # Place trees on the wavy ground
                deco_layer.set_tile(x, tree_y - 1, 3)  # Tree tile

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_loop.stop()
            self.input.process_event(event)

    def update(self) -> None:
        """Variable timestep update."""
        self.handle_events()
        self.input.update()

        if self.input.is_pressed("QUIT"):
            self.game_loop.stop()

    def fixed_update(self) -> None:
        """Fixed timestep update."""
        dt = self.game_loop.fixed_delta_time

        # Update tilemap animations
        self.tilemap.update(dt)

        # Move camera
        if self.input.is_held("MOVE_LEFT"):
            self.camera_x -= self.camera_speed * dt
        if self.input.is_held("MOVE_RIGHT"):
            self.camera_x += self.camera_speed * dt
        if self.input.is_held("MOVE_UP"):
            self.camera_y -= self.camera_speed * dt
        if self.input.is_held("MOVE_DOWN"):
            self.camera_y += self.camera_speed * dt

        # Clamp camera to map bounds
        max_x = self.tilemap.width * self.tilemap.tile_width - self.window.width
        max_y = self.tilemap.height * self.tilemap.tile_height - self.window.height
        self.camera_x = max(0.0, min(self.camera_x, float(max_x)))
        self.camera_y = max(0.0, min(self.camera_y, float(max_y)))

    def render(self) -> None:
        """Render the current frame."""
        # Clear the screen
        self.window.clear((100, 150, 255))  # Sky blue

        # Render tilemap
        self.tilemap.render(
            self.window.surface,
            int(self.camera_x),
            int(self.camera_y)
        )

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
