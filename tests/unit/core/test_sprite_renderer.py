"""Tests for the sprite renderer system."""
import os

import pygame
import pytest

from src.core.sprite import Sprite, SpriteConfig, SpriteFrame, SpriteSheet
from src.core.sprite_renderer import SpriteRenderer


def create_test_image(
    width: int, height: int, color: tuple[int, int, int], path: str
) -> None:
    """Create a test image file."""
    surface = pygame.Surface((width, height))
    surface.fill(color)
    pygame.image.save(surface, path)


def create_test_sprite(
    z_index: int = 0, color: tuple[int, int, int] = (255, 0, 0)
) -> tuple[Sprite, str]:
    """Create a test sprite with the given z-index and color."""
    # Create test image
    path = f"test_sprite_{z_index}_{color[0]}_{color[1]}_{color[2]}.png"
    create_test_image(32, 32, color, path)

    # Create sprite
    sprite_sheet = SpriteSheet(path)
    sprite_sheet.add_frame(SpriteFrame(0, 0, 32, 32))
    config = SpriteConfig(z_index=z_index)
    sprite = Sprite(sprite_sheet, config)

    return sprite, path


def test_sprite_renderer_initialization() -> None:
    """Test sprite renderer initialization."""
    renderer = SpriteRenderer()
    assert len(renderer.sprites) == 0


def test_add_sprite() -> None:
    """Test adding sprites to the renderer."""
    renderer = SpriteRenderer()
    paths = []

    try:
        # Add sprite with default z-index (0)
        sprite1, path1 = create_test_sprite()
        paths.append(path1)
        renderer.add_sprite(sprite1)
        assert 0 in renderer.sprites
        assert len(renderer.sprites[0]) == 1
        assert renderer.sprites[0][0] == sprite1

        # Add another sprite with same z-index
        sprite2, path2 = create_test_sprite(color=(0, 255, 0))
        paths.append(path2)
        renderer.add_sprite(sprite2)
        assert len(renderer.sprites[0]) == 2
        assert renderer.sprites[0][1] == sprite2

        # Add sprite with different z-index
        sprite3, path3 = create_test_sprite(z_index=1, color=(0, 0, 255))
        paths.append(path3)
        renderer.add_sprite(sprite3)
        assert 1 in renderer.sprites
        assert len(renderer.sprites[1]) == 1
        assert renderer.sprites[1][0] == sprite3
    finally:
        # Clean up test files
        for path in paths:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass


def test_remove_sprite() -> None:
    """Test removing sprites from the renderer."""
    renderer = SpriteRenderer()
    paths = []

    try:
        # Add and remove sprite
        sprite1, path1 = create_test_sprite()
        paths.append(path1)
        renderer.add_sprite(sprite1)
        renderer.remove_sprite(sprite1)
        assert 0 not in renderer.sprites

        # Add multiple sprites and remove one
        sprite2, path2 = create_test_sprite(color=(0, 255, 0))
        paths.append(path2)
        sprite3, path3 = create_test_sprite(color=(0, 0, 255))
        paths.append(path3)
        renderer.add_sprite(sprite2)
        renderer.add_sprite(sprite3)
        renderer.remove_sprite(sprite2)
        assert len(renderer.sprites[0]) == 1
        assert renderer.sprites[0][0] == sprite3

        # Try to remove non-existent sprite
        sprite4, path4 = create_test_sprite(z_index=1)
        paths.append(path4)
        renderer.remove_sprite(sprite4)  # Should not raise error

        # Remove last sprite at z-index
        renderer.remove_sprite(sprite3)
        assert 0 not in renderer.sprites
    finally:
        # Clean up test files
        for path in paths:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass


def test_clear_sprites() -> None:
    """Test clearing all sprites."""
    renderer = SpriteRenderer()
    paths = []

    try:
        # Add multiple sprites
        sprite1, path1 = create_test_sprite()
        paths.append(path1)
        sprite2, path2 = create_test_sprite(z_index=1, color=(0, 255, 0))
        paths.append(path2)
        sprite3, path3 = create_test_sprite(z_index=2, color=(0, 0, 255))
        paths.append(path3)

        renderer.add_sprite(sprite1)
        renderer.add_sprite(sprite2)
        renderer.add_sprite(sprite3)

        assert len(renderer.sprites) == 3

        # Clear all sprites
        renderer.clear()
        assert len(renderer.sprites) == 0
    finally:
        # Clean up test files
        for path in paths:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass


def test_render_z_order() -> None:
    """Test rendering sprites in correct z-order."""
    renderer = SpriteRenderer()
    surface = pygame.Surface((64, 64))
    paths = []

    try:
        # Create sprites with different z-indices and colors
        sprite1, path1 = create_test_sprite(z_index=2, color=(255, 0, 0))  # Red, top
        paths.append(path1)
        sprite2, path2 = create_test_sprite(
            z_index=0, color=(0, 255, 0)
        )  # Green, bottom
        paths.append(path2)
        sprite3, path3 = create_test_sprite(
            z_index=1, color=(0, 0, 255)
        )  # Blue, middle
        paths.append(path3)

        # Position sprites to overlap
        sprite1.config.x = 16
        sprite1.config.y = 16
        sprite2.config.x = 0
        sprite2.config.y = 0
        sprite3.config.x = 8
        sprite3.config.y = 8

        # Add sprites in random order
        renderer.add_sprite(sprite1)
        renderer.add_sprite(sprite2)
        renderer.add_sprite(sprite3)

        # Render sprites
        surface.fill((0, 0, 0))  # Black background
        renderer.render(surface)

        # Check pixel colors at key points
        # Bottom sprite (green) should be visible at (0,0)
        assert surface.get_at((0, 0))[:3] == (0, 255, 0)

        # Middle sprite (blue) should be visible at (8,8)
        assert surface.get_at((8, 8))[:3] == (0, 0, 255)

        # Top sprite (red) should be visible at (16,16)
        assert surface.get_at((16, 16))[:3] == (255, 0, 0)
    finally:
        # Clean up test files
        for path in paths:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass


def test_render_empty() -> None:
    """Test rendering with no sprites."""
    renderer = SpriteRenderer()
    surface = pygame.Surface((64, 64))
    surface.fill((0, 0, 0))  # Black background

    # Should not modify the surface
    renderer.render(surface)
    assert surface.get_at((0, 0)) == (0, 0, 0, 255)


def test_render_sprite_transformations() -> None:
    """Test rendering sprites with various transformations."""
    renderer = SpriteRenderer()
    surface = pygame.Surface((128, 128))
    paths = []

    try:
        # Create a sprite with various transformations
        sprite, path = create_test_sprite(color=(255, 0, 0))  # Red sprite
        paths.append(path)

        # Test different transformations
        transformations = [
            SpriteConfig(x=32, y=32),  # Position
            SpriteConfig(scale_x=2.0, scale_y=2.0),  # Scale up
            SpriteConfig(scale_x=0.5, scale_y=0.5),  # Scale down
            SpriteConfig(rotation=90),  # Rotation
            SpriteConfig(flip_x=True),  # Flip X
            SpriteConfig(flip_y=True),  # Flip Y
            SpriteConfig(alpha=128),  # Transparency
        ]

        for config in transformations:
            surface.fill((0, 0, 0))  # Reset surface
            sprite.config = config
            renderer.clear()  # Clear previous sprites
            renderer.add_sprite(sprite)
            renderer.render(surface)

            # Verify that something was drawn (not black)
            # Sample multiple points to ensure the sprite is visible
            points_to_check = [
                (16, 16),  # Center for normal sprite
                (32, 32),  # Center for positioned sprite
                (48, 48),  # For scaled up sprite
                (8, 8),  # For scaled down sprite
            ]

            found_sprite = False
            for x, y in points_to_check:
                try:
                    color = surface.get_at((x, y))
                    if color[:3] != (0, 0, 0):
                        found_sprite = True
                        break
                except IndexError:
                    continue

            assert found_sprite, f"Sprite not found with config: {config}"
    finally:
        # Clean up test files
        for path in paths:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass
