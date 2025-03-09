"""Input handling system for keyboard and mouse events.

This module provides a flexible input system that supports action mapping,
input buffering, and state tracking for both keyboard and mouse input.
"""
import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Set

import pygame


class InputState(Enum):
    """Possible states for an input action."""

    NONE = auto()
    PRESSED = auto()  # Just pressed this frame
    HELD = auto()  # Held down
    RELEASED = auto()  # Just released this frame


@dataclass
class InputAction:
    """Configuration for an input action."""

    name: str
    buffer_time: float = 0.0


@dataclass
class InputBinding:
    """Configuration for an input binding."""

    action: str
    key: int


class InputManager:
    """Manages input state and bindings."""

    def __init__(self) -> None:
        """Initialize the input manager."""
        self._bindings: Dict[str, Set[int]] = {}  # Action -> Set of keys
        self._key_to_action: Dict[int, str] = {}  # Key -> Action
        self._pressed: Set[str] = set()  # Actions pressed this frame
        self._held: Set[str] = set()  # Actions being held
        self._released: Set[str] = set()  # Actions released this frame
        self._buffer_times: Dict[str, float] = {}  # Action -> Buffer time remaining
        self._buffer_durations: Dict[str, float] = {}  # Action -> Buffer duration
        self._last_update_time: float = time.perf_counter()

    def register_action(self, action: str, buffer_time: float = 0.0) -> None:
        """Register a new action.

        Args:
            action: Name of the action
            buffer_time: Time in seconds to buffer the input

        Raises:
            ValueError: If the action already exists
        """
        if action in self._bindings:
            raise ValueError(f"Action '{action}' already exists")
        self._bindings[action] = set()
        if buffer_time > 0:
            self._buffer_durations[action] = buffer_time

    def bind_key(self, action: str, key: int) -> None:
        """Bind a key to an action.

        Args:
            action: Name of the action to bind to
            key: Pygame key constant

        Raises:
            KeyError: If the action doesn't exist
        """
        if action not in self._bindings:
            raise KeyError(f"Action '{action}' not found")
        self._bindings[action].add(key)
        self._key_to_action[key] = action

    def unbind_key(self, action: str, key: int) -> None:
        """Unbind a key from an action.

        Args:
            action: Name of the action to unbind from
            key: Pygame key constant to unbind

        Raises:
            KeyError: If the action doesn't exist
        """
        if action not in self._bindings:
            raise KeyError(f"Action '{action}' not found")
        self._bindings[action].discard(key)
        if key in self._key_to_action:
            del self._key_to_action[key]

    def clear_bindings(self, action: str) -> None:
        """Clear all key bindings for an action.

        Args:
            action: Name of the action to clear

        Raises:
            KeyError: If the action doesn't exist
        """
        if action not in self._bindings:
            raise KeyError(f"Action '{action}' not found")
        for key in list(self._bindings[action]):
            self.unbind_key(action, key)

    def load_mapping(self, mapping: Dict[str, List[int]]) -> None:
        """Load a key mapping configuration.

        Args:
            mapping: Dictionary mapping action names to lists of key constants
        """
        for action, keys in mapping.items():
            if action not in self._bindings:
                self.register_action(action)
            for key in keys:
                self.bind_key(action, key)

    def process_event(self, event: pygame.event.Event) -> None:
        """Process an input event.

        Args:
            event: Pygame event to process
        """
        if event.type == pygame.KEYDOWN:
            if event.key in self._key_to_action:
                action = self._key_to_action[event.key]
                if action not in self._held:  # Only mark as pressed if not already held
                    self._pressed.add(action)
                self._held.add(action)
                if action in self._buffer_durations:
                    self._buffer_times[action] = self._buffer_durations[action]

        elif event.type == pygame.KEYUP:
            if event.key in self._key_to_action:
                action = self._key_to_action[event.key]
                if action in self._held:  # Only mark as released if was held
                    self._released.add(action)
                self._held.discard(action)

    def update(self) -> None:
        """Update input state for this frame."""
        current_time = time.perf_counter()
        dt = current_time - self._last_update_time
        self._last_update_time = current_time

        # Update buffer times
        for action in list(self._buffer_times.keys()):
            self._buffer_times[action] -= dt
            if self._buffer_times[action] <= 0:
                del self._buffer_times[action]

        # Clear one-frame states
        self._pressed.clear()
        self._released.clear()

    def is_pressed(self, action: str) -> bool:
        """Check if an action was pressed this frame.

        Args:
            action: Name of the action to check

        Returns:
            True if the action was pressed this frame
        """
        if action not in self._bindings:
            raise ValueError(f"Action '{action}' not registered")
        return action in self._pressed

    def is_held(self, action: str) -> bool:
        """Check if an action is being held.

        Args:
            action: Name of the action to check

        Returns:
            True if the action is being held
        """
        if action not in self._bindings:
            raise ValueError(f"Action '{action}' not registered")
        return action in self._held

    def is_released(self, action: str) -> bool:
        """Check if an action was released this frame.

        Args:
            action: Name of the action to check

        Returns:
            True if the action was released this frame
        """
        if action not in self._bindings:
            raise ValueError(f"Action '{action}' not registered")
        return action in self._released

    def is_buffered(self, action: str) -> bool:
        """Check if an action is in the input buffer.

        Args:
            action: Name of the action to check

        Returns:
            True if the action is in the buffer
        """
        if action not in self._bindings:
            raise ValueError(f"Action '{action}' not registered")
        return action in self._buffer_times and self._buffer_times[action] > 0.0
