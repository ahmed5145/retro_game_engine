"""Generate sprite sheet for the platformer example."""
import os

import pygame


def main() -> None:
    """Generate the sprite sheet."""
    # Initialize pygame
    pygame.init()

    # Create sprite sheet surface (64x32 for 2 32x32 sprites)
    surface = pygame.Surface((64, 32), pygame.SRCALPHA)

    # Draw player sprite (first 32x32 tile)
    player_color = (255, 200, 0)  # Yellow-orange
    pygame.draw.rect(surface, player_color, (4, 4, 24, 24))  # Body
    pygame.draw.circle(surface, player_color, (16, 0), 8)  # Head

    # Draw platform sprite (second 32x32 tile)
    platform_color = (100, 100, 100)  # Gray
    platform_border = (80, 80, 80)  # Darker gray

    # Main platform block
    pygame.draw.rect(surface, platform_color, (32, 0, 32, 32))

    # Top edge detail
    pygame.draw.line(surface, platform_border, (32, 0), (64, 0), 2)

    # Bottom edge shadow
    pygame.draw.rect(surface, platform_border, (32, 28, 32, 4))

    # Texture lines
    for i in range(4):
        x = 36 + i * 8
        pygame.draw.line(surface, platform_border, (x, 4), (x, 28), 1)

    # Create assets directory if it doesn't exist
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # Save the sprite sheet
    pygame.image.save(surface, os.path.join(assets_dir, "sprites.png"))
    print("Sprite sheet generated successfully!")


if __name__ == "__main__":
    main()
