"""Tests for the Button UI element."""
import pygame
import pytest

from src.core.ui import Button, ButtonStyle, TextConfig, UIRect


@pytest.fixture
def button() -> Button:
    """Create a button for testing."""
    rect = UIRect(x=100, y=100, width=100, height=50)
    style = ButtonStyle(
        background_color=(100, 100, 100),
        hover_color=(150, 150, 150),
        pressed_color=(80, 80, 80),
    )
    return Button("Test Button", rect, style)


def test_button_initialization(button: Button) -> None:
    """Test button initialization."""
    assert button.text_element.text == "Test Button"
    assert button.style.background_color == (100, 100, 100)
    assert button.style.hover_color == (150, 150, 150)
    assert not button._hovered
    assert not button._pressed


def test_button_set_text(button: Button) -> None:
    """Test setting button text."""
    button.set_text("New Text")
    assert button.text_element.text == "New Text"
    assert button._needs_update


def test_button_hover_state(button: Button) -> None:
    """Test button hover state."""
    # Test mouse enter
    event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (150, 125)})
    button.handle_event(event)
    assert button._hovered

    # Test mouse leave
    event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (0, 0)})
    button.handle_event(event)
    assert not button._hovered


def test_button_click(button: Button) -> None:
    """Test button click handling."""
    clicked = False

    def on_click() -> None:
        nonlocal clicked
        clicked = True

    button.on_click = on_click

    # Test mouse down
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (150, 125), "button": 1})
    button.handle_event(event)
    assert button._pressed

    # Test mouse up (click)
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": (150, 125), "button": 1})
    button.handle_event(event)
    assert not button._pressed
    assert clicked


def test_button_click_outside(button: Button) -> None:
    """Test button click handling when released outside button."""
    clicked = False

    def on_click() -> None:
        nonlocal clicked
        clicked = True

    button.on_click = on_click

    # Press inside
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (150, 125), "button": 1})
    button.handle_event(event)
    assert button._pressed

    # Release outside
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": (0, 0), "button": 1})
    button.handle_event(event)
    assert not button._pressed
    assert not clicked


def test_button_disabled_state(button: Button) -> None:
    """Test button behavior when disabled."""
    clicked = False

    def on_click() -> None:
        nonlocal clicked
        clicked = True

    button.on_click = on_click

    # Disable button
    button.enabled = False

    # Try to interact
    event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (150, 125)})
    button.handle_event(event)
    assert not button._hovered

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (150, 125), "button": 1})
    button.handle_event(event)
    assert not button._pressed

    event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": (150, 125), "button": 1})
    button.handle_event(event)
    assert not clicked


def test_button_style_customization() -> None:
    """Test button style customization."""
    rect = UIRect(x=100, y=100, width=100, height=50)
    style = ButtonStyle(
        background_color=(200, 100, 100),
        hover_color=(220, 120, 120),
        pressed_color=(180, 80, 80),
        border_color=(100, 50, 50),
        border_width=3,
        corner_radius=10,
    )
    button = Button("Styled Button", rect, style)

    assert button.style.background_color == (200, 100, 100)
    assert button.style.hover_color == (220, 120, 120)
    assert button.style.pressed_color == (180, 80, 80)
    assert button.style.border_color == (100, 50, 50)
    assert button.style.border_width == 3
    assert button.style.corner_radius == 10


def test_button_text_update(button: Button) -> None:
    """Test updating button text."""
    # Initial state
    assert button.text_element.text == "Test Button"

    # Update text
    button.set_text("Updated Text")
    assert button.text_element.text == "Updated Text"
    assert button._needs_update

    # Render to test surface update
    surface = pygame.Surface((300, 200))
    button.render(surface)
    assert not button._needs_update
