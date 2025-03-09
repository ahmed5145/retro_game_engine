"""Base class for UI elements."""
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import pygame


@dataclass
class UIRect:
    """Rectangle defining UI element bounds and anchor points.

    Attributes:
        x: X position (0-1 for percentage, >1 for pixels)
        y: Y position (0-1 for percentage, >1 for pixels)
        width: Width (0-1 for percentage, >1 for pixels)
        height: Height (0-1 for percentage, >1 for pixels)
        anchor_x: Horizontal anchor point (0=left, 0.5=center, 1=right)
        anchor_y: Vertical anchor point (0=top, 0.5=center, 1=bottom)
    """

    x: float = 0.0
    y: float = 0.0
    width: float = 100.0
    height: float = 100.0
    anchor_x: float = 0.0
    anchor_y: float = 0.0


class UIElement:
    """Base class for all UI elements.

    UI elements can be positioned using either pixel coordinates or percentages
    of their parent container. They support anchoring, layering, and can contain
    child elements.
    """

    def __init__(self, rect: Optional[UIRect] = None) -> None:
        """Initialize the UI element.

        Args:
            rect: Rectangle defining element bounds and anchors
        """
        self.rect = rect or UIRect()
        self._parent: Optional[UIElement] = None
        self._children: List[UIElement] = []
        self._visible = True
        self._enabled = True
        self._z_index = 0
        self._cached_bounds: Optional[pygame.Rect] = None
        self._screen_rect: Optional[pygame.Rect] = None

    @property
    def parent(self) -> Optional["UIElement"]:
        """Get the parent element."""
        return self._parent

    @parent.setter
    def parent(self, value: Optional["UIElement"]) -> None:
        """Set the parent element.

        Args:
            value: New parent element
        """
        if self._parent:
            self._parent._children.remove(self)
        self._parent = value
        if value:
            value._children.append(self)
        self._cached_bounds = None
        self._screen_rect = None

    @property
    def visible(self) -> bool:
        """Check if the element is visible."""
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        """Set element visibility.

        Args:
            value: Whether element should be visible
        """
        self._visible = value

    @property
    def enabled(self) -> bool:
        """Check if the element is enabled."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set element enabled state.

        Args:
            value: Whether element should be enabled
        """
        self._enabled = value

    @property
    def z_index(self) -> int:
        """Get the element's z-index."""
        return self._z_index

    @z_index.setter
    def z_index(self, value: int) -> None:
        """Set the element's z-index.

        Args:
            value: New z-index value
        """
        self._z_index = value

    @property
    def screen_rect(self) -> pygame.Rect:
        """Get the screen-space rectangle.

        Returns:
            Rectangle in screen coordinates
        """
        if self._screen_rect is None:
            # Calculate screen position
            x = self.rect.x
            y = self.rect.y
            width = self.rect.width
            height = self.rect.height

            # Convert percentages to pixels
            if self.parent:
                parent_rect = self.parent.screen_rect
                if isinstance(x, float) and 0.0 <= x <= 1.0:
                    x = parent_rect.width * x
                if isinstance(y, float) and 0.0 <= y <= 1.0:
                    y = parent_rect.height * y
                if isinstance(width, float) and 0.0 <= width <= 1.0:
                    width = parent_rect.width * width
                if isinstance(height, float) and 0.0 <= height <= 1.0:
                    height = parent_rect.height * height

            # Apply anchor
            x -= width * self.rect.anchor_x
            y -= height * self.rect.anchor_y

            # Add parent offset
            if self.parent:
                parent_rect = self.parent.screen_rect
                x += parent_rect.x
                y += parent_rect.y

            self._screen_rect = pygame.Rect(int(x), int(y), int(width), int(height))

        return self._screen_rect

    def add_child(self, child: "UIElement") -> None:
        """Add a child element.

        Args:
            child: Element to add as child
        """
        child.parent = self

    def remove_child(self, child: "UIElement") -> None:
        """Remove a child element.

        Args:
            child: Element to remove
        """
        if child in self._children:
            child.parent = None

    def get_bounds(self, parent_bounds: Optional[pygame.Rect] = None) -> pygame.Rect:
        """Calculate the element's screen-space bounds.

        Args:
            parent_bounds: Parent element's bounds (for percentage calculations)

        Returns:
            Element's bounds in screen coordinates
        """
        if not parent_bounds:
            # Use screen bounds if no parent
            display = pygame.display.get_surface()
            if display:
                parent_bounds = display.get_rect()
            else:
                # Fallback to default size if no display
                parent_bounds = pygame.Rect(0, 0, 800, 600)

        # Return cached bounds if parent hasn't changed
        if self._cached_bounds and parent_bounds == getattr(
            self, "_last_parent_bounds", None
        ):
            return self._cached_bounds

        # Calculate position based on parent bounds
        x = self.rect.x
        y = self.rect.y
        width = self.rect.width
        height = self.rect.height

        # Convert percentages to pixels
        if 0 <= x <= 1:
            x = parent_bounds.width * x
        if 0 <= y <= 1:
            y = parent_bounds.height * y
        if 0 <= width <= 1:
            width = parent_bounds.width * width
        if 0 <= height <= 1:
            height = parent_bounds.height * height

        # Apply anchoring
        x -= width * self.rect.anchor_x
        y -= height * self.rect.anchor_y

        # Add parent offset
        x += parent_bounds.x
        y += parent_bounds.y

        # Cache result
        self._cached_bounds = pygame.Rect(int(x), int(y), int(width), int(height))
        self._last_parent_bounds = parent_bounds

        return self._cached_bounds

    def contains_point(self, point: Tuple[float, float]) -> bool:
        """Check if a point is within the element's bounds.

        Args:
            point: The point to check (x, y).

        Returns:
            bool: True if the point is within the element's bounds, False otherwise.
        """
        if not self.visible:
            return False

        x, y = point
        bounds = self.get_bounds()
        return bool(bounds.collidepoint(int(x), int(y)))

    def update(self, dt: float) -> None:
        """Update the element.

        Args:
            dt: Delta time in seconds
        """
        if not self._enabled:
            return

        # Update children
        for child in self._children:
            child.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        """Render the element.

        Args:
            surface: Surface to render to
        """
        if not self._visible:
            return

        # Get sorted children by z-index
        sorted_children = sorted(self._children, key=lambda c: c.z_index)

        # Render children
        for child in sorted_children:
            child.render(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle a pygame event.

        Args:
            event: The pygame event to handle.

        Returns:
            bool: True if the event was handled, False otherwise.
        """
        if not self.enabled or not self.visible:
            return False

        # Check if event is within bounds for mouse events
        if hasattr(event, "pos") and self.contains_point(event.pos):
            return True

        # Handle children in reverse z-index order
        sorted_children = sorted(self._children, key=lambda c: c.z_index, reverse=True)
        for child in sorted_children:
            if child.handle_event(event):
                return True

        return False
