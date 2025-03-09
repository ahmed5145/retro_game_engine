"""Tests for the Entity class."""
from typing import Generator

import pytest

from src.core.ecs import Component, Entity


class DummyComponent(Component):
    """Test component for testing."""

    value: int = 0


@pytest.fixture
def test_component() -> DummyComponent:
    """Create a test component."""
    return DummyComponent()


def test_entity_initialization() -> None:
    """Test entity initialization."""
    entity = Entity("test")
    assert entity.name == "test"
    assert not entity.components
    assert not entity.children
    assert entity.enabled
    assert entity.parent is None


def test_entity_auto_name() -> None:
    """Test auto-generated entity names."""
    entity = Entity()
    assert entity.name  # Should have a non-empty auto-generated name


def test_add_component(test_component: DummyComponent) -> None:
    """Test adding a component to an entity."""
    entity = Entity()
    entity.add_component(test_component)
    assert test_component.entity == entity
    assert entity.get_component(DummyComponent) == test_component


def test_remove_component(test_component: DummyComponent) -> None:
    """Test removing a component from an entity."""
    entity = Entity()
    entity.add_component(test_component)
    entity.remove_component(DummyComponent)
    assert test_component.entity is None
    assert entity.get_component(DummyComponent) is None


def test_get_component(test_component: DummyComponent) -> None:
    """Test getting a component from an entity."""
    entity = Entity()
    assert entity.get_component(DummyComponent) is None
    entity.add_component(test_component)
    assert entity.get_component(DummyComponent) == test_component


def test_parent_child_relationship() -> None:
    """Test parent-child relationships between entities."""
    parent = Entity("parent")
    child1 = Entity("child1")
    child2 = Entity("child2")

    # Test adding children
    parent.add_child(child1)
    assert child1.parent == parent
    assert child1.id in parent.children

    parent.add_child(child2)
    assert child2.parent == parent
    assert len(parent.children) == 2

    # Test removing child
    parent.remove_child(child1)
    assert child1.parent is None
    assert child1.id not in parent.children
    assert len(parent.children) == 1

    # Test parent change
    child2.set_parent(None)
    assert child2.parent is None
    assert len(parent.children) == 0


def test_enable_disable() -> None:
    """Test enabling and disabling entities."""
    entity = Entity()
    assert entity.enabled

    entity.enabled = False
    assert not entity.enabled

    entity.enabled = True
    assert entity.enabled
