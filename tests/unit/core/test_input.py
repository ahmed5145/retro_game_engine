"""Tests for the input system."""
import time
from typing import Dict, Set

import pygame
import pytest

from src.core.input import InputAction, InputBinding, InputManager, InputState


def test_input_manager_initialization() -> None:
    """Test input manager initialization."""
    manager = InputManager()
    assert not manager._bindings
    assert not manager._pressed
    assert not manager._held
    assert not manager._released
    assert not manager._buffer_times


def test_action_registration() -> None:
    """Test registering input actions."""
    manager = InputManager()
    manager.register_action("JUMP")
    assert "JUMP" in manager._bindings
    assert not manager._bindings["JUMP"]  # No keys bound yet

    # Test registering with buffer time
    manager.register_action("ATTACK", buffer_time=0.1)
    assert "ATTACK" in manager._bindings
    assert "ATTACK" in manager._buffer_durations
    assert manager._buffer_durations["ATTACK"] == 0.1

    # Test duplicate registration
    with pytest.raises(ValueError):
        manager.register_action("JUMP")


def test_key_binding() -> None:
    """Test binding keys to actions."""
    manager = InputManager()
    manager.register_action("JUMP")
    manager.bind_key("JUMP", pygame.K_SPACE)

    assert pygame.K_SPACE in manager._bindings["JUMP"]
    assert manager._key_to_action[pygame.K_SPACE] == "JUMP"

    # Test binding multiple keys
    manager.bind_key("JUMP", pygame.K_UP)
    assert pygame.K_UP in manager._bindings["JUMP"]
    assert manager._key_to_action[pygame.K_UP] == "JUMP"

    # Test binding to non-existent action
    with pytest.raises(KeyError):
        manager.bind_key("NONEXISTENT", pygame.K_SPACE)


def test_input_state() -> None:
    """Test input state tracking."""
    manager = InputManager()
    manager.register_action("JUMP")
    manager.bind_key("JUMP", pygame.K_SPACE)

    # Test key press
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
    manager.process_event(event)

    assert manager.is_pressed("JUMP")
    assert manager.is_held("JUMP")
    assert not manager.is_released("JUMP")

    # After update, should only be held
    manager.update()
    assert not manager.is_pressed("JUMP")
    assert manager.is_held("JUMP")
    assert not manager.is_released("JUMP")

    # Test key release
    event = pygame.event.Event(pygame.KEYUP, {"key": pygame.K_SPACE})
    manager.process_event(event)

    assert not manager.is_pressed("JUMP")
    assert not manager.is_held("JUMP")
    assert manager.is_released("JUMP")

    # After update, all states should be cleared
    manager.update()
    assert not manager.is_pressed("JUMP")
    assert not manager.is_held("JUMP")
    assert not manager.is_released("JUMP")


def test_input_buffering() -> None:
    """Test input buffering system."""
    manager = InputManager()
    manager.register_action("ATTACK", buffer_time=0.1)  # 100ms buffer
    manager.bind_key("ATTACK", pygame.K_x)

    # Test key press
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_x})
    manager.process_event(event)

    assert manager.is_pressed("ATTACK")
    assert manager.is_held("ATTACK")
    assert manager.is_buffered("ATTACK")

    # After update, should still be held and buffered
    manager.update()
    assert not manager.is_pressed("ATTACK")
    assert manager.is_held("ATTACK")
    assert manager.is_buffered("ATTACK")

    # Test buffer expiration
    manager._buffer_times["ATTACK"] = -0.1  # Force buffer expiration
    manager.update()
    assert not manager.is_pressed("ATTACK")
    assert manager.is_held("ATTACK")
    assert not manager.is_buffered("ATTACK")


def test_action_mapping() -> None:
    """Test action mapping system."""
    manager = InputManager()

    # Create a mapping
    mapping = {
        "MOVE_LEFT": [pygame.K_LEFT, pygame.K_a],
        "MOVE_RIGHT": [pygame.K_RIGHT, pygame.K_d],
        "JUMP": [pygame.K_SPACE, pygame.K_w],
    }

    manager.load_mapping(mapping)

    # Verify all actions and bindings are set up
    for action, keys in mapping.items():
        assert action in manager._bindings
        for key in keys:
            assert key in manager._bindings[action]
            assert manager._key_to_action[key] == action


def test_binding_management() -> None:
    """Test managing key bindings."""
    manager = InputManager()
    manager.register_action("TEST")
    manager.bind_key("TEST", pygame.K_a)

    # Test unbinding key
    manager.unbind_key("TEST", pygame.K_a)
    assert pygame.K_a not in manager._bindings["TEST"]
    assert pygame.K_a not in manager._key_to_action

    # Test clearing all bindings
    manager.bind_key("TEST", pygame.K_b)
    manager.clear_bindings("TEST")
    assert not manager._bindings["TEST"]
    assert pygame.K_b not in manager._key_to_action


def test_multiple_key_bindings() -> None:
    """Test handling multiple key bindings for an action."""
    manager = InputManager()
    manager.register_action("MOVE")
    manager.bind_key("MOVE", pygame.K_LEFT)
    manager.bind_key("MOVE", pygame.K_a)

    # Test both keys trigger the action
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT})
    manager.process_event(event)
    manager.update()
    assert manager.is_held("MOVE")

    event = pygame.event.Event(pygame.KEYUP, {"key": pygame.K_LEFT})
    manager.process_event(event)
    manager.update()

    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a})
    manager.process_event(event)
    manager.update()
    assert manager.is_held("MOVE")


def test_simultaneous_keys() -> None:
    """Test handling multiple keys pressed simultaneously."""
    input_manager = InputManager()
    input_manager.register_action("MOVE_LEFT")
    input_manager.register_action("MOVE_RIGHT")

    input_manager.bind_key("MOVE_LEFT", pygame.K_LEFT)
    input_manager.bind_key("MOVE_RIGHT", pygame.K_RIGHT)

    # Press both keys
    event1 = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT})
    event2 = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT})

    input_manager.process_event(event1)
    input_manager.process_event(event2)
    input_manager.update()

    assert input_manager.is_held("MOVE_LEFT")
    assert input_manager.is_held("MOVE_RIGHT")

    # Release one key
    event = pygame.event.Event(pygame.KEYUP, {"key": pygame.K_LEFT})
    input_manager.process_event(event)
    input_manager.update()

    assert not input_manager.is_held("MOVE_LEFT")
    assert input_manager.is_held("MOVE_RIGHT")


def test_buffer_timing_precision() -> None:
    """Test precise timing of input buffer system."""
    input_manager = InputManager()
    buffer_time = 0.1  # 100ms
    input_manager.register_action("ATTACK", buffer_time=buffer_time)
    input_manager.bind_key("ATTACK", pygame.K_x)

    # Simulate key press
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_x})
    input_manager.process_event(event)

    # Check buffer just before expiration
    input_manager._buffer_times["ATTACK"] = buffer_time * 0.9
    input_manager.update()
    assert input_manager.is_buffered("ATTACK")

    # Check buffer just after expiration
    input_manager._buffer_times["ATTACK"] = -0.001
    input_manager.update()
    assert not input_manager.is_buffered("ATTACK")


def test_action_state_transitions() -> None:
    """Test all possible state transitions for an action."""
    input_manager = InputManager()
    input_manager.register_action("TEST")
    input_manager.bind_key("TEST", pygame.K_a)

    # Initial state
    assert not input_manager.is_pressed("TEST")
    assert not input_manager.is_held("TEST")
    assert not input_manager.is_released("TEST")

    # Press -> should be PRESSED
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a})
    input_manager.process_event(event)
    assert input_manager.is_pressed("TEST")
    assert input_manager.is_held("TEST")

    # Update -> should transition to HELD
    input_manager.update()
    assert not input_manager.is_pressed("TEST")
    assert input_manager.is_held("TEST")

    # Release -> should be RELEASED
    event = pygame.event.Event(pygame.KEYUP, {"key": pygame.K_a})
    input_manager.process_event(event)
    assert not input_manager.is_pressed("TEST")
    assert not input_manager.is_held("TEST")
    assert input_manager.is_released("TEST")

    # Update -> should clear state
    input_manager.update()
    assert not input_manager.is_pressed("TEST")
    assert not input_manager.is_held("TEST")
    assert not input_manager.is_released("TEST")
