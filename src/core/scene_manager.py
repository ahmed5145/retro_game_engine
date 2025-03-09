"""Scene management system for handling multiple scenes and transitions."""
from typing import Dict, List, Optional, Type, TypeVar

from .scene import Scene

T = TypeVar("T", bound=Scene)


class SceneManager:
    """Manages multiple scenes and handles transitions between them.

    The SceneManager maintains a stack of scenes and ensures proper lifecycle
    management when switching between scenes.
    """

    def __init__(self) -> None:
        """Initialize the scene manager."""
        self._scenes: Dict[str, Scene] = {}
        self._scene_stack: List[Scene] = []
        self._pending_transition: Optional[Scene] = None

    @property
    def current_scene(self) -> Optional[Scene]:
        """Get the currently active scene."""
        return self._scene_stack[-1] if self._scene_stack else None

    def register_scene(self, scene: Scene) -> None:
        """Register a scene with the manager.

        Args:
            scene: Scene to register

        Raises:
            ValueError: If scene with same name already exists
        """
        if scene.name in self._scenes:
            raise ValueError(f"Scene '{scene.name}' already registered")
        self._scenes[scene.name] = scene

    def get_scene(self, name: str) -> Optional[Scene]:
        """Get a registered scene by name.

        Args:
            name: Name of the scene

        Returns:
            Scene if found, None otherwise
        """
        return self._scenes.get(name)

    def push_scene(self, scene: Scene) -> None:
        """Push a new scene onto the stack.

        The current scene (if any) will be paused.

        Args:
            scene: Scene to push
        """
        # Initialize scene if needed
        if not scene.initialized:
            scene.initialize()

        # Pause current scene
        if current := self.current_scene:
            current.pause()

        # Push and load new scene
        self._scene_stack.append(scene)
        scene.load()

    def pop_scene(self) -> Optional[Scene]:
        """Pop the current scene from the stack.

        Returns:
            The popped scene, or None if stack was empty
        """
        if not self._scene_stack:
            return None

        # Unload and pop current scene
        current = self._scene_stack.pop()
        current.unload()

        # Resume previous scene if any
        if self.current_scene:
            self.current_scene.resume()

        return current

    def switch_scene(self, scene: Scene) -> None:
        """Switch to a new scene, replacing the current one.

        Args:
            scene: Scene to switch to
        """
        # Pop all scenes
        while self._scene_stack:
            self.pop_scene()

        # Push new scene
        self.push_scene(scene)

    def update(self, dt: float) -> None:
        """Update the current scene.

        Args:
            dt: Delta time in seconds
        """
        if current := self.current_scene:
            current.update(dt)

    def clear(self) -> None:
        """Clear all scenes and reset the manager."""
        while self._scene_stack:
            self.pop_scene()
        self._scenes.clear()
