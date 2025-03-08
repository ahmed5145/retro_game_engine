"""Sprite rendering system with batching and z-ordering."""
from typing import List, Dict
import pygame
from .sprite import Sprite

class SpriteRenderer:
    """Handles efficient rendering of multiple sprites with z-ordering."""

    def __init__(self) -> None:
        """Initialize the sprite renderer."""
        self.sprites: Dict[int, List[Sprite]] = {}  # z-index -> sprites

    def add_sprite(self, sprite: Sprite) -> None:
        """Add a sprite to be rendered.
        
        Args:
            sprite: Sprite to add
        """
        z_index = sprite.config.z_index
        if z_index not in self.sprites:
            self.sprites[z_index] = []
        self.sprites[z_index].append(sprite)

    def remove_sprite(self, sprite: Sprite) -> None:
        """Remove a sprite from rendering.
        
        Args:
            sprite: Sprite to remove
        """
        z_index = sprite.config.z_index
        if z_index in self.sprites and sprite in self.sprites[z_index]:
            self.sprites[z_index].remove(sprite)
            if not self.sprites[z_index]:
                del self.sprites[z_index]

    def clear(self) -> None:
        """Remove all sprites."""
        self.sprites.clear()

    def render(self, surface: pygame.Surface) -> None:
        """Render all sprites in order of z-index.
        
        Args:
            surface: Surface to render to
        """
        # Sort z-indices for proper layering
        for z_index in sorted(self.sprites.keys()):
            # Batch render all sprites at this z-index
            for sprite in self.sprites[z_index]:
                sprite.draw(surface)
