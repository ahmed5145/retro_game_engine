"""Generate sprite sheet for the example."""
import os
import pygame

def main() -> None:
    """Generate the sprite sheet."""
    # Initialize pygame
    pygame.init()

    # Create sprite sheet surface (5x5 grid of 32x32 sprites)
    width = 32 * 5
    height = 32 * 5
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Colors for different sprites
    colors = [
        (200, 200, 200),  # Light gray for background
        (255, 100, 100),  # Red
        (100, 255, 100),  # Green
        (100, 100, 255),  # Blue
        (255, 255, 100),  # Yellow
        (255, 100, 255),  # Magenta
        (100, 255, 255),  # Cyan
    ]

    # Draw background sprite (first sprite)
    pygame.draw.rect(surface, colors[0], (0, 0, 32, 32))
    pygame.draw.rect(surface, (150, 150, 150), (0, 0, 32, 32), 1)  # Border

    # Draw character sprites
    for i in range(1, len(colors)):
        x = (i % 5) * 32
        y = (i // 5) * 32

        # Draw colored square with border
        pygame.draw.rect(surface, colors[i], (x, y, 32, 32))
        pygame.draw.rect(surface, (0, 0, 0), (x, y, 32, 32), 1)  # Border

        # Add some simple details
        pygame.draw.circle(surface, (255, 255, 255), (x + 16, y + 12), 4)  # Eyes
        pygame.draw.arc(surface, (0, 0, 0), (x + 8, y + 8, 16, 16), 0, 3.14)  # Smile

    # Create assets directory if it doesn't exist
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # Save the sprite sheet
    pygame.image.save(surface, os.path.join(assets_dir, "character.png"))

    pygame.quit()

if __name__ == "__main__":
    main()
