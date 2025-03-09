"""Input handling system for keyboard and mouse events.

This module provides a flexible input system that supports action mapping,
input buffering, and state tracking for both keyboard and mouse input.
"""
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
    """Configuration for an input action.

    An action represents a game input (like "jump" or "shoot") that can be
    mapped to one or more physical inputs (keys or buttons).
    """

    name: str
    buffer_time: float = 0.0


@dataclass
class InputBinding:
    """Binding between an action and its keys.

    A binding maps a game action to one or more physical inputs and tracks
    the current state of those inputs.
    """

    action: InputAction
    keys: Set[int]
    state: InputState = InputState.NONE
    buffer_time_remaining: float = 0.0


class InputManager:
    """Manages input actions, bindings, and state."""

    def __init__(self) -> None:
        """Initialize the input manager."""
        self._actions: Dict[str, InputAction] = {}
        self._bindings: Dict[str, InputBinding] = {}
        self._pressed_keys: Set[int] = set()
        self._buffer_times: Dict[str, float] = {}
        self._state: Dict[str, bool] = {}

    @property
    def actions(self) -> Dict[str, InputAction]:
        """Get all registered actions."""
        return self._actions

    @property
    def bindings(self) -> Dict[str, InputBinding]:
        """Get all input bindings."""
        return self._bindings

    @property
    def state(self) -> Dict[str, bool]:
        """Get the current state of all input actions.

        Returns:
            Dict[str, bool]: A dictionary mapping action names to their current state.
        """
        return self._state

    @property
    def buffer_times(self) -> Dict[str, float]:
        """Get the buffer times for all input actions.

        Returns:
            Dict[str, float]: A dictionary mapping action names to their buffer times.
        """
        return self._buffer_times

    def register_action(self, name: str, buffer_time: float = 0.0) -> None:
        """Register a new input action.

        Args:
            name: Name of the action
            buffer_time: Time in seconds to buffer this input

        Raises:
            ValueError: If an action with this name already exists
        """
        if name in self._actions:
            raise ValueError(f"Action '{name}' already exists")

        self._actions[name] = InputAction(name, buffer_time)
        self._bindings[name] = InputBinding(self._actions[name], set())

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

        self._bindings[action].keys.add(key)

    def clear_bindings(self, action: str) -> None:
        """Clear all key bindings for an action.

        Args:
            action: Name of the action to clear

        Raises:
            KeyError: If the action doesn't exist
        """
        if action not in self._bindings:
            raise KeyError(f"Action '{action}' not found")

        self._bindings[action].keys.clear()

    def get_bindings(self, action: str) -> Set[int]:
        """Get all key bindings for an action.

        Args:
            action: Name of the action

        Returns:
            Set of pygame key constants bound to the action

        Raises:
            KeyError: If the action doesn't exist
        """
        if action not in self._bindings:
            raise KeyError(f"Action '{action}' not found")

        return self._bindings[action].keys.copy()

    def load_mapping(self, mapping: Dict[str, List[int]]) -> None:
        """Load a key mapping configuration.

        Args:
            mapping: Dictionary mapping action names to lists of key constants
        """
        for action, keys in mapping.items():
            if action in self._bindings:
                self._bindings[action].keys = set(keys)

    def process_event(self, event: pygame.event.Event) -> None:
        """Process an input event.

        Args:
            event: Pygame event to process
        """
        if event.type == pygame.KEYDOWN:
            self._pressed_keys.add(event.key)
            for binding in self._bindings.values():
                if event.key in binding.keys:
                    binding.state = InputState.PRESSED
                    binding.buffer_time_remaining = binding.action.buffer_time

        elif event.type == pygame.KEYUP:
            self._pressed_keys.discard(event.key)
            for binding in self._bindings.values():
                if event.key in binding.keys:
                    if binding.state in (InputState.PRESSED, InputState.HELD):
                        binding.state = InputState.RELEASED

    def update(self) -> None:
        """Update input states and buffers."""
        for binding in self._bindings.values():
            # Update state
            if binding.state == InputState.PRESSED:
                binding.state = InputState.HELD
            elif binding.state == InputState.RELEASED:
                binding.state = InputState.NONE

            # Update buffer time
            if binding.buffer_time_remaining > 0:
                binding.buffer_time_remaining = max(
                    0.0, binding.buffer_time_remaining - 1.0 / 60.0
                )

            # Check if any bound keys are pressed
            any_pressed = any(key in self._pressed_keys for key in binding.keys)
            if any_pressed and binding.state == InputState.NONE:
                binding.state = InputState.PRESSED
                binding.buffer_time_remaining = binding.action.buffer_time

    def is_pressed(self, action: str) -> bool:
        """Check if an action was just pressed.

        Args:
            action: Name of the action to check

        Returns:
            True if the action was just pressed, False otherwise

        Raises:
            KeyError: If the action doesn't exist
        """
        if action not in self._bindings:
            raise KeyError(f"Action '{action}' not found")

        return self._bindings[action].state == InputState.PRESSED

    def is_held(self, action: str) -> bool:
        """Check if an action is being held.

        Args:
            action: Name of the action to check

        Returns:
            True if the action is being held, False otherwise

        Raises:
            KeyError: If the action doesn't exist
        """
        if action not in self._bindings:
            raise KeyError(f"Action '{action}' not found")

        return self._bindings[action].state == InputState.HELD

    def is_released(self, action: str) -> bool:
        """Check if an action was just released.

        Args:
            action: Name of the action to check

        Returns:
            True if the action was just released, False otherwise

        Raises:
            KeyError: If the action doesn't exist
        """
        if action not in self._bindings:
            raise KeyError(f"Action '{action}' not found")

        return self._bindings[action].state == InputState.RELEASED

    def is_buffered(self, action: str) -> bool:
        """Check if an action is in its buffer window.

        Args:
            action: Name of the action to check

        Returns:
            True if the action is buffered, False otherwise

        Raises:
            KeyError: If the action doesn't exist
        """
        if action not in self._bindings:
            raise KeyError(f"Action '{action}' not found")

        return self._bindings[action].buffer_time_remaining > 0
