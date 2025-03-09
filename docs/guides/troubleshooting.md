# Troubleshooting Guide

This guide helps you diagnose and fix common issues when developing with the Retro Game Engine.

## Installation Issues

### Poetry Installation
```
Error: Could not find a version that satisfies the requirement retro-game-engine
```
- Check Python version (requires 3.9+)
- Update Poetry to latest version
- Clear Poetry cache: `poetry cache clear . --all`

### Package Dependencies
```
Error: Dependency resolution failed
```
- Update `pyproject.toml` with correct versions
- Check for conflicting dependencies
- Try `poetry update` to resolve conflicts

## Runtime Issues

### Game Loop

#### Low Frame Rate
```python
# Check performance metrics
metrics = game_loop.performance_metrics
print(f"FPS: {metrics.fps}")
print(f"Frame Time: {metrics.frame_time}ms")
print(f"Update Time: {metrics.update_time}ms")
print(f"Render Time: {metrics.render_time}ms")
```

**Solutions:**
- Profile code for bottlenecks
- Reduce number of active objects
- Implement object pooling
- Use sprite batching

#### Fixed Update Issues
```python
# Common mistake: Variable time step physics
def update(dt):
    player.x += velocity * dt  # Wrong for physics!

# Correct: Fixed time step in physics update
def fixed_update(dt):
    player.x += velocity * dt  # Correct
```

### Rendering

#### Sprite Issues
```python
# Debug sprite bounds
def render():
    for sprite in sprites:
        pygame.draw.rect(
            surface,
            (255, 0, 0),
            sprite.get_bounds(),
            1
        )
```

**Common Problems:**
- Incorrect sprite sheet coordinates
- Missing texture references
- Z-index conflicts
- Transform issues

#### Screen Tearing
```python
# Enable VSync
window_config = WindowConfig(
    title="My Game",
    width=800,
    height=600,
    vsync=True  # Important!
)
```

### Input

#### Input Delay
```python
# Debug input timing
def update():
    if input_manager.is_key_just_pressed(K_SPACE):
        print(f"Jump latency: {time.perf_counter() - last_frame_time}")
```

**Solutions:**
- Use `is_key_just_pressed` for immediate actions
- Implement input buffering
- Check for input every frame
- Reduce processing in input handlers

#### Input Not Registering
```python
# Common mistake: Not updating input state
def update():
    if pygame.key.get_pressed()[K_SPACE]:  # Wrong!
        player.jump()

# Correct: Using input manager
def update():
    input_manager.update()  # Important!
    if input_manager.is_key_pressed(K_SPACE):
        player.jump()
```

### Physics

#### Collision Detection
```python
# Debug collision boxes
def render():
    for obj in physics_objects:
        bounds = obj.get_collision_bounds()
        pygame.draw.rect(surface, (0, 255, 0), bounds, 1)
```

**Common Issues:**
- Objects passing through each other
- Stuck in walls
- Jittery movement
- Missing collisions

#### Physics Glitches
```python
# Check for extreme velocities
def update():
    for obj in physics_objects:
        if obj.velocity.magnitude() > 1000:
            print(f"Warning: High velocity on {obj}")
```

### Memory

#### Memory Leaks
```python
# Track object counts
def debug_memory():
    print(f"Sprites: {len(sprite_renderer.sprites)}")
    print(f"Physics Objects: {len(physics_world.objects)}")
    print(f"Event Listeners: {len(event_manager.listeners)}")
```

**Solutions:**
- Remove unused sprites
- Clear event listeners
- Implement proper cleanup
- Use weak references

#### Resource Management
```python
# Debug asset loading
def load_scene():
    print(f"Before: {len(asset_manager.cache)}")
    scene.load()
    print(f"After: {len(asset_manager.cache)}")
```

### Audio

#### Sound Not Playing
```python
# Check audio system state
def debug_audio():
    print(f"Mixer initialized: {pygame.mixer.get_init()}")
    print(f"Sound volume: {audio_manager.sound_volume}")
    print(f"Active channels: {pygame.mixer.get_num_busy()}")
```

#### Audio Lag
```python
# Monitor audio buffer
def update():
    if pygame.mixer.get_busy():
        print(f"Queue size: {audio_manager.get_queue_size()}")
```

## Development Tools

### Debugging Tools
```python
class DebugInfo:
    def __init__(self):
        self.show_fps = True
        self.show_collisions = True
        self.show_sprites = True

    def render(self, surface):
        if self.show_fps:
            render_fps()
        if self.show_collisions:
            render_collision_boxes()
        if self.show_sprites:
            render_sprite_bounds()
```

### Performance Monitoring
```python
class PerformanceMonitor:
    def __init__(self):
        self.frame_times = []
        self.max_samples = 60

    def update(self, dt):
        self.frame_times.append(dt)
        if len(self.frame_times) > self.max_samples:
            self.frame_times.pop(0)

    def get_average_fps(self):
        return 1.0 / (sum(self.frame_times) / len(self.frame_times))
```

## Common Error Messages

### ImportError
```
ImportError: No module named 'retro_game_engine'
```
- Check Python path
- Verify installation
- Check virtual environment

### TypeError
```
TypeError: 'NoneType' object is not subscriptable
```
- Check for uninitialized objects
- Verify asset loading
- Debug object lifecycle

### ValueError
```
ValueError: Invalid sprite frame index
```
- Verify sprite sheet configuration
- Check animation sequences
- Debug frame calculations

## Getting Help

### Debug Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Sprite loaded: %s", sprite_path)
logger.warning("High frame time: %f", frame_time)
logger.error("Failed to load asset: %s", asset_path)
```

### Support Resources
- Check documentation
- Search GitHub issues
- Join Discord community
- Post on forums

### Reporting Issues
- Include error messages
- Provide minimal example
- List system information
- Share relevant logs
