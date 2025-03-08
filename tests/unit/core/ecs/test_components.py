"""Tests for the built-in ECS components."""
from pathlib import Path

import pygame
import pytest

from src.core.ecs import Entity
from src.core.ecs.components import SpriteRenderer, Transform
from src.core.sprite import Sprite, SpriteSheet
from src.core.vector2d import Vector2D


@pytest.fixture
def transform() -> Transform:
    """Create a Transform component for testing."""
    return Transform()


@pytest.fixture
def sprite_sheet(tmp_path: Path) -> SpriteSheet:
    """Create a test sprite sheet."""
    # Create a small test image
    surface = pygame.Surface((32, 32))
    surface.fill((255, 0, 0))  # Red square
    path = tmp_path / "test_sprite.png"
    pygame.image.save(surface, str(path))
    return SpriteSheet(str(path))


def test_transform_initialization(transform: Transform) -> None:
    """Test that Transform component is properly initialized."""
    assert transform.position == Vector2D()
    assert transform.rotation == 0.0
    assert transform.scale == Vector2D(1.0, 1.0)
    assert transform.local_position == Vector2D()
    assert transform.local_rotation == 0.0
    assert transform.local_scale == Vector2D(1.0, 1.0)


def test_transform_translate(transform: Transform) -> None:
    """Test Transform translation."""
    transform.translate(Vector2D(10, 20))
    assert transform.position == Vector2D(10, 20)

    transform.translate(Vector2D(-5, 5))
    assert transform.position == Vector2D(5, 25)


def test_transform_rotate(transform: Transform) -> None:
    """Test Transform rotation."""
    transform.rotate(45)
    assert transform.rotation == 45

    transform.rotate(360)
    assert transform.rotation == 45  # Should wrap around

    transform.rotate(-90)
    assert transform.rotation == 315


def test_transform_scale(transform: Transform) -> None:
    """Test Transform scaling."""
    transform.set_scale(2.0, 3.0)
    assert transform.scale == Vector2D(2.0, 3.0)


def test_transform_hierarchy() -> None:
    """Test Transform hierarchy calculations."""
    parent = Entity("parent")
    child = Entity("child")
    grandchild = Entity("grandchild")

    parent_transform = Transform(position=Vector2D(100, 100))
    child_transform = Transform(position=Vector2D(50, 50))
    grandchild_transform = Transform(position=Vector2D(25, 25))

    parent.add_component(parent_transform)
    child.add_component(child_transform)
    grandchild.add_component(grandchild_transform)

    child.set_parent(parent)
    grandchild.set_parent(child)

    # Test world position
    assert grandchild_transform.get_world_position() == Vector2D(175, 175)

    # Test world rotation
    parent_transform.rotation = 90
    child_transform.rotation = 45
    grandchild_transform.rotation = 45
    assert grandchild_transform.get_world_rotation() == 180

    # Test world scale
    parent_transform.set_scale(2.0, 2.0)
    child_transform.set_scale(2.0, 2.0)
    grandchild_transform.set_scale(2.0, 2.0)
    world_scale = grandchild_transform.get_world_scale()
    assert world_scale == Vector2D(8.0, 8.0)


def test_sprite_renderer(sprite_sheet: SpriteSheet) -> None:
    """Test SpriteRenderer component."""
    entity = Entity()
    transform = Transform()
    entity.add_component(transform)

    sprite = Sprite(sprite_sheet)
    renderer = SpriteRenderer(sprite)

    # Test that renderer requires transform
    entity.add_component(renderer)
    assert renderer._transform == transform

    # Test that renderer fails without transform
    entity2 = Entity()
    renderer2 = SpriteRenderer(sprite)
    with pytest.raises(ValueError):
        entity2.add_component(renderer2)

    # Test render updates config from transform
    surface = pygame.Surface((100, 100))
    transform.position = Vector2D(10, 20)
    transform.rotation = 90
    transform.set_scale(2.0, 3.0)

    renderer.render(surface)
    assert renderer.config.x == 10
    assert renderer.config.y == 20
    assert renderer.config.rotation == 90
    assert renderer.config.scale_x == 2.0
    assert renderer.config.scale_y == 3.0


def test_disabled_components(sprite_sheet: SpriteSheet) -> None:
    """Test that disabled components behave correctly."""
    entity = Entity()
    transform = Transform()
    entity.add_component(transform)

    sprite = Sprite(sprite_sheet)
    renderer = SpriteRenderer(sprite)
    entity.add_component(renderer)

    # Test disabled renderer
    surface = pygame.Surface((100, 100))
    renderer.enabled = False
    transform.position = Vector2D(10, 20)
    renderer.render(surface)
    assert renderer.config.x == 0  # Should not update when disabled
