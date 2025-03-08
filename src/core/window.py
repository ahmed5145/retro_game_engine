from dataclasses import dataclass
from typing import Tuple
import pygame

@dataclass
class WindowConfig:
    """Configuration for the game window."""
    title: str
    width: int
    height: int
    scale: int = 1
    vsync: bool = True
    fullscreen: bool = False

class Window:
    """Manages the game window and provides basic rendering functionality."""

    def __init__(self, config: WindowConfig):
        """Initialize the window with the given configuration.
        
        Args:
            config: WindowConfig object containing window settings
            
        Raises:
            ValueError: If width, height or scale are invalid
        """
        if config.width <= 0 or config.height <= 0:
            raise ValueError("Window dimensions must be positive")
        if config.scale <= 0:
            raise ValueError("Scale must be positive")

        self.title = config.title
        self.width = config.width
        self.height = config.height
        self.scale = config.scale
        self.vsync = config.vsync

        # Initialize Pygame if not already initialized
        if not pygame.get_init():
            pygame.init()

        # Create the internal surface at the original resolution
        self.surface = pygame.Surface((self.width, self.height))

        # Create the display surface at the scaled resolution
        flags = pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF
        if config.fullscreen:
            flags |= pygame.FULLSCREEN

        self.display_surface = pygame.display.set_mode(
            (self.width * self.scale, self.height * self.scale),
            flags,
            vsync=self.vsync
        )

        pygame.display.set_caption(self.title)

    def clear(self, color: Tuple[int, int, int] = (0, 0, 0)) -> None:
        """Clear the window with the specified color.
        
        Args:
            color: RGB tuple specifying the clear color (default: black)
        """
        self.surface.fill(color)

    def present(self) -> None:
        """Scale and present the internal surface to the display."""
        # Scale the internal surface to the display surface
        pygame.transform.scale(
            self.surface,
            (self.width * self.scale, self.height * self.scale),
            self.display_surface
        )
        # Update the display
        pygame.display.flip()

    def set_title(self, title: str) -> None:
        """Set the window title.
        
        Args:
            title: New window title
        """
        self.title = title
        pygame.display.set_caption(title)

    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode."""
        pygame.display.toggle_fullscreen()

    def __del__(self) -> None:
        """Clean up Pygame resources."""
        pygame.quit()
