"""Core sprite system implementation."""
from dataclasses import dataclass
from typing import Tuple, List, Optional
import pygame

@dataclass
class SpriteFrame:
    """A single frame from a sprite sheet."""
    x: int
    y: int
    width: int
    height: int

@dataclass
class SpriteConfig:
    """Configuration for a sprite."""
    x: float = 0.0
    y: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    rotation: int = 0  # Degrees, must be multiple of 90
    flip_x: bool = False
    flip_y: bool = False
    alpha: int = 255
    z_index: int = 0

class SpriteSheet:
    """Manages a sprite sheet texture and its frames."""

    def __init__(self, texture_path: str):
        """Initialize the sprite sheet.
        
        Args:
            texture_path: Path to the sprite sheet image
            
        Raises:
            FileNotFoundError: If texture file doesn't exist
            pygame.error: If texture file is invalid
        """
        self.texture = pygame.image.load(texture_path).convert_alpha()
        self.frames: List[SpriteFrame] = []

    def add_frame(self, frame: SpriteFrame) -> int:
        """Add a frame to the sprite sheet.
        
        Args:
            frame: Frame to add
            
        Returns:
            Index of the added frame
            
        Raises:
            ValueError: If frame coordinates are invalid
        """
        # Validate frame bounds
        if (frame.x < 0 or frame.y < 0 or
            frame.width <= 0 or frame.height <= 0 or
            frame.x + frame.width > self.texture.get_width() or
            frame.y + frame.height > self.texture.get_height()):
            raise ValueError("Invalid frame coordinates")

        self.frames.append(frame)
        return len(self.frames) - 1

    def add_frames_grid(self, frame_width: int, frame_height: int,
                       margin: int = 0, spacing: int = 0) -> None:
        """Add frames in a grid layout.
        
        Args:
            frame_width: Width of each frame
            frame_height: Height of each frame
            margin: Margin around the frames (default: 0)
            spacing: Spacing between frames (default: 0)
            
        Raises:
            ValueError: If frame size or spacing is invalid
        """
        if frame_width <= 0 or frame_height <= 0:
            raise ValueError("Frame dimensions must be positive")
        if margin < 0 or spacing < 0:
            raise ValueError("Margin and spacing must be non-negative")

        texture_width = self.texture.get_width()
        texture_height = self.texture.get_height()

        # Validate that at least one frame will fit
        if (margin * 2 + frame_width > texture_width or
            margin * 2 + frame_height > texture_height):
            raise ValueError("Frame dimensions with margin exceed texture size")

        x = margin
        y = margin

        while y + frame_height <= texture_height - margin:
            while x + frame_width <= texture_width - margin:
                self.add_frame(SpriteFrame(x, y, frame_width, frame_height))
                x += frame_width + spacing
            x = margin
            y += frame_height + spacing

class Sprite:
    """A drawable sprite with transform and animation capabilities."""

    def __init__(self, sprite_sheet: SpriteSheet, config: Optional[SpriteConfig] = None):
        """Initialize the sprite.
        
        Args:
            sprite_sheet: SpriteSheet containing the sprite's frames
            config: Initial configuration (default: None)
        """
        self.sprite_sheet = sprite_sheet
        self.config = config or SpriteConfig()
        self.current_frame = 0

    def set_frame(self, frame_index: int) -> None:
        """Set the current frame.
        
        Args:
            frame_index: Index of the frame to display
            
        Raises:
            IndexError: If frame_index is out of range
        """
        if not 0 <= frame_index < len(self.sprite_sheet.frames):
            raise IndexError("Frame index out of range")
        self.current_frame = frame_index

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the sprite to a surface.
        
        Args:
            surface: Surface to draw on
        """
        if not self.sprite_sheet.frames:
            return

        frame = self.sprite_sheet.frames[self.current_frame]

        # Extract the frame from the sprite sheet
        frame_surface = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
        frame_surface.blit(
            self.sprite_sheet.texture,
            (0, 0),
            (frame.x, frame.y, frame.width, frame.height)
        )

        # Apply transformations
        if self.config.flip_x or self.config.flip_y:
            frame_surface = pygame.transform.flip(
                frame_surface,
                self.config.flip_x,
                self.config.flip_y
            )

        if self.config.rotation != 0:
            frame_surface = pygame.transform.rotate(frame_surface, self.config.rotation)

        if self.config.scale_x != 1.0 or self.config.scale_y != 1.0:
            new_width = int(frame.width * abs(self.config.scale_x))
            new_height = int(frame.height * abs(self.config.scale_y))
            if new_width > 0 and new_height > 0:
                frame_surface = pygame.transform.scale(
                    frame_surface,
                    (new_width, new_height)
                )

        if self.config.alpha != 255:
            frame_surface.set_alpha(self.config.alpha)

        # Draw to the target surface
        surface.blit(
            frame_surface,
            (int(self.config.x), int(self.config.y))
        )
