"""Platformer example game using the Entity Component System."""
import os
import sys
from typing import List

import pygame

from examples.platformer.components import BoxCollider, Physics, PlayerController
from examples.platformer.systems import PhysicsSystem, collision_system, player_system
from src.core.ecs import World
from src.core.ecs.components import SpriteRenderer, Transform
from src.core.sprite import Sprite, SpriteConfig, SpriteFrame, SpriteSheet
from src.core.vector2d import Vector2D
from src.core.window import Window, WindowConfig


class PlatformerGame:
    """Simple platformer game example."""

    def __init__(self) -> None:
        """Initialize the game."""
        # Initialize window
        config = WindowConfig(
            title="Platformer Example", width=800, height=600, scale=1, vsync=True
        )
        self.window = Window(config)
        self.world = World()
        self.running = True
        self.clock = pygame.time.Clock()
        self.physics_system = PhysicsSystem()

        # Load sprites
        self.sprite_sheet = self._load_sprites()

        # Set up game
        self.setup_game()

    def _load_sprites(self) -> SpriteSheet:
        """Load game sprites.

        Returns:
            Loaded sprite sheet
        """
        # Create sprite sheet
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        sprite_sheet = SpriteSheet(os.path.join(assets_dir, "sprites.png"))

        # Add frames
        sprite_sheet.add_frame(SpriteFrame(0, 0, 32, 32))  # Player
        sprite_sheet.add_frame(SpriteFrame(32, 0, 32, 32))  # Platform

        return sprite_sheet

    def setup_game(self) -> None:
        """Set up the initial game state."""
        # Create player
        player = self.world.create_entity("player")
        if player:  # Type guard
            player.add_component(Transform(position=Vector2D(400, 300)))
            player.add_component(PlayerController())
            player.add_component(Physics())
            player.add_component(BoxCollider(width=32, height=32))

            # Add player sprite
            player_sprite = Sprite(self.sprite_sheet)
            player_sprite.set_frame(0)  # Use first frame for player
            player.add_component(SpriteRenderer(sprite=player_sprite))

        # Create ground
        self.create_platform(400, 500, 800, 32)  # Ground
        self.create_platform(200, 400, 200, 32)  # Left platform
        self.create_platform(650, 450, 200, 32)  # Right platform
        self.create_platform(650, 350, 100, 32)  # Upper right platform
        self.create_platform(400, 250, 200, 32)  # Top middle platform

    def create_platform(self, x: float, y: float, width: float, height: float) -> None:
        """Create a platform entity.

        Args:
            x: X position
            y: Y position
            width: Platform width
            height: Platform height
        """
        platform = self.world.create_entity("platform")
        if platform:  # Type guard
            platform.add_component(Transform(position=Vector2D(x, y)))
            platform.add_component(
                BoxCollider(width=width, height=height, is_static=True)
            )

            # Add sprite renderer with proper scaling
            sprite = Sprite(self.sprite_sheet)
            sprite.set_frame(1)  # Use second frame for platform
            renderer = SpriteRenderer(sprite=sprite)
            renderer.config.scale_x = width / 32  # Scale to match collider width
            renderer.config.scale_y = height / 32  # Scale to match collider height
            platform.add_component(renderer)

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self) -> None:
        """Update game state."""
        dt = self.clock.tick(60) / 1000.0

        # Run systems
        player_system(self.world, dt)
        self.physics_system.update(self.world, dt)
        collision_system(self.world, dt)

    def render(self) -> None:
        """Render the game."""
        # Clear window
        self.window.clear((100, 100, 255))  # Sky blue background

        # Get all sprite renderers
        renderers: List[SpriteRenderer] = []
        for entity in self.world._entities.values():
            if not entity:
                continue
            renderer = entity.get_component(SpriteRenderer)
            transform = entity.get_component(Transform)
            if renderer and transform:
                renderers.append(renderer)

        # Sort by Y position for basic depth
        def get_y_position(renderer: SpriteRenderer) -> float:
            if not renderer.entity:
                return 0.0
            transform = renderer.entity.get_component(Transform)
            if not transform:
                return 0.0
            return transform.position.y

        renderers.sort(key=get_y_position)

        # Render all sprites
        for renderer in renderers:
            renderer.render(self.window.surface)

        # Present frame
        self.window.present()

    def run(self) -> None:
        """Run the game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = PlatformerGame()
    game.run()
