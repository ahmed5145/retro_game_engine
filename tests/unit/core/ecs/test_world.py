"""Tests for the World class."""
import pytest

from src.core.ecs import Component, Entity, World


class TestComponent(Component):
    """Test component for testing."""

    def __init__(self, value: int = 0):
        super().__init__()
        self.value = value


def test_world_initialization() -> None:
    """Test that world is properly initialized."""
    world = World()
    assert len(world._entities) == 0
    assert len(world._systems) == 0
    assert len(world._component_cache) == 0
    assert len(world._pending_removal) == 0


def test_create_entity() -> None:
    """Test creating entities in the world."""
    world = World()
    entity = world.create_entity("test")

    assert entity.name == "test"
    assert entity.id in world._entities
    assert world._entities[entity.id] == entity


def test_remove_entity() -> None:
    """Test removing entities from the world."""
    world = World()
    entity = world.create_entity()

    # Mark for removal
    world.remove_entity(entity)
    assert entity.id in world._pending_removal
    assert entity.id in world._entities  # Still exists until cleanup

    # Update to trigger cleanup
    world.update(0.016)
    assert entity.id not in world._entities
    assert len(world._pending_removal) == 0


def test_get_entity() -> None:
    """Test getting entities by ID."""
    world = World()
    entity = world.create_entity()

    retrieved = world.get_entity(entity.id)
    assert retrieved == entity

    # Test getting non-existent entity
    assert world.get_entity("non-existent") is None


def test_add_system() -> None:
    """Test adding and running systems."""
    world = World()
    calls = []

    def test_system(dt: float) -> None:
        calls.append(dt)

    world.add_system(test_system)
    world.update(0.016)

    assert len(calls) == 1
    assert calls[0] == 0.016


def test_get_entities_with_component() -> None:
    """Test querying entities by component type."""
    world = World()

    # Create some entities with different components
    entity1 = world.create_entity()
    entity1.add_component(TestComponent(1))

    entity2 = world.create_entity()
    entity2.add_component(TestComponent(2))

    entity3 = world.create_entity()  # No component

    # Test querying
    entities = world.get_entities_with_component(TestComponent)
    assert len(entities) == 2
    assert entity1 in entities
    assert entity2 in entities
    assert entity3 not in entities

    # Test cache
    assert TestComponent in world._component_cache
    assert world._component_cache[TestComponent] == entities


def test_component_cache_invalidation() -> None:
    """Test that component cache is properly invalidated."""
    world = World()

    # Create entity and cache query
    entity = world.create_entity()
    entity.add_component(TestComponent())
    entities1 = world.get_entities_with_component(TestComponent)
    assert len(entities1) == 1

    # Remove entity and verify cache is cleared
    world.remove_entity(entity)
    world.update(0.016)  # Trigger cleanup
    assert len(world._component_cache) == 0

    # Query again
    entities2 = world.get_entities_with_component(TestComponent)
    assert len(entities2) == 0


def test_clear() -> None:
    """Test clearing all entities from the world."""
    world = World()

    # Add some entities
    entity1 = world.create_entity()
    entity1.add_component(TestComponent())
    entity2 = world.create_entity()
    world.get_entities_with_component(TestComponent)  # Build cache

    # Clear world
    world.clear()
    assert len(world._entities) == 0
    assert len(world._component_cache) == 0
    assert len(world._pending_removal) == 0


def test_parent_child_cleanup() -> None:
    """Test that removing a parent entity also cleans up children."""
    world = World()

    # Create parent and child
    parent = world.create_entity("parent")
    child = world.create_entity("child")
    child.set_parent(parent)

    # Remove parent
    world.remove_entity(parent)
    world.update(0.016)  # Trigger cleanup

    assert parent.id not in world._entities
    assert child.parent is None  # Child should be detached
