from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Set, List, Optional
import time
import pygame

class InputState(Enum):
    """Possible states for an input action."""
    NONE = auto()
    PRESSED = auto()  # Just pressed this frame
    HELD = auto()     # Held down
    RELEASED = auto() # Just released this frame

@dataclass
class InputAction:
    """Configuration for an input action."""
    name: str
    buffer_time: float = 0.0  # Time in seconds to buffer this input

@dataclass
class InputBinding:
    """Binding between an action and its keys."""
    action: InputAction
    keys: Set[int]  # Set of pygame key constants

class InputManager:
    """
    Manages input state and key bindings.
    Supports action mapping, input buffering, and both event-based and polling interfaces.
    """

    def __init__(self) -> None:
        """Initialize the input manager."""
        self.actions: Dict[str, InputAction] = {}
        self.bindings: Dict[str, Set[int]] = {}
        self.state: Dict[str, InputState] = {}

        # Input buffering
        self._buffer_times: Dict[str, float] = {}  # Time remaining in buffer
        self._last_press_times: Dict[str, float] = {}  # Time of last press

    def register_action(self, name: str, buffer_time: float = 0.0) -> None:
        """Register a new input action.
        
        Args:
            name: Name of the action
            buffer_time: Time in seconds to buffer this input
            
        Raises:
            ValueError: If action already exists
        """
        if name in self.actions:
            raise ValueError(f"Action '{name}' already registered")

        self.actions[name] = InputAction(name, buffer_time)
        self.bindings[name] = set()
        self.state[name] = InputState.NONE
        self._buffer_times[name] = 0.0
        self._last_press_times[name] = 0.0

    def bind_key(self, action: str, key: int) -> None:
        """Bind a key to an action.
        
        Args:
            action: Name of the action
            key: Pygame key constant
            
        Raises:
            ValueError: If action doesn't exist
        """
        if action not in self.actions:
            raise ValueError(f"Action '{action}' not registered")

        self.bindings[action].add(key)

    def clear_bindings(self, action: str) -> None:
        """Clear all key bindings for an action.
        
        Args:
            action: Name of the action
            
        Raises:
            ValueError: If action doesn't exist
        """
        if action not in self.actions:
            raise ValueError(f"Action '{action}' not registered")

        self.bindings[action].clear()

    def get_bindings(self, action: str) -> Set[int]:
        """Get all key bindings for an action.
        
        Args:
            action: Name of the action
            
        Returns:
            Set of pygame key constants
            
        Raises:
            ValueError: If action doesn't exist
        """
        if action not in self.actions:
            raise ValueError(f"Action '{action}' not registered")

        return self.bindings[action].copy()

    def load_mapping(self, mapping: Dict[str, List[int]]) -> None:
        """Load a complete action mapping configuration.
        
        Args:
            mapping: Dictionary mapping action names to lists of key constants
        """
        for action, keys in mapping.items():
            if action not in self.actions:
                self.register_action(action)
            for key in keys:
                self.bind_key(action, key)

    def process_event(self, event: pygame.event.Event) -> None:
        """Process a pygame event and update input state.
        
        Args:
            event: Pygame event to process
        """
        if event.type == pygame.KEYDOWN:
            for action, keys in self.bindings.items():
                if event.key in keys:
                    self.state[action] = InputState.PRESSED
                    self._last_press_times[action] = time.perf_counter()
                    # Start buffer timer if action has buffer time
                    if self.actions[action].buffer_time > 0:
                        self._buffer_times[action] = self.actions[action].buffer_time

        elif event.type == pygame.KEYUP:
            for action, keys in self.bindings.items():
                if event.key in keys:
                    # Only mark as released if it was pressed or held
                    if self.state[action] in (InputState.PRESSED, InputState.HELD):
                        self.state[action] = InputState.RELEASED

    def update(self) -> None:
        """Update input state for this frame."""
        current_time = time.perf_counter()

        for action in self.actions:
            # Update press/hold/release state
            if self.state[action] == InputState.PRESSED:
                self.state[action] = InputState.HELD
            elif self.state[action] == InputState.RELEASED:
                self.state[action] = InputState.NONE

            # Update input buffers
            if self._buffer_times[action] > 0:
                self._buffer_times[action] -= current_time - self._last_press_times[action]
                if self._buffer_times[action] <= 0:
                    self._buffer_times[action] = 0.0
                self._last_press_times[action] = current_time

    def is_pressed(self, action: str) -> bool:
        """Check if an action was just pressed this frame.
        
        Args:
            action: Name of the action
            
        Returns:
            True if action was just pressed
            
        Raises:
            ValueError: If action doesn't exist
        """
        if action not in self.actions:
            raise ValueError(f"Action '{action}' not registered")

        return self.state[action] == InputState.PRESSED

    def is_held(self, action: str) -> bool:
        """Check if an action is being held down.
        
        Args:
            action: Name of the action
            
        Returns:
            True if action is held down
            
        Raises:
            ValueError: If action doesn't exist
        """
        if action not in self.actions:
            raise ValueError(f"Action '{action}' not registered")

        return self.state[action] in (InputState.PRESSED, InputState.HELD)

    def is_released(self, action: str) -> bool:
        """Check if an action was just released this frame.
        
        Args:
            action: Name of the action
            
        Returns:
            True if action was just released
            
        Raises:
            ValueError: If action doesn't exist
        """
        if action not in self.actions:
            raise ValueError(f"Action '{action}' not registered")

        return self.state[action] == InputState.RELEASED

    def is_buffered(self, action: str) -> bool:
        """Check if an action is currently buffered.
        
        Args:
            action: Name of the action
            
        Returns:
            True if action is buffered
            
        Raises:
            ValueError: If action doesn't exist
        """
        if action not in self.actions:
            raise ValueError(f"Action '{action}' not registered")

        return self._buffer_times[action] > 0
