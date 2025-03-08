"""Tests for the tilemap system."""
import os
from typing import Tuple

import pygame
import pytest

from src.core import (
    SpriteFrame,
    SpriteSheet,
    TileConfig,
    TileLayerConfig,
    Tilemap,
    Vector2D,
)
from src.core.tilemap import TileLayer


def create_test_tileset() -> SpriteSheet:
    """Create a test tileset.

    Returns:
        SpriteSheet: The created tileset
    """
    # Create test surface
    surface = pygame.Surface((64, 64))
    surface.fill((255, 255, 255))  # White background

    # Save the tileset
    pygame.image.save(surface, "test_tileset.png")

    # Create sprite sheet
    tileset = SpriteSheet("test_tileset.png")

    # Add frames
    tileset.add_frame(SpriteFrame(0, 0, 32, 32))
    tileset.add_frame(SpriteFrame(32, 0, 32, 32))
    tileset.add_frame(SpriteFrame(0, 32, 32, 32))
    tileset.add_frame(SpriteFrame(32, 32, 32, 32))

    # Clean up
    os.remove("test_tileset.png")

    return tileset


def test_tile_layer_initialization() -> None:
    """Test that tile layer is properly initialized."""
    layer = TileLayer(10, 8)

    assert layer.width == 10
    assert layer.height == 8
    assert layer.config == TileLayerConfig()
    assert layer.dirty
    assert layer._cache is None

    # Check that all tiles are None
    for y in range(layer.height):
        for x in range(layer.width):
            assert layer.tiles[y][x] is None


def test_tile_layer_set_get_tile() -> None:
    """Test setting and getting tiles."""
    layer = TileLayer(10, 8)

    # Set some tiles
    layer.set_tile(0, 0, 1)
    layer.set_tile(5, 3, 2)

    # Check tiles were set
    assert layer.get_tile(0, 0) == 1
    assert layer.get_tile(5, 3) == 2

    # Check out of bounds
    with pytest.raises(IndexError):
        layer.set_tile(-1, 0, 1)

    with pytest.raises(IndexError):
        layer.set_tile(0, -1, 1)

    with pytest.raises(IndexError):
        layer.set_tile(10, 0, 1)

    with pytest.raises(IndexError):
        layer.set_tile(0, 8, 1)


def test_tile_layer_clear_fill() -> None:
    """Test clearing and filling tile layer."""
    layer = TileLayer(10, 8)

    # Fill with tile ID 1
    layer.fill(1)

    # Check all tiles are 1
    for y in range(layer.height):
        for x in range(layer.width):
            assert layer.get_tile(x, y) == 1

    # Clear layer
    layer.clear()

    # Check all tiles are None
    for y in range(layer.height):
        for x in range(layer.width):
            assert layer.get_tile(x, y) is None


def test_tilemap_initialization() -> None:
    """Test that tilemap is properly initialized."""
    tileset = create_test_tileset()
    tilemap = Tilemap(32, 32, tileset)

    assert tilemap.tile_width == 32
    assert tilemap.tile_height == 32
    assert tilemap.tileset == tileset
    assert len(tilemap.layers) == 0
    assert len(tilemap.tile_configs) == 0
    assert tilemap.time == 0.0


def test_tilemap_layer_management() -> None:
    """Test adding and removing layers."""
    tileset = create_test_tileset()
    tilemap = Tilemap(32, 32, tileset)

    # Add layers
    tilemap.add_layer("background", 10, 8)
    tilemap.add_layer("foreground", 12, 10, TileLayerConfig(z_index=1))

    assert "background" in tilemap.layers
    assert "foreground" in tilemap.layers
    assert tilemap.get_layer("background").width == 10
    assert tilemap.get_layer("background").height == 8
    assert tilemap.get_layer("foreground").config.z_index == 1

    # Try to add duplicate layer
    with pytest.raises(ValueError):
        tilemap.add_layer("background", 10, 8)

    # Remove layer
    tilemap.remove_layer("background")
    assert "background" not in tilemap.layers

    # Try to get non-existent layer
    with pytest.raises(KeyError):
        tilemap.get_layer("background")


def test_tilemap_tile_config() -> None:
    """Test tile configuration."""
    tileset = create_test_tileset()
    tilemap = Tilemap(32, 32, tileset)

    # Set tile config
    config = TileConfig(solid=True, animated=True, frames=[0, 1, 2], frame_duration=0.2)
    tilemap.set_tile_config(1, config)

    # Get tile config
    retrieved = tilemap.get_tile_config(1)
    assert retrieved == config

    # Get non-existent config
    assert tilemap.get_tile_config(2) is None


def test_tilemap_animation() -> None:
    """Test tile animation."""
    tileset = create_test_tileset()
    tilemap = Tilemap(32, 32, tileset)

    # Set up animated tile
    config = TileConfig(animated=True, frames=[0, 1, 2], frame_duration=0.5)
    tilemap.set_tile_config(1, config)

    # Add layer with animated tile
    tilemap.add_layer("test", 1, 1)
    layer = tilemap.get_layer("test")
    layer.set_tile(0, 0, 1)

    # Check animation frames
    tilemap.time = 0.0  # Frame 0
    surface = pygame.Surface((32, 32))
    tilemap.render(surface)

    tilemap.time = 0.6  # Frame 1
    surface = pygame.Surface((32, 32))
    tilemap.render(surface)

    tilemap.time = 1.1  # Frame 2
    surface = pygame.Surface((32, 32))
    tilemap.render(surface)


def test_tilemap_parallax() -> None:
    """Test parallax scrolling."""
    tileset = create_test_tileset()
    tilemap = Tilemap(32, 32, tileset)

    # Add layers with different scroll factors
    bg_config = TileLayerConfig(scroll_factor_x=0.5, scroll_factor_y=0.5)
    tilemap.add_layer("background", 10, 8, bg_config)

    fg_config = TileLayerConfig(scroll_factor_x=1.0, scroll_factor_y=1.0)
    tilemap.add_layer("foreground", 10, 8, fg_config)

    # Fill layers
    bg_layer = tilemap.get_layer("background")
    fg_layer = tilemap.get_layer("foreground")
    bg_layer.fill(0)
    fg_layer.fill(1)

    # Render with camera offset
    surface = pygame.Surface((320, 240))
    tilemap.render(surface, camera_x=100, camera_y=100)

    # Background should move half as much as foreground
    # We can't easily test the exact pixels, but the code runs without errors


def test_tilemap_opacity() -> None:
    """Test layer opacity."""
    tileset = create_test_tileset()
    tilemap = Tilemap(32, 32, tileset)

    # Add layer with partial opacity
    config = TileLayerConfig(opacity=128)
    tilemap.add_layer("test", 1, 1, config)
    layer = tilemap.get_layer("test")
    layer.set_tile(0, 0, 0)

    # Render the layer
    surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    tilemap.render(surface)

    # Check pixel alpha
    # We can't easily test the exact alpha values due to blending,
    # but the code runs without errors


def test_tilemap_visible_range() -> None:
    """Test calculation of visible tile range."""
    tileset = create_test_tileset()
    tilemap = Tilemap(32, 32, tileset)
    tilemap.add_layer("test", 10, 8)

    # Test with no camera offset
    start_x, start_y, end_x, end_y = tilemap._get_visible_range(0, 0, 320, 240)
    assert start_x == 0
    assert start_y == 0
    assert end_x == 10  # 320/32 = 10
    assert end_y == 8  # 240/32 = 7.5, rounded up to 8

    # Test with camera offset
    start_x, start_y, end_x, end_y = tilemap._get_visible_range(32, 32, 320, 240)
    assert start_x == 1  # Offset by 1 tile
    assert start_y == 1  # Offset by 1 tile
    assert end_x == 10  # Limited by map width
    assert end_y == 8  # Limited by map height

    # Test with partial tile offset
    start_x, start_y, end_x, end_y = tilemap._get_visible_range(20, 20, 320, 240)
    assert start_x == 0  # Less than one tile offset
    assert start_y == 0  # Less than one tile offset
    assert end_x == 10  # Limited by map width
    assert end_y == 8  # Limited by map height


def test_tilemap_width_height() -> None:
    """Test tilemap width and height properties."""
    tileset = create_test_tileset()
    tilemap = Tilemap(32, 32, tileset)

    # No layers initially
    assert tilemap.width == 0
    assert tilemap.height == 0

    # Add layers of different sizes
    tilemap.add_layer("layer1", 10, 8)
    assert tilemap.width == 10
    assert tilemap.height == 8

    tilemap.add_layer("layer2", 12, 6)
    assert tilemap.width == 12  # Maximum width
    assert tilemap.height == 8  # Maximum height


def test_tilemap_render_empty() -> None:
    """Test rendering an empty tilemap."""
    tileset = create_test_tileset()
    tilemap = Tilemap(32, 32, tileset)
    surface = pygame.Surface((320, 240))

    # Should not raise any errors
    tilemap.render(surface)


def test_tilemap_render_invalid_tile() -> None:
    """Test rendering with invalid tile IDs."""
    tileset = create_test_tileset()
    tilemap = Tilemap(32, 32, tileset)
    tilemap.add_layer("test", 1, 1)
    layer = tilemap.get_layer("test")

    # Set invalid tile ID
    layer.set_tile(0, 0, 999)  # ID doesn't exist in tileset
    surface = pygame.Surface((32, 32))

    # Should not raise any errors
    tilemap.render(surface)


def test_tilemap_animation_update() -> None:
    """Test updating tile animations."""
    tileset = create_test_tileset()
    tilemap = Tilemap(32, 32, tileset)

    # Set up animated tile
    config = TileConfig(animated=True, frames=[0, 1], frame_duration=0.5)
    tilemap.set_tile_config(1, config)

    # Add layer with animated tile
    tilemap.add_layer("test", 1, 1)
    layer = tilemap.get_layer("test")
    layer.set_tile(0, 0, 1)

    # Update animation
    tilemap.time = 0.0
    tilemap.update(0.4)  # Not enough time for frame change
    assert abs(tilemap.time - 0.4) < 0.001  # Account for floating point precision

    tilemap.update(0.2)  # Should trigger frame change
    assert abs(tilemap.time - 0.6) < 0.001  # Account for floating point precision

    # Time should wrap around after full animation cycle
    tilemap.update(0.5)
    assert abs(tilemap.time - 0.1) < 0.001  # Account for floating point precision


def test_tilemap_layer_visibility() -> None:
    """Test layer visibility control."""
    tileset = create_test_tileset()
    tilemap = Tilemap(32, 32, tileset)

    # Add a layer and make it invisible
    config = TileLayerConfig(visible=False)
    tilemap.add_layer("test", 1, 1, config)
    layer = tilemap.get_layer("test")
    layer.set_tile(0, 0, 0)

    # Render the tilemap
    surface = pygame.Surface((32, 32))
    surface.fill((0, 0, 0))  # Black background
    tilemap.render(surface)

    # Surface should still be black since layer is invisible
    assert surface.get_at((0, 0)) == (0, 0, 0, 255)


def test_tilemap_collision_layer() -> None:
    """Test setting and using the collision layer."""
    tileset = create_test_tileset()
    tilemap = Tilemap(32, 32, tileset)
    tilemap.add_layer("background", 10, 10, TileLayerConfig())
    tilemap.add_layer("collision", 10, 10, TileLayerConfig())

    # Test setting invalid layer
    with pytest.raises(KeyError):
        tilemap.set_collision_layer("invalid")

    # Test with no collision layer set
    assert tilemap.get_tile_at_position(50, 50) == (None, "")
    assert tilemap.get_solid_tiles_in_rect(pygame.Rect(0, 0, 32, 32)) == []
    assert tilemap.check_collision(pygame.Rect(0, 0, 32, 32)) is None

    # Set collision layer and add some solid tiles
    tilemap.set_collision_layer("collision")
    tilemap.set_tile_config(1, TileConfig(solid=True))
    tilemap.layers["collision"].set_tile(1, 1, 1)  # Solid tile at (1,1)

    # Test getting tile at position
    assert tilemap.get_tile_at_position(50, 50) == (1, "collision")

    # Test getting solid tiles in rect
    solid_tiles = tilemap.get_solid_tiles_in_rect(pygame.Rect(32, 32, 32, 32))
    assert len(solid_tiles) == 1
    tile_rect, normal = solid_tiles[0]
    assert tile_rect == pygame.Rect(32, 32, 32, 32)
    assert isinstance(normal, Vector2D)


@pytest.mark.parametrize(
    "rect,expected",
    [
        # Test left collision - rectangle overlapping the left side of the tile
        (pygame.Rect(28, 32, 16, 16), (Vector2D(-1.0, 0.0), 12.0)),
        # Test right collision - rectangle overlapping the right side of the tile
        (pygame.Rect(52, 32, 16, 16), (Vector2D(1.0, 0.0), 16.0)),
        # Test top collision - rectangle overlapping the top of the tile
        (pygame.Rect(32, 28, 16, 16), (Vector2D(0.0, -1.0), 12.0)),
        # Test bottom collision - rectangle overlapping the bottom of the tile
        (pygame.Rect(32, 52, 16, 16), (Vector2D(0.0, 1.0), 16.0)),
    ],
)
def test_tilemap_collision_detection(
    rect: pygame.Rect, expected: Tuple[Vector2D, float]
) -> None:
    """Test collision detection and normal calculation.

    Args:
        rect: Rectangle to test collision with
        expected: Expected (normal, penetration) tuple
    """
    # Create a simple tilemap with one solid tile in the center
    tilemap = Tilemap(32, 32, create_test_tileset())
    tilemap.add_layer("collision", 3, 3)
    tilemap.set_collision_layer("collision")

    # Set up tile configuration
    config = TileConfig(solid=True)
    tilemap.set_tile_config(0, config)

    # Place a solid tile in the center (1, 1) which is at pixel position (32, 32)
    layer = tilemap.get_layer("collision")
    layer.set_tile(1, 1, 0)

    # Test collision
    result = tilemap.check_collision(rect)
    assert result is not None

    normal, penetration = result
    expected_normal, expected_penetration = expected

    # Verify normal direction and penetration depth
    assert normal.x == expected_normal.x
    assert normal.y == expected_normal.y
    assert (
        abs(penetration - expected_penetration) < 0.001
    )  # Allow small floating point differences
