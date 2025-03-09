"""Tests for the Button UI element."""
from typing import Generator

import pygame
import pytest

from src.core.ui import Button, ButtonStyle, TextConfig, UIRect


@pytest.fixture(autouse=True)
def setup_pygame() -> Generator[None, None, None]:
    """Set up pygame for testing."""
    pygame.init()
    pygame.display.set_mode((300, 250))
    yield
    pygame.quit()


@pytest.fixture
def button() -> Button:
    """Create a button for testing."""
    rect = UIRect(x=100, y=100, width=100, height=50)
    style = ButtonStyle()
    return Button("Test Button", rect, style)


def test_button_initialization(button: Button) -> None:
    """Test button initialization."""
    assert button.text_element.text == "Test Button"
    assert button.rect.x == 100
    assert button.rect.y == 100
    assert button.rect.width == 100
    assert button.rect.height == 50
    assert not button._hovered
    assert not button._pressed


def test_button_set_text(button: Button) -> None:
    """Test setting button text."""
    button.set_text("New Text")
    assert button.text_element.text == "New Text"


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
    assert not clicked

    # Test mouse up (click completion)
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": (150, 125), "button": 1})
    button.handle_event(event)
    assert not button._pressed
    assert clicked


def test_button_click_outside(button: Button) -> None:
    """Test clicking outside button bounds."""
    clicked = False

    def on_click() -> None:
        nonlocal clicked
        clicked = True

    button.on_click = on_click

    # Test mouse down outside
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0), "button": 1})
    button.handle_event(event)
    assert not button._pressed
    assert not clicked

    # Test mouse up outside
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": (0, 0), "button": 1})
    button.handle_event(event)
    assert not clicked


def test_button_disabled_state(button: Button) -> None:
    """Test button behavior when disabled."""
    clicked = False

    def on_click() -> None:
        nonlocal clicked
        clicked = True

    button.on_click = on_click
    button.enabled = False

    # Test click on disabled button
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (150, 125), "button": 1})
    button.handle_event(event)
    assert not button._pressed
    assert not clicked

    event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": (150, 125), "button": 1})
    button.handle_event(event)
    assert not clicked


def test_button_style_customization() -> None:
    """Test button style customization."""
    style = ButtonStyle(
        background_color=(200, 200, 200),
        hover_color=(220, 220, 220),
        pressed_color=(180, 180, 180),
        border_color=(100, 100, 100),
        border_width=3,
        corner_radius=10,
        padding=(15, 8, 15, 8),
    )

    rect = UIRect(x=100, y=100, width=100, height=50)
    button = Button("Custom Style", rect, style)

    assert button.style == style


def test_button_text_update(button: Button) -> None:
    """Test text element updates with button state."""
    # Initial state
    assert button.text_element.enabled == button.enabled
    assert button.text_element.visible == button.visible

    # Test disabled state
    button.enabled = False
    assert not button.text_element.enabled

    # Test visibility
    button.visible = False
    assert not button.text_element.visible


def test_button_rendering_square() -> None:
    """Test button rendering with square corners."""
    style = ButtonStyle(corner_radius=0)
    rect = UIRect(x=100, y=100, width=100, height=50)
    button = Button("Square Button", rect, style)

    surface = pygame.Surface((300, 250))
    button.render(surface)


def test_button_rendering_rounded() -> None:
    """Test button rendering with rounded corners."""
    style = ButtonStyle(corner_radius=10)
    rect = UIRect(x=100, y=100, width=100, height=50)
    button = Button("Rounded Button", rect, style)

    surface = pygame.Surface((300, 250))
    button.render(surface)


def test_button_visibility() -> None:
    """Test button visibility state."""
    rect = UIRect(x=100, y=100, width=100, height=50)
    style = ButtonStyle()
    button = Button("Test Button", rect, style)

    # Test initial visibility
    assert button.visible
    assert button.text_element.visible

    # Test hiding button
    button.visible = False
    assert not button.visible
    assert not button.text_element.visible

    # Test showing button
    button.visible = True
    assert button.visible
    assert button.text_element.visible


def test_button_update_mouse_states() -> None:
    """Test button mouse state updates."""
    rect = UIRect(x=100, y=100, width=100, height=50)
    style = ButtonStyle()
    button = Button("Test Button", rect, style)

    clicked = False

    def on_click() -> None:
        nonlocal clicked
        clicked = True

    button.on_click = on_click

    # Test hover state
    button.update(0.016)
    assert not button._hovered

    # Move mouse over button
    pygame.mouse.set_pos((150, 125))
    button.update(0.016)
    assert button._hovered
    assert not button._pressed

    # Test press state
    pygame.mouse.set_pressed((True, False, False))
    button.update(0.016)
    assert button._pressed

    # Test release state
    pygame.mouse.set_pressed((False, False, False))
    button.update(0.016)
    assert not button._pressed
    assert clicked


def test_button_text_alignment() -> None:
    """Test button text alignment."""
    style = ButtonStyle(padding=(10, 5, 10, 5))
    rect = UIRect(x=100, y=100, width=200, height=50)
    button = Button("Aligned Text", rect, style)

    # Get bounds
    button_bounds = button.get_bounds()
    text_bounds = button.text_element.get_bounds()

    # Verify text is within button bounds
    assert (
        text_bounds.width <= button_bounds.width - style.padding[0] - style.padding[2]
    )
    assert (
        text_bounds.height <= button_bounds.height - style.padding[1] - style.padding[3]
    )
