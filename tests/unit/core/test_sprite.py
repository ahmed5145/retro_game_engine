"""Tests for the sprite system."""
import os
from typing import Tuple

import pygame
import pytest

from src.core.sprite import Sprite, SpriteConfig, SpriteFrame, SpriteSheet


def create_test_image(
    width: int, height: int, color: Tuple[int, int, int], path: str
) -> None:
    """Create a test image file."""
    surface = pygame.Surface((width, height))
    surface.fill(color)
    pygame.image.save(surface, path)


def test_sprite_frame() -> None:
    """Test sprite frame initialization and properties."""
    frame = SpriteFrame(10, 20, 32, 48)
    assert frame.x == 10
    assert frame.y == 20
    assert frame.width == 32
    assert frame.height == 48


def test_sprite_config() -> None:
    """Test sprite configuration."""
    # Test default values
    config = SpriteConfig()
    assert config.x == 0.0
    assert config.y == 0.0
    assert config.scale_x == 1.0
    assert config.scale_y == 1.0
    assert config.rotation == 0
    assert not config.flip_x
    assert not config.flip_y
    assert config.alpha == 255
    assert config.z_index == 0

    # Test custom values
    config = SpriteConfig(
        x=100.0,
        y=200.0,
        scale_x=2.0,
        scale_y=0.5,
        rotation=90,
        flip_x=True,
        flip_y=True,
        alpha=128,
        z_index=10,
    )
    assert config.x == 100.0
    assert config.y == 200.0
    assert config.scale_x == 2.0
    assert config.scale_y == 0.5
    assert config.rotation == 90
    assert config.flip_x
    assert config.flip_y
    assert config.alpha == 128
    assert config.z_index == 10


def test_sprite_sheet_initialization() -> None:
    """Test sprite sheet initialization."""
    # Create test image
    create_test_image(64, 64, (255, 0, 0), "test.png")

    try:
        sprite_sheet = SpriteSheet("test.png")
        assert sprite_sheet.texture is not None
        assert len(sprite_sheet.frames) == 0

        # Test loading non-existent file
        with pytest.raises(FileNotFoundError):
            SpriteSheet("nonexistent.png")
    finally:
        os.remove("test.png")


def test_sprite_sheet_add_frame() -> None:
    """Test adding frames to a sprite sheet."""
    create_test_image(64, 64, (255, 0, 0), "test.png")

    try:
        sprite_sheet = SpriteSheet("test.png")

        # Add some frames
        frame1 = SpriteFrame(0, 0, 32, 32)
        frame2 = SpriteFrame(32, 0, 32, 32)

        index1 = sprite_sheet.add_frame(frame1)
        index2 = sprite_sheet.add_frame(frame2)

        assert len(sprite_sheet.frames) == 2
        assert sprite_sheet.frames[index1] == frame1
        assert sprite_sheet.frames[index2] == frame2

        # Test invalid frame coordinates
        invalid_frames = [
            SpriteFrame(-1, 0, 32, 32),  # Negative x
            SpriteFrame(0, -1, 32, 32),  # Negative y
            SpriteFrame(0, 0, 0, 32),  # Zero width
            SpriteFrame(0, 0, 32, 0),  # Zero height
            SpriteFrame(40, 0, 32, 32),  # Width exceeds texture
            SpriteFrame(0, 40, 32, 32),  # Height exceeds texture
        ]

        for frame in invalid_frames:
            with pytest.raises(ValueError):
                sprite_sheet.add_frame(frame)
    finally:
        os.remove("test.png")


def test_sprite_sheet_add_frames_grid() -> None:
    """Test adding frames in a grid pattern."""
    create_test_image(64, 64, (255, 0, 0), "test.png")

    try:
        sprite_sheet = SpriteSheet("test.png")

        # Add 2x2 grid of frames
        sprite_sheet.add_frames_grid(frame_width=32, frame_height=32)

        assert len(sprite_sheet.frames) == 4

        # Check frame positions
        assert (
            sprite_sheet.frames[0].x == 0 and sprite_sheet.frames[0].y == 0
        )  # Top-left
        assert (
            sprite_sheet.frames[1].x == 32 and sprite_sheet.frames[1].y == 0
        )  # Top-right
        assert (
            sprite_sheet.frames[2].x == 0 and sprite_sheet.frames[2].y == 32
        )  # Bottom-left
        assert (
            sprite_sheet.frames[3].x == 32 and sprite_sheet.frames[3].y == 32
        )  # Bottom-right

        # Test with margin and spacing
        sprite_sheet.frames.clear()
        sprite_sheet.add_frames_grid(
            frame_width=16, frame_height=16, margin=8, spacing=8
        )

        # Should fit 2x2 grid with margins and spacing
        assert len(sprite_sheet.frames) == 4

        # Test invalid parameters
        invalid_params = [
            (0, 32),  # Invalid width
            (32, 0),  # Invalid height
            (32, 32, -1),  # Invalid margin
            (32, 32, 0, -1),  # Invalid spacing
        ]

        for params in invalid_params:
            with pytest.raises(ValueError):
                sprite_sheet.add_frames_grid(*params)
    finally:
        os.remove("test.png")


def test_sprite_sheet_invalid_frames() -> None:
    """Test adding invalid frames."""
    create_test_image(64, 64, (255, 0, 0), "test.png")

    try:
        sprite_sheet = SpriteSheet("test.png")

        # Try to add frame outside texture bounds
        invalid_frame = SpriteFrame(32, 32, 64, 64)
        with pytest.raises(ValueError):
            sprite_sheet.add_frame(invalid_frame)

        # Try to add grid frames with margin that would make first frame invalid
        with pytest.raises(ValueError):
            sprite_sheet.add_frames_grid(
                frame_width=32,
                frame_height=32,
                margin=64,  # This would push the first frame outside the texture
            )
    finally:
        os.remove("test.png")


def test_sprite_initialization() -> None:
    """Test sprite initialization."""
    create_test_image(64, 64, (255, 0, 0), "test.png")

    try:
        sprite_sheet = SpriteSheet("test.png")
        sprite_sheet.add_frame(SpriteFrame(0, 0, 32, 32))

        # Test with default config
        sprite = Sprite(sprite_sheet)
        assert sprite.sprite_sheet == sprite_sheet
        assert isinstance(sprite.config, SpriteConfig)
        assert sprite.current_frame == 0

        # Test with custom config
        config = SpriteConfig(x=100.0, y=100.0)
        sprite = Sprite(sprite_sheet, config)
        assert sprite.config == config
    finally:
        os.remove("test.png")


def test_sprite_set_frame() -> None:
    """Test setting sprite frames."""
    create_test_image(64, 64, (255, 0, 0), "test.png")

    try:
        sprite_sheet = SpriteSheet("test.png")
        sprite_sheet.add_frames_grid(32, 32)
        sprite = Sprite(sprite_sheet)

        # Test valid frame indices
        sprite.set_frame(0)
        assert sprite.current_frame == 0

        sprite.set_frame(3)
        assert sprite.current_frame == 3

        # Test invalid frame index
        with pytest.raises(IndexError):
            sprite.set_frame(4)
        with pytest.raises(IndexError):
            sprite.set_frame(-1)
    finally:
        os.remove("test.png")


def test_sprite_draw() -> None:
    """Test sprite drawing with various transformations."""
    create_test_image(32, 32, (255, 0, 0), "test.png")

    try:
        sprite_sheet = SpriteSheet("test.png")
        sprite_sheet.add_frame(SpriteFrame(0, 0, 32, 32))
        surface = pygame.Surface((64, 64))

        # Test basic drawing
        sprite = Sprite(sprite_sheet)
        sprite.draw(surface)

        # Test with all transformations
        configs = [
            SpriteConfig(x=16.0, y=16.0),  # Position
            SpriteConfig(scale_x=0.5, scale_y=0.5),  # Scale
            SpriteConfig(scale_x=-1.0, scale_y=1.0),  # Negative scale
            SpriteConfig(rotation=90),  # Rotation
            SpriteConfig(rotation=180),  # Rotation
            SpriteConfig(rotation=270),  # Rotation
            SpriteConfig(flip_x=True),  # Flip X
            SpriteConfig(flip_y=True),  # Flip Y
            SpriteConfig(flip_x=True, flip_y=True),  # Flip both
            SpriteConfig(alpha=128),  # Alpha
            # Combined transformations
            SpriteConfig(
                x=16.0,
                y=16.0,
                scale_x=0.5,
                scale_y=0.5,
                rotation=90,
                flip_x=True,
                alpha=128,
            ),
        ]

        for config in configs:
            sprite = Sprite(sprite_sheet, config)
            sprite.draw(surface)  # Should not raise any errors

        # Test drawing with no frames
        empty_sprite_sheet = SpriteSheet("test.png")
        sprite = Sprite(empty_sprite_sheet)
        sprite.draw(surface)  # Should not draw anything or raise errors
    finally:
        os.remove("test.png")
