"""Tests for the input system."""
from typing import Dict, Set
import time
import pytest
import pygame
from src.core.input import InputManager, InputAction, InputState, InputBinding

def test_input_manager_initialization() -> None:
    """Test that input manager is properly initialized."""
    input_manager = InputManager()
    assert len(input_manager.actions) == 0
    assert len(input_manager.bindings) == 0
    assert len(input_manager.state) == 0

def test_action_registration() -> None:
    """Test that actions can be registered and retrieved."""
    input_manager = InputManager()

    # Register some actions
    input_manager.register_action("MOVE_LEFT")
    input_manager.register_action("MOVE_RIGHT")
    input_manager.register_action("JUMP")

    assert "MOVE_LEFT" in input_manager.actions
    assert "MOVE_RIGHT" in input_manager.actions
    assert "JUMP" in input_manager.actions

    # Try to register duplicate action
    with pytest.raises(ValueError):
        input_manager.register_action("MOVE_LEFT")

def test_key_binding() -> None:
    """Test that keys can be bound to actions."""
    input_manager = InputManager()

    # Register and bind actions
    input_manager.register_action("MOVE_LEFT")
    input_manager.register_action("MOVE_RIGHT")

    input_manager.bind_key("MOVE_LEFT", pygame.K_LEFT)
    input_manager.bind_key("MOVE_RIGHT", pygame.K_RIGHT)

    assert input_manager.get_bindings("MOVE_LEFT") == {pygame.K_LEFT}
    assert input_manager.get_bindings("MOVE_RIGHT") == {pygame.K_RIGHT}

    # Test binding multiple keys to same action
    input_manager.bind_key("MOVE_LEFT", pygame.K_a)
    assert input_manager.get_bindings("MOVE_LEFT") == {pygame.K_LEFT, pygame.K_a}

def test_input_state() -> None:
    """Test input state tracking."""
    input_manager = InputManager()
    input_manager.register_action("JUMP")
    input_manager.bind_key("JUMP", pygame.K_SPACE)

    # Simulate key press
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})
    input_manager.process_event(event)

    assert input_manager.is_pressed("JUMP")
    assert input_manager.is_held("JUMP")
    assert not input_manager.is_released("JUMP")

    # Simulate key release
    event = pygame.event.Event(pygame.KEYUP, {'key': pygame.K_SPACE})
    input_manager.process_event(event)

    assert not input_manager.is_pressed("JUMP")
    assert not input_manager.is_held("JUMP")
    assert input_manager.is_released("JUMP")

    # State should be cleared after update
    input_manager.update()
    assert not input_manager.is_pressed("JUMP")
    assert not input_manager.is_held("JUMP")
    assert not input_manager.is_released("JUMP")

def test_input_buffering() -> None:
    """Test input buffering system."""
    input_manager = InputManager()
    input_manager.register_action("ATTACK", buffer_time=0.1)  # 100ms buffer
    input_manager.bind_key("ATTACK", pygame.K_x)

    # Simulate key press
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_x})
    input_manager.process_event(event)

    assert input_manager.is_pressed("ATTACK")
    assert input_manager.is_buffered("ATTACK")

    # Buffer should remain active for buffer_time
    input_manager.update()  # First frame
    assert not input_manager.is_pressed("ATTACK")
    assert input_manager.is_buffered("ATTACK")

    # Simulate buffer expiration
    input_manager._buffer_times["ATTACK"] = 0  # Force buffer expiration
    input_manager.update()
    assert not input_manager.is_buffered("ATTACK")

def test_action_mapping() -> None:
    """Test action mapping system."""
    input_manager = InputManager()

    # Create a mapping
    mapping = {
        "MOVE_LEFT": [pygame.K_LEFT, pygame.K_a],
        "MOVE_RIGHT": [pygame.K_RIGHT, pygame.K_d],
        "JUMP": [pygame.K_SPACE, pygame.K_w]
    }

    input_manager.load_mapping(mapping)

    # Verify all actions and bindings are set up
    for action, keys in mapping.items():
        assert action in input_manager.actions
        assert input_manager.get_bindings(action) == set(keys)

def test_error_handling() -> None:
    """Test error handling for invalid actions and operations."""
    input_manager = InputManager()
    
    # Test various invalid operations
    with pytest.raises(ValueError):
        input_manager.bind_key("NONEXISTENT", pygame.K_a)
        
    with pytest.raises(ValueError):
        input_manager.is_pressed("NONEXISTENT")
        
    with pytest.raises(ValueError):
        input_manager.is_held("NONEXISTENT")
        
    with pytest.raises(ValueError):
        input_manager.is_released("NONEXISTENT")
        
    with pytest.raises(ValueError):
        input_manager.is_buffered("NONEXISTENT")
        
    with pytest.raises(ValueError):
        input_manager.clear_bindings("NONEXISTENT")

def test_binding_management() -> None:
    """Test comprehensive binding management."""
    input_manager = InputManager()
    input_manager.register_action("TEST")
    
    # Add multiple bindings
    input_manager.bind_key("TEST", pygame.K_a)
    input_manager.bind_key("TEST", pygame.K_b)
    input_manager.bind_key("TEST", pygame.K_c)
    
    assert len(input_manager.get_bindings("TEST")) == 3
    
    # Clear bindings
    input_manager.clear_bindings("TEST")
    assert len(input_manager.get_bindings("TEST")) == 0
    
    # Test that events for cleared bindings don't trigger the action
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a})
    input_manager.process_event(event)
    assert not input_manager.is_pressed("TEST")

def test_multiple_key_bindings() -> None:
    """Test handling multiple key bindings for the same action."""
    input_manager = InputManager()
    input_manager.register_action("JUMP")
    
    # Bind multiple keys
    input_manager.bind_key("JUMP", pygame.K_SPACE)
    input_manager.bind_key("JUMP", pygame.K_w)
    input_manager.bind_key("JUMP", pygame.K_UP)
    
    # Test each key triggers the action
    for key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
        event = pygame.event.Event(pygame.KEYDOWN, {'key': key})
        input_manager.process_event(event)
        assert input_manager.is_pressed("JUMP")
        input_manager.update()

def test_simultaneous_keys() -> None:
    """Test handling multiple keys pressed simultaneously."""
    input_manager = InputManager()
    input_manager.register_action("MOVE_LEFT")
    input_manager.register_action("MOVE_RIGHT")
    
    input_manager.bind_key("MOVE_LEFT", pygame.K_LEFT)
    input_manager.bind_key("MOVE_RIGHT", pygame.K_RIGHT)
    
    # Press both keys
    event1 = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
    event2 = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
    
    input_manager.process_event(event1)
    input_manager.process_event(event2)
    
    assert input_manager.is_held("MOVE_LEFT")
    assert input_manager.is_held("MOVE_RIGHT")

def test_buffer_timing_precision() -> None:
    """Test precise timing of input buffer system."""
    input_manager = InputManager()
    buffer_time = 0.1  # 100ms
    input_manager.register_action("ATTACK", buffer_time=buffer_time)
    input_manager.bind_key("ATTACK", pygame.K_x)
    
    # Simulate key press
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_x})
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
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a})
    input_manager.process_event(event)
    assert input_manager.is_pressed("TEST")
    assert input_manager.is_held("TEST")
    
    # Update -> should transition to HELD
    input_manager.update()
    assert not input_manager.is_pressed("TEST")
    assert input_manager.is_held("TEST")
    
    # Release -> should be RELEASED
    event = pygame.event.Event(pygame.KEYUP, {'key': pygame.K_a})
    input_manager.process_event(event)
    assert not input_manager.is_pressed("TEST")
    assert not input_manager.is_held("TEST")
    assert input_manager.is_released("TEST")
    
    # Update -> should clear state
    input_manager.update()
    assert not input_manager.is_pressed("TEST")
    assert not input_manager.is_held("TEST")
    assert not input_manager.is_released("TEST")
