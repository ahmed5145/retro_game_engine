"""Tests for the UIElement class."""
import pygame
import pytest

from src.core.ui import UIElement, UIRect


@pytest.fixture
def ui_element() -> UIElement:
    """Create a test UI element."""
    return UIElement(UIRect(x=10, y=20, width=100, height=50))


@pytest.fixture
def child_element() -> UIElement:
    """Create a test child element."""
    return UIElement(UIRect(x=5, y=5, width=50, height=25))


def test_ui_element_initialization(ui_element: UIElement) -> None:
    """Test UIElement initialization."""
    assert ui_element.rect.x == 10
    assert ui_element.rect.y == 20
    assert ui_element.rect.width == 100
    assert ui_element.rect.height == 50
    assert ui_element.visible
    assert ui_element.enabled
    assert ui_element.z_index == 0
    assert ui_element.parent is None


def test_ui_element_parent_child_relationship(
    ui_element: UIElement, child_element: UIElement
) -> None:
    """Test parent-child relationship management."""
    ui_element.add_child(child_element)
    assert child_element.parent == ui_element
    assert child_element in ui_element._children

    ui_element.remove_child(child_element)
    assert child_element.parent is None
    assert child_element not in ui_element._children


def test_ui_element_visibility(ui_element: UIElement) -> None:
    """Test visibility property."""
    assert ui_element.visible
    ui_element.visible = False
    assert not ui_element.visible


def test_ui_element_enabled(ui_element: UIElement) -> None:
    """Test enabled property."""
    assert ui_element.enabled
    ui_element.enabled = False
    assert not ui_element.enabled


def test_ui_element_z_index(ui_element: UIElement) -> None:
    """Test z-index property."""
    assert ui_element.z_index == 0
    ui_element.z_index = 5
    assert ui_element.z_index == 5


def test_ui_element_bounds_calculation(ui_element: UIElement) -> None:
    """Test bounds calculation."""
    # Initialize pygame for surface creation
    pygame.init()
    pygame.display.set_mode((800, 600))

    bounds = ui_element.get_bounds()
    assert bounds.x == 10
    assert bounds.y == 20
    assert bounds.width == 100
    assert bounds.height == 50

    # Test percentage-based positioning
    percent_element = UIElement(UIRect(x=0.5, y=0.5, width=0.25, height=0.25))
    bounds = percent_element.get_bounds()
    assert bounds.x == 400  # 50% of 800
    assert bounds.y == 300  # 50% of 600
    assert bounds.width == 200  # 25% of 800
    assert bounds.height == 150  # 25% of 600

    pygame.quit()


def test_ui_element_contains_point(ui_element: UIElement) -> None:
    """Test point containment check."""
    # Initialize pygame for surface creation
    pygame.init()
    pygame.display.set_mode((800, 600))

    assert ui_element.contains_point((15, 25))  # Inside
    assert not ui_element.contains_point((5, 5))  # Outside
    assert not ui_element.contains_point((150, 150))  # Outside

    pygame.quit()


def test_ui_element_anchoring(ui_element: UIElement) -> None:
    """Test anchor point positioning."""
    # Initialize pygame for surface creation
    pygame.init()
    pygame.display.set_mode((800, 600))

    # Test center anchoring
    centered = UIElement(
        UIRect(x=400, y=300, width=100, height=50, anchor_x=0.5, anchor_y=0.5)
    )
    bounds = centered.get_bounds()
    assert bounds.x == 350  # 400 - (100 * 0.5)
    assert bounds.y == 275  # 300 - (50 * 0.5)

    # Test bottom-right anchoring
    bottom_right = UIElement(
        UIRect(x=800, y=600, width=100, height=50, anchor_x=1.0, anchor_y=1.0)
    )
    bounds = bottom_right.get_bounds()
    assert bounds.x == 700  # 800 - 100
    assert bounds.y == 550  # 600 - 50

    pygame.quit()


def test_ui_element_event_handling(
    ui_element: UIElement, child_element: UIElement
) -> None:
    """Test event handling and propagation."""
    # Initialize pygame for event handling
    pygame.init()
    pygame.display.set_mode((800, 600))

    # Add child element
    ui_element.add_child(child_element)

    # Test disabled state
    ui_element.enabled = False
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (15, 25), "button": 1})
    assert not ui_element.handle_event(event)

    # Test enabled state
    ui_element.enabled = True
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (15, 25), "button": 1})
    assert ui_element.handle_event(event)

    pygame.quit()


def test_ui_element_update(ui_element: UIElement, child_element: UIElement) -> None:
    """Test update propagation."""
    ui_element.add_child(child_element)

    # Test disabled state
    ui_element.enabled = False
    ui_element.update(0.016)  # Simulate one frame at 60 FPS

    # Test enabled state
    ui_element.enabled = True
    ui_element.update(0.016)  # Should update self and child
