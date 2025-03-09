# Input System

The input system provides a unified interface for handling keyboard, mouse, and gamepad input.

## InputManager

```python
class InputManager:
    def __init__(self):
        """Initialize the input manager."""
```

### Methods

#### update()
```python
def update(self) -> None
```
Update input state for the current frame. Should be called once per frame.

#### is_key_pressed()
```python
def is_key_pressed(self, key: int) -> bool
```
Check if a key is currently being held down.

#### is_key_just_pressed()
```python
def is_key_just_pressed(self, key: int) -> bool
```
Check if a key was just pressed this frame.

#### is_key_just_released()
```python
def is_key_just_released(self, key: int) -> bool
```
Check if a key was just released this frame.

#### get_mouse_position()
```python
def get_mouse_position(self) -> Tuple[int, int]
```
Get the current mouse position as (x, y).

#### is_mouse_button_pressed()
```python
def is_mouse_button_pressed(self, button: int) -> bool
```
Check if a mouse button is currently being held down.

#### is_mouse_button_just_pressed()
```python
def is_mouse_button_just_pressed(self, button: int) -> bool
```
Check if a mouse button was just pressed this frame.

#### is_mouse_button_just_released()
```python
def is_mouse_button_just_released(self, button: int) -> bool
```
Check if a mouse button was just released this frame.

## Key Constants

Common keyboard key constants:

```python
from pygame import K_a, K_b, K_c  # Letters
from pygame import K_0, K_1, K_2  # Numbers
from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN  # Arrows
from pygame import K_SPACE, K_RETURN, K_ESCAPE  # Special keys
```

## Mouse Button Constants

Mouse button constants:

```python
from pygame import BUTTON_LEFT, BUTTON_MIDDLE, BUTTON_RIGHT
```

## Example Usage

### Basic Input Handling
```python
from src.core.input import InputManager
from pygame import K_SPACE, K_LEFT, K_RIGHT, BUTTON_LEFT

# Create input manager
input_manager = InputManager()

def update():
    # Update input state
    input_manager.update()

    # Check keyboard input
    if input_manager.is_key_pressed(K_LEFT):
        move_left()
    elif input_manager.is_key_pressed(K_RIGHT):
        move_right()

    # Check for jump (only on initial press)
    if input_manager.is_key_just_pressed(K_SPACE):
        jump()

    # Get mouse position
    mouse_x, mouse_y = input_manager.get_mouse_position()

    # Check mouse input
    if input_manager.is_mouse_button_just_pressed(BUTTON_LEFT):
        shoot(mouse_x, mouse_y)
```

### Advanced Input Handling
```python
# Checking key combinations
if (input_manager.is_key_pressed(K_LCTRL) and
    input_manager.is_key_just_pressed(K_s)):
    save_game()

# Double click detection
if (input_manager.is_mouse_button_just_pressed(BUTTON_LEFT) and
    time.time() - last_click_time < DOUBLE_CLICK_TIME):
    handle_double_click()

# Mouse movement
prev_x, prev_y = last_mouse_pos
curr_x, curr_y = input_manager.get_mouse_position()
mouse_delta_x = curr_x - prev_x
mouse_delta_y = curr_y - prev_y
```

## Best Practices

1. **Input State Management**:
   - Call `update()` once per frame
   - Use `is_key_just_pressed()` for one-time actions
   - Use `is_key_pressed()` for continuous actions

2. **Input Mapping**:
   - Define input constants at the start
   - Consider creating an input configuration system
   - Support key rebinding

3. **Mouse Input**:
   - Handle both relative and absolute positions
   - Consider screen scaling when using positions
   - Implement proper double-click detection

4. **Performance**:
   - Cache input states when needed
   - Avoid checking input multiple times per frame
   - Use efficient key combination detection

## Common Issues

### Input Lag
- Missing `update()` calls
- Processing input multiple times
- Heavy processing in input handlers

### Missed Input
- Not using `is_key_just_pressed()`
- Incorrect frame timing
- Input buffer overflow

### Key Combinations
- Order dependency issues
- Race conditions
- Missing key release events

### Mouse Position
- Incorrect coordinate space
- Screen scaling issues
- Resolution independence problems
