"""Text UI element for rendering text with optional animation."""
from dataclasses import dataclass, field
from typing import Optional, Tuple

import pygame

from src.core.ui.ui_element import UIElement, UIRect


@dataclass
class TextConfig:
    """Configuration for text rendering."""

    font_size: int = 16
    font_name: str = "arial"
    font_path: Optional[str] = None
    color: Tuple[int, int, int] = (255, 255, 255)
    shadow_color: Tuple[int, int, int] = (0, 0, 0)
    shadow_offset: Optional[Tuple[int, int]] = None
    align: str = "left"  # "left", "center", or "right"
    _animation_speed: float = field(
        default=0.0, init=False
    )  # Characters per second, 0 for instant
    _text_element: Optional["Text"] = field(default=None, init=False)

    @property
    def animation_speed(self) -> float:
        """Get the animation speed."""
        return self._animation_speed

    @animation_speed.setter
    def animation_speed(self, value: float) -> None:
        """Set the animation speed and update animation progress if needed.

        Args:
            value: New animation speed in characters per second
        """
        self._animation_speed = value
        if self._text_element and value > 0:
            self._text_element._animation_progress = 0.0
            self._text_element._needs_update = True


class Text(UIElement):
    """Text UI element with optional animation and shadow effects."""

    def __init__(
        self,
        text: str = "",
        rect: Optional[UIRect] = None,
        config: Optional[TextConfig] = None,
    ) -> None:
        """Initialize the text element.

        Args:
            text: Text to display
            rect: Rectangle defining element bounds and anchors
            config: Text configuration
        """
        super().__init__(rect)
        self.text = text
        self.config = config or TextConfig()
        self.config._text_element = self
        self._font: Optional[pygame.font.Font] = None
        self._surface: Optional[pygame.Surface] = None
        self._animation_progress: float = (
            0.0 if self.config.animation_speed > 0 else len(text)
        )
        self._needs_update = True

        # Initialize font and create initial surface
        self._ensure_font()
        if self.text:
            self._surface = self._create_surface(self.text)

    def set_text(self, text: str) -> None:
        """Set the text content.

        Args:
            text: New text to display
        """
        if self.text != text:
            self.text = text
            # Reset animation progress based on current animation speed
            self._animation_progress = (
                0.0 if self.config.animation_speed > 0 else len(text)
            )
            self._needs_update = True

    def update(self, dt: float) -> None:
        """Update text animation.

        Args:
            dt: Time delta in seconds
        """
        super().update(dt)

        if self.config.animation_speed > 0 and self._animation_progress < len(
            self.text
        ):
            self._animation_progress = min(
                self._animation_progress + self.config.animation_speed * dt,
                len(self.text),
            )
            self._needs_update = True

    def _ensure_font(self) -> None:
        """Ensure the font is loaded."""
        if self._font is None:
            if self.config.font_path:
                try:
                    self._font = pygame.font.Font(
                        self.config.font_path, self.config.font_size
                    )
                except (pygame.error, FileNotFoundError):
                    # Fallback to system font if custom font fails
                    self._font = pygame.font.SysFont(
                        self.config.font_name, self.config.font_size
                    )
            else:
                self._font = pygame.font.SysFont(
                    self.config.font_name, self.config.font_size
                )

    def _create_surface(self, text: str) -> Optional[pygame.Surface]:
        """Create a surface with the rendered text.

        Args:
            text: Text to render

        Returns:
            Surface with rendered text or None if font creation fails
        """
        self._ensure_font()
        if not self._font:
            return None

        # Handle empty text
        if not text:
            return pygame.Surface((1, 1), pygame.SRCALPHA)

        # Create main text surface
        text_surface = self._font.render(text, True, self.config.color)

        # If no shadow, return text surface directly
        if not self.config.shadow_offset:
            return text_surface

        # Create shadow surface
        shadow_surface = self._font.render(text, True, self.config.shadow_color)

        # Create combined surface
        combined = pygame.Surface(
            (
                text_surface.get_width() + abs(self.config.shadow_offset[0]),
                text_surface.get_height() + abs(self.config.shadow_offset[1]),
            ),
            pygame.SRCALPHA,
        )

        # Blit shadow first
        shadow_x = max(0, self.config.shadow_offset[0])
        shadow_y = max(0, self.config.shadow_offset[1])
        combined.blit(shadow_surface, (shadow_x, shadow_y))

        # Blit main text
        text_x = max(0, -self.config.shadow_offset[0])
        text_y = max(0, -self.config.shadow_offset[1])
        combined.blit(text_surface, (text_x, text_y))

        return combined

    def render(self, surface: pygame.Surface) -> None:
        """Render the text element.

        Args:
            surface: Surface to render to
        """
        if not self.visible or not self.text:
            return

        # Update surface if needed
        if self._needs_update or self._surface is None:
            visible_text = self.text[: int(self._animation_progress)]
            self._surface = self._create_surface(visible_text)
            self._needs_update = False

        if not self._surface:
            return

        # Get bounds and handle alignment
        bounds = self.get_bounds()
        if self.config.align == "center":
            x = bounds.x + (bounds.width - self._surface.get_width()) // 2
        elif self.config.align == "right":
            x = bounds.x + bounds.width - self._surface.get_width()
        else:  # left align
            x = bounds.x

        # Render text
        surface.blit(self._surface, (x, bounds.y))

        # Render children
        super().render(surface)
