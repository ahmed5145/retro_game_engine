# Game Loop

The game loop is the core component that drives your game's execution. It manages the timing of updates and rendering, ensuring consistent gameplay regardless of the system's performance.

## GameLoop

```python
class GameLoop:
    def __init__(
        self,
        update_func: Callable[[float], None],
        render_func: Callable[[], None],
        config: Optional[GameLoopConfig] = None
    ) -> None
```

### Parameters
- `update_func`: Function called each frame to update game state. Takes delta time in seconds.
- `render_func`: Function called each frame to render the game.
- `config`: Optional configuration for the game loop.

### Methods

#### run()
```python
def run(self) -> None
```
Start the game loop. This will run until `stop()` is called.

#### stop()
```python
def stop(self) -> None
```
Stop the game loop.

#### run_one_frame()
```python
def run_one_frame(self) -> None
```
Process a single frame of the game loop.

### Properties

#### average_fps
```python
@property
def average_fps(self) -> float
```
Get the current average FPS over the last `fps_sample_size` frames.

#### running
```python
@property
def running(self) -> bool
```
Check if the game loop is currently running.

## GameLoopConfig

Configuration options for the game loop.

```python
@dataclass
class GameLoopConfig:
    fps: int = 60
    fixed_time_step: float = 1.0 / 60.0
    max_frame_time: float = 0.25
    fps_sample_size: int = 60
```

### Fields
- `fps`: Target frames per second (default: 60)
- `fixed_time_step`: Time step for physics/fixed updates (default: 1/60 second)
- `max_frame_time`: Maximum time to process in a single frame (default: 0.25 seconds)
- `fps_sample_size`: Number of frames to sample for FPS calculation (default: 60)

## PerformanceMetrics

Performance monitoring data for the game loop.

```python
@dataclass
class PerformanceMetrics:
    fps: float = 0.0
    frame_time: float = 0.0
    min_frame_time: float = float("inf")
    max_frame_time: float = 0.0
    avg_frame_time: float = 0.0
    fixed_update_time: float = 0.0
    update_time: float = 0.0
    render_time: float = 0.0
    idle_time: float = 0.0
```

### Fields
- `fps`: Current frames per second
- `frame_time`: Time taken for the last frame
- `min_frame_time`: Minimum frame time recorded
- `max_frame_time`: Maximum frame time recorded
- `avg_frame_time`: Average frame time
- `fixed_update_time`: Time spent in fixed update
- `update_time`: Time spent in update
- `render_time`: Time spent rendering
- `idle_time`: Time spent idle

## Example Usage

```python
from src.core.game_loop import GameLoop, GameLoopConfig

# Create configuration
config = GameLoopConfig(
    fps=60,
    fixed_time_step=1/60,
    max_frame_time=0.25
)

# Define update and render functions
def update(dt: float) -> None:
    # Update game state
    pass

def render() -> None:
    # Render game
    pass

# Create and run game loop
game_loop = GameLoop(update, render, config)
game_loop.run()
```

## Best Practices

1. **Fixed Time Step**: Use the fixed time step for physics and gameplay logic that needs to be consistent.

2. **Frame Independent Movement**: Always multiply movement by delta time:
```python
def update(dt: float) -> None:
    position.x += velocity.x * dt
    position.y += velocity.y * dt
```

3. **Performance Monitoring**: Monitor the performance metrics to identify bottlenecks:
```python
def update(dt: float) -> None:
    if game_loop.average_fps < 55:
        # Reduce visual effects or complexity
        pass
```

4. **Maximum Frame Time**: Set a reasonable `max_frame_time` to prevent the "spiral of death" when the game falls behind.

## Common Issues

### Low FPS
- Check for expensive operations in the update or render functions
- Consider using sprite batching
- Profile the game using the performance metrics

### Inconsistent Physics
- Ensure physics calculations are done in the fixed time step
- Don't modify physics state directly in the render function
- Use interpolation for smooth rendering between physics updates

### High CPU Usage
- Use frame limiting when appropriate
- Don't perform unnecessary calculations each frame
- Consider using spatial partitioning for large numbers of objects
