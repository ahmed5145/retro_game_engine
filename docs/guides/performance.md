# Performance Tips

This guide provides detailed strategies for optimizing your game's performance with the Retro Game Engine.

## Profiling and Monitoring

### Built-in Tools
- Use `GameLoop.performance_metrics` to monitor:
  - Frame rate (FPS)
  - Frame time
  - Update time
  - Render time
  - Physics time

### External Tools
- Python profilers (cProfile, line_profiler)
- Memory profilers (memory_profiler)
- System monitoring tools

## Rendering Optimization

### Sprite Management
```python
# Bad: Creating sprites individually
for i in range(100):
    sprite = Sprite(sheet, SpriteConfig(x=i*32, y=100))
    renderer.add_sprite(sprite)

# Good: Using sprite batching
sprite_batch = []
for i in range(100):
    sprite = Sprite(sheet, SpriteConfig(x=i*32, y=100))
    sprite_batch.append(sprite)
renderer.add_sprites(sprite_batch)
```

### Z-Index Organization
```python
# Define clear z-index ranges
Z_BACKGROUND = 0
Z_TERRAIN = 100
Z_OBJECTS = 200
Z_CHARACTERS = 300
Z_PARTICLES = 400
Z_UI = 500
```

### View Culling
```python
def is_visible(sprite: Sprite, camera: Rect) -> bool:
    sprite_rect = sprite.get_bounds()
    return camera.colliderect(sprite_rect)

# Only render visible sprites
visible_sprites = [s for s in sprites if is_visible(s, camera_rect)]
renderer.render(visible_sprites)
```

## Memory Management

### Object Pooling
```python
class BulletPool:
    def __init__(self, size: int):
        self.bullets = [Bullet() for _ in range(size)]
        self.active = set()

    def get_bullet(self) -> Optional[Bullet]:
        for bullet in self.bullets:
            if bullet not in self.active:
                self.active.add(bullet)
                return bullet
        return None

    def return_bullet(self, bullet: Bullet):
        self.active.remove(bullet)
        bullet.reset()
```

### Asset Management
```python
class AssetManager:
    def __init__(self):
        self.cache = {}
        self.reference_counts = {}

    def load_asset(self, path: str) -> Any:
        if path not in self.cache:
            self.cache[path] = load_file(path)
            self.reference_counts[path] = 0
        self.reference_counts[path] += 1
        return self.cache[path]

    def unload_asset(self, path: str):
        self.reference_counts[path] -= 1
        if self.reference_counts[path] <= 0:
            del self.cache[path]
            del self.reference_counts[path]
```

## Physics Optimization

### Spatial Partitioning
```python
class Grid:
    def __init__(self, cell_size: int):
        self.cell_size = cell_size
        self.cells = {}

    def add_object(self, obj: GameObject):
        cell_x = obj.x // self.cell_size
        cell_y = obj.y // self.cell_size
        if (cell_x, cell_y) not in self.cells:
            self.cells[(cell_x, cell_y)] = set()
        self.cells[(cell_x, cell_y)].add(obj)

    def get_nearby(self, obj: GameObject) -> Set[GameObject]:
        cell_x = obj.x // self.cell_size
        cell_y = obj.y // self.cell_size
        nearby = set()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                cell = (cell_x + dx, cell_y + dy)
                if cell in self.cells:
                    nearby.update(self.cells[cell])
        return nearby
```

### Collision Optimization
```python
def check_collisions(objects: List[GameObject], grid: Grid):
    for obj in objects:
        # Only check nearby objects
        nearby = grid.get_nearby(obj)
        for other in nearby:
            if obj != other and obj.collides_with(other):
                handle_collision(obj, other)
```

## Input Handling

### Event Buffering
```python
class InputBuffer:
    def __init__(self, buffer_time: float = 0.1):
        self.buffer_time = buffer_time
        self.buffer = []

    def add_input(self, action: str, timestamp: float):
        self.buffer.append((action, timestamp))
        self.cleanup_old_inputs(timestamp)

    def cleanup_old_inputs(self, current_time: float):
        self.buffer = [(a, t) for a, t in self.buffer
                      if current_time - t <= self.buffer_time]

    def has_input(self, action: str, current_time: float) -> bool:
        return any(a == action and current_time - t <= self.buffer_time
                  for a, t in self.buffer)
```

## Audio Optimization

### Sound Pooling
```python
class SoundPool:
    def __init__(self, sound_path: str, pool_size: int = 4):
        self.sounds = [load_sound(sound_path) for _ in range(pool_size)]
        self.current = 0

    def play(self):
        sound = self.sounds[self.current]
        self.current = (self.current + 1) % len(self.sounds)
        sound.play()
```

## Scene Management

### Loading Optimization
```python
class Scene:
    def __init__(self):
        self.loaded = False
        self.assets = set()

    async def load(self):
        if not self.loaded:
            await self.preload_assets()
            self.setup_scene()
            self.loaded = True

    def unload(self):
        if self.loaded:
            self.cleanup_assets()
            self.loaded = False
```

## Debugging Performance

### Performance Logging
```python
class PerformanceLogger:
    def __init__(self):
        self.timings = {}
        self.samples = 100

    @contextmanager
    def measure(self, name: str):
        start = time.perf_counter()
        yield
        end = time.perf_counter()
        if name not in self.timings:
            self.timings[name] = []
        self.timings[name].append(end - start)
        if len(self.timings[name]) > self.samples:
            self.timings[name].pop(0)

    def get_average(self, name: str) -> float:
        return sum(self.timings[name]) / len(self.timings[name])
```

## Common Performance Issues

### Memory Leaks
- Event listeners not being removed
- Circular references between objects
- Cached assets not being cleared
- Texture memory not being freed

### CPU Bottlenecks
- Too many active physics objects
- Inefficient collision detection
- Complex particle systems
- Unoptimized rendering loops

### GPU Bottlenecks
- Too many draw calls
- Large textures
- Complex shaders
- Excessive screen effects
