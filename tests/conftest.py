"""Pytest configuration and fixtures."""
from typing import Generator

import pygame
import pytest


@pytest.fixture(autouse=True)
def pygame_init() -> Generator[None, None, None]:
    """Initialize pygame before each test."""
    pygame.init()
    pygame.display.set_mode((800, 600))  # Create a window large enough for UI tests
    yield
    pygame.quit()
