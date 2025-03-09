# Sprite System

The sprite system handles loading, managing, and rendering game sprites and animations.

## Sprite

```python
class Sprite:
    def __init__(
        self,
        sprite_sheet: SpriteSheet,
        config: Optional[SpriteConfig] = None
    ):
        """Initialize a sprite with the given sprite sheet and configuration."""
```

### Methods

#### set_frame()
```python
def set_frame(self, frame_index: int) -> None
```
Set the current frame of the sprite.

#### draw()
```python
def draw(self, surface: pygame.Surface) -> None
```
Draw the sprite to the given surface.

## SpriteSheet

```python
class SpriteSheet:
    def __init__(self, texture_path: str):
        """Load a sprite sheet from the given image file."""
```

### Methods

#### add_frame()
```python
def add_frame(self, frame: SpriteFrame) -> int
```
Add a frame to the sprite sheet. Returns the frame index.

#### add_frames_grid()
```python
def add_frames_grid(
    self,
    frame_width: int,
    frame_height: int,
    margin: int = 0,
    spacing: int = 0
) -> None
```
Add frames from a grid layout. Useful for uniform sprite sheets.

## SpriteFrame

Configuration for a single frame in a sprite sheet.

```python
@dataclass
class SpriteFrame:
    x: int
    y: int
    width: int
    height: int
```

### Fields
- `x`: X position of the frame in the sprite sheet
- `y`: Y position of the frame in the sprite sheet
- `width`: Width of the frame
- `height`: Height of the frame

## SpriteConfig

Configuration for sprite rendering.

```python
@dataclass
class SpriteConfig:
    x: float = 0.0
    y: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    rotation: int = 0  # Degrees, must be multiple of 90
    flip_x: bool = False
    flip_y: bool = False
    alpha: int = 255
    z_index: int = 0
```

### Fields
- `x`: X position for rendering
- `y`: Y position for rendering
- `scale_x`: Horizontal scale factor
- `scale_y`: Vertical scale factor
- `rotation`: Rotation in degrees (must be multiple of 90)
- `flip_x`: Horizontally flip the sprite
- `flip_y`: Vertically flip the sprite
- `alpha`: Transparency (0-255)
- `z_index`: Rendering order

## Example Usage

### Loading a Sprite Sheet
```python
from src.core.sprite import SpriteSheet, SpriteFrame

# Load sprite sheet
sheet = SpriteSheet("player.png")

# Add individual frames
sheet.add_frame(SpriteFrame(0, 0, 32, 32))  # Idle
sheet.add_frame(SpriteFrame(32, 0, 32, 32))  # Walk 1
sheet.add_frame(SpriteFrame(64, 0, 32, 32))  # Walk 2

# Or add frames from a grid
sheet.add_frames_grid(
    frame_width=32,
    frame_height=32,
    margin=1,
    spacing=1
)
```

### Creating and Using Sprites
```python
from src.core.sprite import Sprite, SpriteConfig

# Create sprite configuration
config = SpriteConfig(
    x=100,
    y=100,
    scale_x=2.0,
    scale_y=2.0,
    flip_x=False
)

# Create sprite
sprite = Sprite(sheet, config)

# Set current frame
sprite.set_frame(1)  # Show walking frame

# Draw sprite
sprite.draw(window.surface)
```

## Best Practices

1. **Sprite Sheet Organization**:
   - Group related frames together
   - Use consistent frame sizes when possible
   - Add padding to prevent bleeding
   - Consider power-of-two textures for compatibility

2. **Memory Management**:
   - Share sprite sheets between similar sprites
   - Unload unused sprite sheets
   - Use texture atlases for small sprites

3. **Animation**:
   - Use frame indices for animation sequences
   - Consider frame timing in animation loops
   - Implement state machines for complex animations

4. **Performance**:
   - Batch similar sprites together
   - Use sprite culling for off-screen objects
   - Minimize sprite sheet switches

## Common Issues

### Texture Bleeding
- Add padding between frames
- Use texture coordinates slightly inset from edges
- Ensure power-of-two textures when required

### Performance
- Too many individual sprites
- Frequent sprite sheet switching
- Excessive scaling or rotation

### Memory Usage
- Large sprite sheets
- Duplicate sprite sheet loading
- Unused frames in memory

### Visual Artifacts
- Incorrect transparency
- Scaling artifacts
- Rotation limitations
