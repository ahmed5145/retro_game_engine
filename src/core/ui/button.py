"""Button UI element with text and interaction states."""
from dataclasses import dataclass
from typing import Callable, Optional, Tuple, cast

import pygame

from src.core.ui.text import Text
from src.core.ui.ui_element import UIElement, UIElementConfig


@dataclass
class ButtonStyle:
    """Visual style configuration for buttons.

    Attributes:
        background_color: Normal state background color
        hover_color: Background color when mouse is over button
        pressed_color: Background color when button is pressed
        border_color: Color of button border
        border_width: Width of button border in pixels
        corner_radius: Radius for rounded corners (0 for square)
        padding: Padding around text (left, top, right, bottom)
    """

    background_color: Tuple[int, int, int] = (100, 100, 100)
    hover_color: Tuple[int, int, int] = (120, 120, 120)
    pressed_color: Tuple[int, int, int] = (80, 80, 80)
    border_color: Tuple[int, int, int] = (50, 50, 50)
    border_width: int = 2
    corner_radius: int = 5
    padding: Tuple[int, int, int, int] = (10, 5, 10, 5)


class Button(UIElement):
    """Interactive button UI element with text and click handling."""

    def __init__(self, text: str, rect: UIElementConfig, style: ButtonStyle) -> None:
        """Initialize the button.

        Args:
            text: Text to display on the button
            rect: Position and size of the button
            style: Visual style configuration
        """
        super().__init__(rect)
        text_rect = UIElementConfig(x=0, y=0, width=rect.width, height=rect.height)
        self.text_element = Text(text, text_rect)
        self.text_element.parent = self
        self.style = style
        self._hovered = False
        self._pressed = False
        self.on_click: Optional[Callable[[], None]] = None
        self._surface: Optional[pygame.Surface] = None
        self._needs_update = True

    def set_text(self, text: str) -> None:
        """Set the button's text.

        Args:
            text: New text to display
        """
        self.text_element.set_text(text)
        self._needs_update = True

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input events.

        Args:
            event: Pygame event to handle

        Returns:
            True if event was handled
        """
        if not self._enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            was_hovered = self._hovered
            self._hovered = self.contains_point(event.pos)
            if was_hovered != self._hovered:
                self._needs_update = True
            return self._hovered

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.contains_point(event.pos):
                self._pressed = True
                self._needs_update = True
                return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self._pressed
            self._pressed = False
            if was_pressed and self.contains_point(event.pos):
                if self.on_click is not None:
                    self.on_click()
            self._needs_update = True
            return was_pressed

        return False

    def render(self, surface: pygame.Surface) -> None:
        """Render the button.

        Args:
            surface: Surface to render to
        """
        if not self.visible:
            return

        bounds = self.get_bounds()

        # Determine current color based on state
        if not self.enabled:
            color = self.style.background_color
        elif self._pressed:
            color = self.style.pressed_color
        elif self._hovered:
            color = self.style.hover_color
        else:
            color = self.style.background_color

        # Create button surface if needed
        if self._needs_update or self._surface is None:
            self._surface = pygame.Surface(
                (bounds.width, bounds.height), pygame.SRCALPHA
            )

            # Draw background
            if self.style.corner_radius > 0:
                pygame.draw.rect(
                    self._surface,
                    color,
                    (0, 0, bounds.width, bounds.height),
                    border_radius=self.style.corner_radius,
                )
                if self.style.border_width > 0:
                    pygame.draw.rect(
                        self._surface,
                        self.style.border_color,
                        (0, 0, bounds.width, bounds.height),
                        width=self.style.border_width,
                        border_radius=self.style.corner_radius,
                    )
            else:
                pygame.draw.rect(
                    self._surface, color, (0, 0, bounds.width, bounds.height)
                )
                if self.style.border_width > 0:
                    pygame.draw.rect(
                        self._surface,
                        self.style.border_color,
                        (0, 0, bounds.width, bounds.height),
                        width=self.style.border_width,
                    )

            self._needs_update = False

        # Draw button background
        surface.blit(self._surface, (bounds.x, bounds.y))

        # Draw text
        self.text_element.render(surface)

    def update(self, dt: float) -> None:
        """Update button state.

        Args:
            dt: Time delta in seconds
        """
        super().update(dt)
        self.text_element.update(dt)

        # Update hover state
        mouse_pos = pygame.mouse.get_pos()
        bounds = self.get_bounds()
        self._hovered = (
            bounds.x <= mouse_pos[0] <= bounds.x + bounds.width
            and bounds.y <= mouse_pos[1] <= bounds.y + bounds.height
        )

        # Handle click
        if self._hovered and self._pressed and not pygame.mouse.get_pressed()[0]:
            self._pressed = False
            if self.on_click:
                self.on_click()
        elif self._hovered and pygame.mouse.get_pressed()[0]:
            self._pressed = True
        elif not pygame.mouse.get_pressed()[0]:
            self._pressed = False

        self._needs_update = False
