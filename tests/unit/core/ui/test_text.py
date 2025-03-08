"""Tests for the Text UI element."""
import pygame
import pytest

from src.core.ui import Text, TextConfig, UIRect


@pytest.fixture
def text_element() -> Text:
    """Create a test text element."""
    return Text(
        text="Test Text",
        rect=UIRect(x=10, y=20, width=100, height=50),
        config=TextConfig(font_size=16, color=(255, 255, 255)),
    )


def test_text_initialization(text_element: Text) -> None:
    """Test Text initialization."""
    assert text_element.text == "Test Text"
    assert text_element.config.font_size == 16
    assert text_element.config.color == (255, 255, 255)
    assert text_element._animation_progress == len(
        "Test Text"
    )  # No animation by default


def test_text_set_text(text_element: Text) -> None:
    """Test setting text content."""
    text_element.set_text("New Text")
    assert text_element.text == "New Text"
    text_element.update(0.0)
    assert text_element._surface is not None


def test_text_animation(text_element: Text) -> None:
    """Test text animation."""
    text_element.set_text("Test")
    text_element.config.animation_speed = 10  # 10 characters per second
    text_element.update(0.0)

    # Check initial state
    assert text_element._animation_progress == 0

    # Update with time delta
    text_element.update(0.1)  # Should show 1 character
    assert text_element._animation_progress == 1

    # Update until complete
    text_element.update(0.3)  # Should show all characters
    assert text_element._animation_progress == len("Test")


def test_text_shadow() -> None:
    """Test text shadow rendering."""
    # Initialize pygame for surface creation
    pygame.init()
    pygame.display.set_mode((800, 600))

    # Create text with shadow
    config = TextConfig(
        font_size=16,
        color=(255, 255, 255),
        shadow_offset=(2, 2),
        shadow_color=(0, 0, 0),
    )
    text = Text("Shadow Text", config=config)

    # Force surface creation
    surface = pygame.Surface((200, 100), pygame.SRCALPHA)
    text.render(surface)

    # Verify shadow was created
    assert text._surface is not None
    assert text._surface.get_width() > 0
    assert text._surface.get_height() > 0

    pygame.quit()


def test_text_alignment() -> None:
    """Test text alignment options."""
    # Initialize pygame for surface creation
    pygame.init()
    pygame.display.set_mode((800, 600))

    # Test left alignment (default)
    left_text = Text(
        "Left",
        rect=UIRect(x=0, y=0, width=100, height=50),
        config=TextConfig(align="left"),
    )
    surface = pygame.Surface((200, 100), pygame.SRCALPHA)
    left_text.render(surface)
    bounds = left_text.get_bounds()
    assert bounds.x == 0

    # Test center alignment
    center_text = Text(
        "Center",
        rect=UIRect(x=0, y=0, width=100, height=50),
        config=TextConfig(align="center"),
    )
    center_text.render(surface)
    bounds = center_text.get_bounds()
    assert bounds.x == 0  # Base position is still 0
    # Center alignment is handled in render

    # Test right alignment
    right_text = Text(
        "Right",
        rect=UIRect(x=0, y=0, width=100, height=50),
        config=TextConfig(align="right"),
    )
    right_text.render(surface)
    bounds = right_text.get_bounds()
    assert bounds.x == 0  # Base position is still 0
    # Right alignment is handled in render

    pygame.quit()


def test_text_font_loading(text_element: Text) -> None:
    """Test font loading."""
    assert text_element._font is not None
    assert isinstance(text_element._font, pygame.font.Font)
    assert text_element._font.get_height() > 0


def test_text_surface_creation(text_element: Text) -> None:
    """Test surface creation."""
    text_element.set_text("Test Surface")
    text_element.update(0.0)

    assert text_element._surface is not None
    assert isinstance(text_element._surface, pygame.Surface)
    assert text_element._surface.get_width() > 0
    assert text_element._surface.get_height() > 0
