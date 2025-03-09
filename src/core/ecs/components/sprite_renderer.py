"""SpriteRenderer component for rendering sprites on entities."""
from dataclasses import dataclass, field
from typing import Optional

import pygame

from src.core.ecs import Component
from src.core.sprite import Sprite, SpriteConfig

from .transform import Transform


@dataclass
class SpriteRenderer(Component):
    """Component for rendering sprites on entities.

    The SpriteRenderer component handles the visual representation of an entity
    using sprites. It requires a Transform component to determine where and how
    to render the sprite.
    """

    sprite: Sprite
    config: SpriteConfig = field(default_factory=SpriteConfig)
    _transform: Optional[Transform] = None

    def __post_init__(self) -> None:
        """Initialize the component after dataclass initialization."""
        super().__init__()

    def on_attach(self) -> None:
        """Called when the component is attached to an entity.

        Verifies that the entity has a Transform component.

        Raises:
            ValueError: If entity doesn't have a Transform component
        """
        if not self.entity:
            return

        self._transform = self.entity.get_component(Transform)
        if not self._transform:
            raise ValueError(
                f"Entity '{self.entity.name}' must have a Transform component"
            )

    def render(self, surface: pygame.Surface) -> None:
        """Render the sprite to the given surface.

        Args:
            surface: Surface to render to
        """
        if not self._transform or not self.enabled:
            return

        # Update sprite configuration from transform
        world_pos = self._transform.get_world_position()
        world_scale = self._transform.get_world_scale()

        self.config.x = world_pos.x
        self.config.y = world_pos.y
        self.config.scale_x = world_scale.x
        self.config.scale_y = world_scale.y
        self.config.rotation = int(self._transform.get_world_rotation())

        # Draw the sprite
        self.sprite.draw(surface)
