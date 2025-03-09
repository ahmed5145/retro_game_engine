# Sprite Renderer

The sprite renderer system handles efficient rendering of multiple sprites with z-ordering and batching support.

## SpriteRenderer

```python
class SpriteRenderer:
    def __init__(self) -> None:
        """Initialize the sprite renderer."""
```

### Methods

#### add_sprite()
```python
def add_sprite(self, sprite: Sprite) -> None
```
Add a sprite to be rendered.

#### remove_sprite()
```python
def remove_sprite(self, sprite: Sprite) -> None
```
Remove a sprite from rendering.

#### clear()
```python
def clear(self) -> None
```
Remove all sprites from the renderer.

#### render()
```python
def render(self, surface: pygame.Surface) -> None
```
Render all sprites in order of z-index.

## Best Practices

1. **Batching**:
   - Group sprites with similar z-indices together
   - Add sprites in bulk when possible
   - Clear sprites when changing scenes

2. **Performance**:
   - Remove unused sprites promptly
   - Use appropriate z-indices to minimize state changes
   - Consider sprite atlases for large numbers of sprites

3. **Z-Index Management**:
   - Use consistent z-index ranges for different types of objects
   - Leave gaps between z-indices for future additions
   - Document z-index ranges in your game

## Common Issues

### Performance
- Too many individual sprite additions/removals
- Excessive z-index changes
- Large number of unique textures

### Memory Usage
- Not removing sprites when they're no longer needed
- Keeping references to removed sprites
- Memory leaks from circular references

### Rendering Artifacts
- Z-index conflicts
- Sprite flickering
- Incorrect sprite ordering
