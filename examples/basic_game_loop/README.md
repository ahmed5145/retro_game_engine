# Basic Game Loop Example

This example demonstrates the core game loop functionality of the Retro Game Engine. It shows how to:
- Create a window
- Set up a game loop
- Handle basic input
- Render graphics
- Monitor performance

## Running the Example

```bash
# From the project root
poetry install
poetry run python -m examples.basic_game_loop
```

## Code Overview

The example consists of a simple window that displays the current FPS and responds to keyboard input:

```python
from src.core import Window, WindowConfig
from src.core.game_loop import GameLoop, GameLoopConfig

class GameLoopExample:
    def __init__(self):
        # Create window
        self.window = Window(WindowConfig(
            title="Game Loop Example",
            width=800,
            height=600
        ))

        # Create game loop
        self.game_loop = GameLoop(
            update_func=self.update,
            render_func=self.render,
            config=GameLoopConfig(fps=60)
        )

    def update(self, dt: float):
        # Game logic here
        pass

    def render(self):
        # Rendering here
        self.window.clear()
        self.window.present()

    def run(self):
        self.game_loop.run()
```

## Key Concepts

### Game Loop

The game loop is the heart of any game. It consists of three main phases:
1. **Input Processing**: Handle user input
2. **Update**: Update game state
3. **Render**: Draw the current game state

### Fixed Time Step

The game loop uses a fixed time step for consistent physics and game logic:
```python
config = GameLoopConfig(
    fps=60,                    # Target 60 FPS
    fixed_time_step=1.0/60.0,  # Physics updates at 60Hz
    max_frame_time=0.25        # Prevent spiral of death
)
```

### Performance Monitoring

The game loop provides performance metrics:
- FPS (Frames Per Second)
- Frame time
- Update time
- Render time

## Next Steps

- Check out the [Sprite Animation](../sprite_test) example to learn about sprites
- See the [Input Handling](../input_test) example for more input features
- Read the [Game Loop API Reference](../../docs/api/game_loop.md)
