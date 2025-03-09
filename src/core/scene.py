"""Scene management system for the game engine."""
from typing import Any, Dict, Optional

import pygame

from .ecs import World


class Scene:
    """A scene represents a distinct state in the game (level, menu, etc.).

    Scenes manage their own World instance and provide lifecycle methods for
    initialization, cleanup, and state management.
    """

    def __init__(self, name: str = "") -> None:
        """Initialize the scene.

        Args:
            name: Optional name for the scene (default: "")
        """
        self.name = name
        self.world = World()
        self._initialized = False
        self._active = False
        self._paused = False
        self._environment_vars: Dict[str, Any] = {}

    @property
    def initialized(self) -> bool:
        """Check if the scene has been initialized."""
        return self._initialized

    @property
    def active(self) -> bool:
        """Check if the scene is currently active."""
        return self._active

    @property
    def paused(self) -> bool:
        """Check if the scene is paused."""
        return self._paused

    def initialize(self) -> None:
        """Initialize the scene.

        This is called once when the scene is first created.
        Override this to set up your scene.
        """
        self._initialized = True

    def load(self) -> None:
        """Load scene resources.

        Called when the scene becomes active.
        Override this to load assets, create entities, etc.
        """
        self._active = True
        self._paused = False

    def unload(self) -> None:
        """Unload scene resources.

        Called when the scene becomes inactive.
        Override this to clean up resources.
        """
        self._active = False
        self._paused = False
        self.world.clear()

    def pause(self) -> None:
        """Pause the scene.

        Called when another scene is pushed on top of this one.
        """
        self._paused = True

    def resume(self) -> None:
        """Resume the scene.

        Called when this scene becomes active again after being paused.
        """
        self._paused = False

    def update(self, dt: float) -> None:
        """Update the scene.

        Args:
            dt: Delta time in seconds
        """
        if self._active and not self._paused:
            self.world.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        """Render the scene.

        Args:
            surface: Surface to render to
        """
        pass

    def set_environment_variable(self, key: str, value: Any) -> None:
        """Set a scene-specific environment variable.

        Args:
            key: Variable name
            value: Variable value
        """
        self._environment_vars[key] = value

    def get_environment_variable(self, key: str, default: Any = None) -> Any:
        """Get a scene-specific environment variable.

        Args:
            key: Variable name
            default: Default value if key doesn't exist

        Returns:
            Variable value or default
        """
        return self._environment_vars.get(key, default)
