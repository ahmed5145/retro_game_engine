# Window

The window system handles the game's display and provides basic rendering functionality.

## Window

```python
class Window:
    def __init__(self, config: WindowConfig):
        """Initialize the window with the given configuration."""
```

### Methods

#### clear()
```python
def clear(self, color: Tuple[int, int, int] = (0, 0, 0)) -> None
```
Clear the window with the specified color (default: black).

#### present()
```python
def present(self) -> None
```
Scale and present the internal surface to the display.

#### set_title()
```python
def set_title(self, title: str) -> None
```
Set the window title.

#### toggle_fullscreen()
```python
def toggle_fullscreen(self) -> None
```
Toggle fullscreen mode.

### Properties

#### surface
```python
@property
def surface(self) -> pygame.Surface
```
Get the internal rendering surface.

#### display_surface
```python
@property
def display_surface(self) -> pygame.Surface
```
Get the scaled display surface.

## WindowConfig

Configuration options for the game window.

```python
@dataclass
class WindowConfig:
    title: str
    width: int
    height: int
    scale: int = 1
    vsync: bool = True
    fullscreen: bool = False
```

### Fields
- `title`: Window title
- `width`: Window width in pixels
- `height`: Window height in pixels
- `scale`: Integer scaling factor (default: 1)
- `vsync`: Enable vertical synchronization (default: True)
- `fullscreen`: Start in fullscreen mode (default: False)

## Example Usage

```python
from src.core import Window, WindowConfig

# Create window configuration
config = WindowConfig(
    title="My Game",
    width=320,
    height=240,
    scale=2,
    vsync=True
)

# Create window
window = Window(config)

# Game loop
while True:
    # Clear window
    window.clear((100, 149, 237))  # Cornflower blue

    # Draw game objects to window.surface
    # ...

    # Update display
    window.present()
```

## Best Practices

1. **Resolution**: Choose a base resolution that matches your game's style:
   - 256×224: NES/Master System style
   - 320×240: SNES/Genesis style
   - 640×480: Early PC style

2. **Scaling**: Use integer scaling to maintain pixel-perfect rendering:
```python
config = WindowConfig(
    width=320,
    height=240,
    scale=2  # Creates a 640×480 window
)
```

3. **VSync**: Enable VSync to prevent screen tearing:
```python
config = WindowConfig(
    # ...
    vsync=True
)
```

4. **Surface Management**: Draw to the internal surface, not the display surface:
```python
# Correct
window.surface.blit(sprite, position)

# Incorrect
window.display_surface.blit(sprite, position)
```

## Common Issues

### Blurry Graphics
- Ensure you're using integer scaling values
- Draw to the internal surface, not the display surface
- Avoid floating-point positions for sprites

### Performance Issues
- Use hardware acceleration when available
- Batch similar draw operations
- Minimize surface locking/unlocking
- Consider using display lists for static elements

### Fullscreen Problems
- Handle window resize events properly
- Save/restore window state when toggling fullscreen
- Consider different scaling modes for fullscreen
