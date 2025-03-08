"""Tests for the Entity class."""
import pytest

from src.core.ecs import Component, Entity


class TestComponent(Component):
    """Test component for testing."""

    def __init__(self, value: int = 0):
        super().__init__()
        self.value = value


def test_entity_initialization() -> None:
    """Test that entity is properly initialized."""
    entity = Entity("test")
    assert entity.name == "test"
    assert entity.enabled
    assert entity.parent is None
    assert len(entity.children) == 0


def test_entity_auto_name() -> None:
    """Test that entity gets auto-generated name if none provided."""
    entity = Entity()
    assert entity.name.startswith("Entity_")
    assert len(entity.name) > 7  # Should have UUID part


def test_add_component() -> None:
    """Test adding components to entity."""
    entity = Entity()
    component = TestComponent(42)

    entity.add_component(component)
    assert entity.has_component(TestComponent)
    assert component.entity == entity

    # Test adding duplicate component type
    with pytest.raises(ValueError):
        entity.add_component(TestComponent())


def test_remove_component() -> None:
    """Test removing components from entity."""
    entity = Entity()
    component = TestComponent()

    entity.add_component(component)
    assert entity.has_component(TestComponent)

    entity.remove_component(TestComponent)
    assert not entity.has_component(TestComponent)
    assert component.entity is None


def test_get_component() -> None:
    """Test getting components from entity."""
    entity = Entity()
    component = TestComponent(42)

    entity.add_component(component)
    retrieved = entity.get_component(TestComponent)
    assert retrieved is component
    assert retrieved.value == 42  # type: ignore

    # Test getting non-existent component
    assert entity.get_component(Component) is None


def test_parent_child_relationship() -> None:
    """Test parent-child relationships between entities."""
    parent = Entity("parent")
    child1 = Entity("child1")
    child2 = Entity("child2")

    # Add children
    parent.add_child(child1)
    parent.add_child(child2)

    assert child1.parent == parent
    assert child2.parent == parent
    assert len(parent.children) == 2
    assert parent.children[child1.id] == child1
    assert parent.children[child2.id] == child2

    # Remove child
    parent.remove_child(child1)
    assert child1.parent is None
    assert len(parent.children) == 1
    assert child1.id not in parent.children

    # Change parent
    new_parent = Entity("new_parent")
    child2.set_parent(new_parent)
    assert child2.parent == new_parent
    assert len(parent.children) == 0
    assert len(new_parent.children) == 1


def test_enable_disable() -> None:
    """Test enabling and disabling entities."""
    entity = Entity()
    assert entity.enabled

    entity.enabled = False
    assert not entity.enabled

    entity.enabled = True
    assert entity.enabled
