"""Pytest configuration and fixtures."""
from typing import Generator

import pygame
import pytest


@pytest.fixture(autouse=True)
def pygame_init() -> Generator[None, None, None]:
    """Initialize pygame before each test."""
    pygame.init()
    pygame.display.set_mode((100, 100))  # Create a small display surface
    yield
    pygame.quit()
