"""Button UI element with text and interaction states."""
from dataclasses import dataclass
from typing import Callable, Optional, Tuple, cast

import pygame

from src.core.ui.text import Text, TextConfig
from src.core.ui.ui_element import UIElement, UIRect


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
        text_config: Text configuration
    """

    background_color: Tuple[int, int, int] = (100, 100, 100)
    hover_color: Tuple[int, int, int] = (120, 120, 120)
    pressed_color: Tuple[int, int, int] = (80, 80, 80)
    border_color: Optional[Tuple[int, int, int]] = None
    border_width: int = 0
    corner_radius: int = 0
    padding: Tuple[int, int, int, int] = (0, 0, 0, 0)
    text_config: Optional[TextConfig] = None


class Button(UIElement):
    """Interactive button UI element with text and click handling."""

    def __init__(self, text: str, rect: UIRect, style: ButtonStyle) -> None:
        """Initialize the button.

        Args:
            text: Text to display on the button
            rect: Position and size of the button
            style: Visual style configuration
        """
        super().__init__(rect)

        self.style = style
        self._hovered = False
        self._pressed = False
        self._on_click: Optional[Callable[[], None]] = None
        self._last_mouse_pos = (0, 0)

        # Create text element
        text_rect = UIRect(
            x=style.padding[0],
            y=style.padding[1],
            width=rect.width - style.padding[0] - style.padding[2],
            height=rect.height - style.padding[1] - style.padding[3],
            anchor_x=0.5,
            anchor_y=0.5,
        )
        self.text_element = Text(text, text_rect, style.text_config)
        self.add_child(self.text_element)

    @property
    def text(self) -> str:
        """Get the button's text.

        Returns:
            Current button text
        """
        return self.text_element.text

    @text.setter
    def text(self, value: str) -> None:
        """Set the button's text.

        Args:
            value: New text to display
        """
        self.text_element.text = value

    def set_text(self, text: str) -> None:
        """Set the button's text (legacy method)."""
        self.text = text

    @property
    def on_click(self) -> Optional[Callable[[], None]]:
        """Get the click handler."""
        return self._on_click

    @on_click.setter
    def on_click(self, value: Optional[Callable[[], None]]) -> None:
        """Set the click handler."""
        self._on_click = value

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle pygame events.

        Args:
            event: The pygame event to handle

        Returns:
            True if the event was handled, False otherwise
        """
        if not self.enabled or not self.visible:
            return False

        if hasattr(event, "pos"):
            self._last_mouse_pos = event.pos

        bounds = self.get_bounds()
        mouse_over = bounds.collidepoint(self._last_mouse_pos)

        if event.type == pygame.MOUSEMOTION:
            was_hovered = self._hovered
            self._hovered = mouse_over
            return was_hovered != self._hovered
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if mouse_over:
                self._hovered = True
                self._pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self._pressed
            self._pressed = False
            if was_pressed and mouse_over and self._on_click is not None:
                self._on_click()
            return was_pressed

        return False

    def render(self, surface: pygame.Surface) -> None:
        """Render the button.

        Args:
            surface: Surface to render to
        """
        if not self.visible:
            return

        # Get current color based on state
        color = self.style.background_color
        if self._pressed:
            color = self.style.pressed_color
        elif self._hovered:
            color = self.style.hover_color

        # Draw background
        rect = pygame.Rect(
            self.screen_rect.x,
            self.screen_rect.y,
            self.screen_rect.width,
            self.screen_rect.height,
        )
        if self.style.corner_radius > 0:
            pygame.draw.rect(
                surface,
                color,
                rect,
                border_radius=self.style.corner_radius,
            )
        else:
            pygame.draw.rect(surface, color, rect)

        # Draw border
        if self.style.border_color and self.style.border_width > 0:
            pygame.draw.rect(
                surface,
                self.style.border_color,
                rect,
                self.style.border_width,
                border_radius=self.style.corner_radius,
            )

        # Render text
        super().render(surface)

    def update(self, dt: float) -> None:
        """Update button state.

        Args:
            dt: Time delta in seconds
        """
        super().update(dt)

        # Update text element state
        self.text_element.enabled = self.enabled
        self.text_element.visible = self.visible
        self.text_element.update(dt)

        # Reset hover state if button is disabled or invisible
        if not self.enabled or not self.visible:
            self._hovered = False
            self._pressed = False
            return

        # Update hover state based on last known mouse position
        bounds = self.get_bounds()
        self._hovered = bounds.collidepoint(self._last_mouse_pos)

        # If mouse is not hovering, button can't be pressed
        if not self._hovered:
            self._pressed = False

    def get_bounds(self, parent_bounds: Optional[pygame.Rect] = None) -> pygame.Rect:
        """Calculate the button's screen-space bounds.

        Args:
            parent_bounds: Parent element's bounds (for percentage calculations)

        Returns:
            Button's bounds in screen coordinates
        """
        bounds = super().get_bounds(parent_bounds)
        return pygame.Rect(
            bounds.x,
            bounds.y,
            bounds.width,
            bounds.height,
        )
