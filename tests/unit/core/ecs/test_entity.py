"""Tests for the Entity class."""
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


def test_add_component(test_component: DummyComponent) -> None:
    """Test adding components to entity."""
    entity = Entity()
    test_component.value = 42

    entity.add_component(test_component)
    assert entity.has_component(DummyComponent)
    assert test_component.entity == entity

    # Test adding duplicate component type
    with pytest.raises(ValueError):
        entity.add_component(DummyComponent())


def test_remove_component(test_component: DummyComponent) -> None:
    """Test removing components from entity."""
    entity = Entity()

    entity.add_component(test_component)
    assert entity.has_component(DummyComponent)

    entity.remove_component(DummyComponent)
    assert not entity.has_component(DummyComponent)
    assert test_component.entity is None


def test_get_component(test_component: DummyComponent) -> None:
    """Test getting components from entity."""
    entity = Entity()
    test_component.value = 42

    entity.add_component(test_component)
    retrieved = entity.get_component(DummyComponent)
    assert retrieved is test_component
    assert retrieved.value == 42

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

    # Test child removal
    if len(parent.children) == 2:
        parent.remove_child(child1)
        assert child1.parent is None
        assert len(parent.children) == 1
        assert child1.id not in parent.children

    # Test parent change
    new_parent = Entity("new_parent")
    if child2.parent == parent:
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
