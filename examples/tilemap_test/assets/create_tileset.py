"""Script to generate a simple tileset image for the tilemap example."""
import os

import pygame


def create_tileset() -> None:
    """Create a simple tileset image."""
    # Initialize pygame
    pygame.init()

    # Create a 128x128 surface (4x4 tiles of 32x32 pixels)
    surface = pygame.Surface((128, 128))

    # Define colors
    MOUNTAIN = (100, 100, 100)  # Gray
    GROUND = (139, 69, 19)  # Brown
    GROUND_TOP = (34, 139, 34)  # Green
    TREE = (0, 100, 0)  # Dark green
    WATER = [
        (0, 0, 139),  # Dark blue
        (0, 0, 159),  # Slightly lighter blue
        (0, 0, 179),  # Even lighter blue
        (0, 0, 199),  # Lightest blue
    ]

    # Draw tiles (4x4 grid)
    tile_size = 32

    # Mountains (0)
    pygame.draw.rect(surface, MOUNTAIN, (0, 0, tile_size, tile_size))
    pygame.draw.polygon(surface, (80, 80, 80), [(4, 28), (16, 4), (28, 28)])

    # Ground (1)
    pygame.draw.rect(surface, GROUND, (tile_size, 0, tile_size, tile_size))

    # Ground top (2)
    pygame.draw.rect(surface, GROUND, (tile_size * 2, 0, tile_size, tile_size))
    pygame.draw.rect(surface, GROUND_TOP, (tile_size * 2, 0, tile_size, tile_size // 2))

    # Tree (3)
    pygame.draw.rect(
        surface, (139, 69, 19), (tile_size * 3, tile_size - 10, 6, 10)
    )  # Trunk
    pygame.draw.circle(surface, TREE, (tile_size * 3 + 8, tile_size - 12), 12)  # Leaves

    # Water animation frames (4-7)
    for i, color in enumerate(WATER):
        x = (i % 4) * tile_size
        y = tile_size
        pygame.draw.rect(surface, color, (x, y, tile_size, tile_size))
        # Add wave effect
        wave_color = (
            min(color[0] + 20, 255),
            min(color[1] + 20, 255),
            min(color[2] + 20, 255),
        )
        for j in range(3):
            wave_y = y + 8 + j * 8
            pygame.draw.line(surface, wave_color, (x + 4, wave_y), (x + 28, wave_y), 2)

    # Save the tileset
    assets_dir = os.path.dirname(__file__)
    pygame.image.save(surface, os.path.join(assets_dir, "tileset.png"))


if __name__ == "__main__":
    create_tileset()
