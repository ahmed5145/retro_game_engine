"""Unit tests for the Scene class."""
import pytest

from src.core.ecs.world import World
from src.core.scene import Scene


def test_scene_initialization() -> None:
    """Test scene initialization."""
    scene = Scene("test_scene")
    assert scene.name == "test_scene"
    assert isinstance(scene.world, World)
    assert not scene.initialized
    assert not scene.active
    assert not scene.paused


def test_scene_lifecycle() -> None:
    """Test scene lifecycle methods."""
    scene = Scene("test_scene")

    # Test initialize
    scene.initialize()
    assert scene.initialized

    # Test load
    scene.load()
    assert scene.active
    assert not scene.paused

    # Test pause/resume
    scene.pause()
    assert scene.paused
    scene.resume()
    assert not scene.paused

    # Test unload
    scene.unload()
    assert not scene.active


def test_scene_environment_variables() -> None:
    """Test scene environment variable management."""
    scene = Scene("test_scene")

    # Test setting and getting variables
    scene.set_environment_variable("test_var", 42)
    assert scene.get_environment_variable("test_var") == 42

    # Test default value
    assert scene.get_environment_variable("non_existent", "default") == "default"

    # Test overwriting variable
    scene.set_environment_variable("test_var", "new_value")
    assert scene.get_environment_variable("test_var") == "new_value"


def test_scene_update() -> None:
    """Test scene update behavior."""
    scene = Scene("test_scene")
    scene.initialize()
    scene.load()

    # Scene should update when active and not paused
    scene.update(0.016)  # Typical frame time

    # Scene should not update when paused
    scene.pause()
    scene.update(0.016)

    # Scene should not update when unloaded
    scene.unload()
    scene.update(0.016)


def test_scene_world_management() -> None:
    """Test scene world management."""
    scene = Scene("test_scene")

    # World should be created on initialization
    assert scene.world is not None

    # World should be accessible
    world = scene.world
    assert isinstance(world, World)

    # Test that world updates with scene
    scene.initialize()
    scene.load()
    scene.update(0.016)  # Should trigger world update
