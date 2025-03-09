"""Unit tests for the SceneManager class."""
import pytest
from src.core.scene import Scene
from src.core.scene_manager import SceneManager
from typing import List

class MockScene(Scene):
    """Mock scene for testing."""
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.update_called = False
        
    def update(self, dt: float) -> None:
        if not self.paused:
            super().update(dt)
            self.update_called = True

@pytest.fixture
def scene_manager() -> SceneManager:
    """Create a fresh SceneManager for each test."""
    return SceneManager()

@pytest.fixture
def mock_scenes() -> List[MockScene]:
    """Create a set of mock scenes for testing."""
    return [MockScene(f"scene_{i}") for i in range(3)]

def test_scene_registration(scene_manager: SceneManager, mock_scenes: List[MockScene]) -> None:
    """Test scene registration functionality."""
    scene = mock_scenes[0]
    
    # Test successful registration
    scene_manager.register_scene(scene)
    assert scene_manager.get_scene(scene.name) == scene
    
    # Test duplicate registration
    with pytest.raises(ValueError):
        scene_manager.register_scene(scene)
    
    # Test getting non-existent scene
    assert scene_manager.get_scene("non_existent") is None

def test_scene_stack_operations(scene_manager: SceneManager, mock_scenes: List[MockScene]) -> None:
    """Test scene stack push/pop operations."""
    scene1, scene2 = mock_scenes[:2]
    
    # Test push
    scene_manager.push_scene(scene1)
    assert scene_manager.current_scene == scene1
    assert scene1.active
    
    # Test second push
    if scene1.active:
        scene_manager.push_scene(scene2)
        assert scene_manager.current_scene == scene2
        assert scene2.active
        assert scene1.paused
    
        # Test pop
        if scene2.active:
            popped = scene_manager.pop_scene()
            assert popped == scene2
            assert not scene2.active
            assert scene_manager.current_scene == scene1
            assert not scene1.paused

def test_scene_switching(scene_manager: SceneManager, mock_scenes: List[MockScene]) -> None:
    """Test scene switching functionality."""
    scene1, scene2 = mock_scenes[:2]
    
    # Push initial scenes
    scene_manager.push_scene(scene1)
    scene_manager.push_scene(scene2)
    assert len(scene_manager._scene_stack) == 2
    
    # Switch to new scene
    scene3 = mock_scenes[2]
    scene_manager.switch_scene(scene3)
    
    # Verify stack is cleared and new scene is active
    assert len(scene_manager._scene_stack) == 1
    assert scene_manager.current_scene == scene3
    assert scene3.active
    assert not scene1.active
    assert not scene2.active

def test_scene_update(scene_manager: SceneManager, mock_scenes: List[MockScene]) -> None:
    """Test scene update propagation."""
    scene = mock_scenes[0]
    scene_manager.push_scene(scene)
    
    # Test update propagation
    scene_manager.update(0.016)
    assert scene.update_called
    
    # Test update when paused
    scene.update_called = False
    scene.pause()
    scene_manager.update(0.016)
    assert not scene.update_called

def test_scene_manager_clear(scene_manager: SceneManager, mock_scenes: List[MockScene]) -> None:
    """Test clearing all scenes."""
    # Push multiple scenes
    for scene in mock_scenes:
        scene_manager.register_scene(scene)
        scene_manager.push_scene(scene)
    
    # Clear manager
    scene_manager.clear()
    assert len(scene_manager._scene_stack) == 0
    assert len(scene_manager._scenes) == 0
    assert scene_manager.current_scene is None
    
    # Verify all scenes are unloaded
    for scene in mock_scenes:
        assert not scene.active 