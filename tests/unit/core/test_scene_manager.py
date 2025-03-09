"""Unit tests for the SceneManager class."""
from typing import List

import pytest

from src.core.scene import Scene
from src.core.scene_manager import SceneManager


class MockScene(Scene):
    """Mock scene for testing."""

    def __init__(self, name: str) -> None:
        """Initialize the mock scene."""
        super().__init__(name)
        self.update_called = False

    def update(self, dt: float) -> None:
        """Track update calls."""
        super().update(dt)
        self.update_called = True


@pytest.fixture
def scene_manager() -> SceneManager:
    """Create a scene manager for testing."""
    return SceneManager()


@pytest.fixture
def mock_scenes() -> List[MockScene]:
    """Create mock scenes for testing."""
    return [MockScene(f"scene{i}") for i in range(3)]


def test_scene_registration(
    scene_manager: SceneManager, mock_scenes: List[MockScene]
) -> None:
    """Test scene registration."""
    scene1, scene2 = mock_scenes[:2]

    # Test registration
    scene_manager.register_scene(scene1)
    assert scene_manager.get_scene(scene1.name) == scene1

    # Test duplicate registration
    with pytest.raises(ValueError):
        scene_manager.register_scene(scene1)

    # Test multiple scenes
    scene_manager.register_scene(scene2)
    assert scene_manager.get_scene(scene2.name) == scene2


def test_scene_stack_operations(
    scene_manager: SceneManager, mock_scenes: List[MockScene]
) -> None:
    """Test scene stack push operations."""
    scene1, scene2 = mock_scenes[:2]

    # Test initial push
    scene_manager.push_scene(scene1)
    assert scene_manager.current_scene == scene1
    assert scene1.active

    # Test second push
    scene_manager.push_scene(scene2)
    assert scene_manager.current_scene == scene2
    assert scene2.active
    assert scene1.paused


def test_scene_stack_pop(
    scene_manager: SceneManager, mock_scenes: List[MockScene]
) -> None:
    """Test scene stack pop operations."""
    scene1, scene2 = mock_scenes[:2]

    # Setup stack
    scene_manager.push_scene(scene1)
    scene_manager.push_scene(scene2)

    # Test pop
    popped = scene_manager.pop_scene()
    assert popped == scene2
    assert not scene2.active
    assert scene_manager.current_scene == scene1
    assert not scene1.paused


def test_scene_switching(
    scene_manager: SceneManager, mock_scenes: List[MockScene]
) -> None:
    """Test scene switching functionality."""
    scene1, scene2 = mock_scenes[:2]

    # Test initial switch
    scene_manager.switch_scene(scene1)
    assert scene_manager.current_scene == scene1
    assert scene1.active

    # Test switching to new scene
    scene_manager.switch_scene(scene2)
    assert scene_manager.current_scene == scene2
    assert scene2.active
    assert not scene1.active

    # Test switching to same scene (no effect)
    scene_manager.switch_scene(scene2)
    assert scene_manager.current_scene == scene2
    assert scene2.active


def test_scene_update(
    scene_manager: SceneManager, mock_scenes: List[MockScene]
) -> None:
    """Test scene update propagation."""
    scene = mock_scenes[0]
    scene_manager.push_scene(scene)

    # Test update propagation
    scene_manager.update(0.016)
    assert scene.update_called


def test_scene_manager_clear(
    scene_manager: SceneManager, mock_scenes: List[MockScene]
) -> None:
    """Test clearing all scenes."""
    scene1, scene2 = mock_scenes[:2]

    # Setup scenes
    scene_manager.push_scene(scene1)
    scene_manager.push_scene(scene2)

    # Test clear
    scene_manager.clear()
    assert scene_manager.current_scene is None
    assert not scene1.active
    assert not scene2.active
