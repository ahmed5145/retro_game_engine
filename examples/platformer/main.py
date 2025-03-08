"""Simple platformer example using the Entity Component System."""
import sys

import pygame

from examples.platformer.components import BoxCollider, Physics, PlayerController
from examples.platformer.systems import collision_system, physics_system, player_system
from src.core.ecs import World
from src.core.ecs.components import SpriteRenderer, Transform
from src.core.sprite import Sprite, SpriteSheet
from src.core.vector2d import Vector2D


class PlatformerGame:
    """Simple platformer game using ECS."""

    def __init__(self) -> None:
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Platformer Example")
        self.clock = pygame.time.Clock()
        self.running = True

        # Create world
        self.world = World()

        # Load assets and create entities
        self.setup_game()

    def setup_game(self) -> None:
        """Set up the initial game state."""
        # Create player
        player = self.world.create_entity("player")
        player.add_component(Transform(position=Vector2D(400, 300)))
        player.add_component(PlayerController())
        player.add_component(Physics())
        player.add_component(BoxCollider(width=32, height=32))

        # TODO: Add sprite renderer once we have player sprite
        # player.add_component(SpriteRenderer(player_sprite))

        # Create platforms
        # Main ground platform
        self.create_platform(400, 550, 600, 32)  # Ground

        # Left side platforms
        self.create_platform(150, 450, 200, 32)  # Left platform
        self.create_platform(150, 350, 100, 32)  # Upper left platform

        # Right side platforms
        self.create_platform(650, 450, 200, 32)  # Right platform
        self.create_platform(650, 350, 100, 32)  # Upper right platform

        # Middle platform
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
        platform.add_component(Transform(position=Vector2D(x, y)))
        platform.add_component(BoxCollider(width=width, height=height, is_static=True))
        # TODO: Add sprite renderer once we have platform sprite

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
        physics_system(self.world, dt)
        collision_system(self.world, dt)

    def render(self) -> None:
        """Render the game."""
        self.screen.fill((100, 100, 255))  # Sky blue background

        # TODO: Add rendering system
        # for entity in self.world.get_entities_with_component(SpriteRenderer):
        #     renderer = entity.get_component(SpriteRenderer)
        #     if renderer:
        #         renderer.render(self.screen)

        # Debug rendering
        for entity in self.world.get_entities_with_component(BoxCollider):
            collider = entity.get_component(BoxCollider)
            transform = entity.get_component(Transform)
            if collider and transform:
                rect = pygame.Rect(
                    transform.position.x - collider.width / 2,
                    transform.position.y - collider.height / 2,
                    collider.width,
                    collider.height,
                )
                color = (255, 0, 0) if collider.is_static else (0, 255, 0)
                pygame.draw.rect(self.screen, color, rect, 2)

        pygame.display.flip()

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
