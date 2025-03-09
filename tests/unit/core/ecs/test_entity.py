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
    entity = Entity("test_entity")
    assert entity.name == "test_entity"
    assert entity.id != ""
    assert entity.enabled
    assert not entity._components
    assert not entity._children
    assert entity.parent is None


def test_entity_auto_name() -> None:
    """Test automatic entity naming."""
    entity = Entity()
    assert entity.name.startswith("Entity_")
    assert len(entity.name) > 7  # "Entity_" + at least 1 character


def test_add_component(test_component: DummyComponent) -> None:
    """Test adding a component to an entity."""
    entity = Entity()

    # Test adding component
    entity.add_component(test_component)
    assert test_component in entity._components
    assert test_component.entity == entity

    # Test adding duplicate component type
    with pytest.raises(ValueError):
        entity.add_component(DummyComponent())


def test_remove_component(test_component: DummyComponent) -> None:
    """Test removing a component from an entity."""
    entity = Entity()
    entity.add_component(test_component)

    # Test removing component
    entity.remove_component(DummyComponent)
    assert test_component not in entity._components
    assert test_component.entity is None


def test_get_component(test_component: DummyComponent) -> None:
    """Test getting a component from an entity."""
    entity = Entity()
    entity.add_component(test_component)

    # Test getting existing component
    assert entity.get_component(DummyComponent) == test_component

    # Test getting non-existent component
    entity.remove_component(DummyComponent)
    assert entity.get_component(DummyComponent) is None


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
