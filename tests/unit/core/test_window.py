"""Tests for the window system."""
from typing import Any, Generator, Optional, Tuple

import pygame
import pytest

from src.core.window import Window, WindowConfig


@pytest.fixture(autouse=True)
def setup_pygame_for_tests(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[None, None, None]:
    """Set up pygame for testing in headless mode."""

    # Create a mock surface
    class MockSurface:
        def __init__(self, size: Tuple[int, int]) -> None:
            self._size = size
            self._fill_color: Optional[Tuple[int, int, int]] = None

        def fill(self, color: Tuple[int, int, int]) -> None:
            self._fill_color = color

        def get_at(self, pos: Tuple[int, int]) -> Tuple[int, int, int, int]:
            return (*self._fill_color, 255) if self._fill_color else (0, 0, 0, 255)

        def blit(self, *args: Any, **kwargs: Any) -> None:
            pass

        def get_width(self) -> int:
            return self._size[0]

        def get_height(self) -> int:
            return self._size[1]

    # Create mock transform module
    class MockTransform:
        @staticmethod
        def scale(
            surface: Any, size: Tuple[int, int], dest_surface: Any = None
        ) -> None:
            pass

    # Create mock display module
    class MockDisplay:
        @staticmethod
        def set_mode(
            size: Tuple[int, int],
            flags: int = 0,
            depth: int = 0,
            display: int = 0,
            vsync: int = 0,
        ) -> MockSurface:
            return MockSurface(size)

        @staticmethod
        def set_caption(title: str) -> None:
            pass

        @staticmethod
        def flip() -> None:
            pass

        @staticmethod
        def get_surface() -> MockSurface:
            return MockSurface((320, 240))

    # Patch pygame modules with our mocks
    monkeypatch.setattr(pygame, "display", MockDisplay)
    monkeypatch.setattr(pygame, "transform", MockTransform)

    # Initialize pygame for tests
    if not pygame.get_init():
        pygame.init()

    yield

    # Clean up pygame after tests
    pygame.quit()


def test_window_initialization() -> None:
    """Test that window is properly initialized with default settings."""
    config = WindowConfig(
        title="Test Window", width=320, height=240, scale=2, vsync=True
    )
    window = Window(config)
    assert window.width == 320
    assert window.height == 240
    assert window.scale == 2
    assert window.title == "Test Window"
    assert window.vsync is True


def test_window_scaling() -> None:
    """Test that window scaling works correctly."""
    config = WindowConfig(
        title="Test Window", width=320, height=240, scale=2, vsync=True
    )
    window = Window(config)
    assert window.display_surface.get_width() == 640
    assert window.display_surface.get_height() == 480


def test_invalid_dimensions() -> None:
    """Test that invalid dimensions raise ValueError."""
    with pytest.raises(ValueError):
        Window(WindowConfig(title="Test", width=0, height=240))
    with pytest.raises(ValueError):
        Window(WindowConfig(title="Test", width=320, height=0))
    with pytest.raises(ValueError):
        Window(WindowConfig(title="Test", width=-320, height=240))
    with pytest.raises(ValueError):
        Window(WindowConfig(title="Test", width=320, height=-240))


def test_invalid_scale() -> None:
    """Test that invalid scale raises ValueError."""
    with pytest.raises(ValueError):
        Window(WindowConfig(title="Test", width=320, height=240, scale=0))
    with pytest.raises(ValueError):
        Window(WindowConfig(title="Test", width=320, height=240, scale=-1))


def test_window_clear() -> None:
    """Test that window clear fills with black by default."""
    config = WindowConfig(
        title="Test Window", width=320, height=240, scale=1, vsync=True
    )
    window = Window(config)
    window.clear()
    assert window.surface.get_at((0, 0)) == (0, 0, 0, 255)


def test_window_clear_with_color() -> None:
    """Test that window clear works with custom color."""
    config = WindowConfig(
        title="Test Window", width=320, height=240, scale=1, vsync=True
    )
    window = Window(config)
    window.clear((255, 0, 0))  # Red
    assert window.surface.get_at((0, 0)) == (255, 0, 0, 255)


def test_set_title() -> None:
    """Test that window title can be changed."""
    config = WindowConfig(
        title="Initial Title", width=320, height=240, scale=1, vsync=True
    )
    window = Window(config)
    window.title = "New Title"
    assert window.title == "New Title"


def test_fullscreen_initialization() -> None:
    """Test that window can be initialized in fullscreen mode."""
    config = WindowConfig(
        title="Fullscreen Window",
        width=320,
        height=240,
        scale=1,
        vsync=True,
        fullscreen=True,
    )
    Window(config)
    # Just verify it initializes without error


def test_window_present() -> None:
    """Test that present method works correctly."""
    config = WindowConfig(
        title="Test Window", width=320, height=240, scale=2, vsync=True
    )
    window = Window(config)
    window.clear((255, 0, 0))  # Red
    window.present()  # Should not raise any errors


def test_cleanup() -> None:
    """Test that window cleanup works correctly."""
    config = WindowConfig(
        title="Test Window", width=320, height=240, scale=1, vsync=True
    )
    Window(config).__del__()  # Call destructor directly
