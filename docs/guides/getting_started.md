# Getting Started with Retro Game Engine

This guide will help you get started with creating your first game using the Retro Game Engine.

## Installation

1. First, make sure you have Python 3.9 or newer installed:
```bash
python --version
```

2. Install the engine using pip:
```bash
pip install retro-game-engine
```

Or using Poetry:
```bash
poetry add retro-game-engine
```

## Creating Your First Game

Here's a simple example that creates a window and displays a sprite:

```python
from src.core import Window, WindowConfig
from src.core.game_loop import GameLoop, GameLoopConfig
from src.core.sprite import Sprite, SpriteSheet, SpriteConfig

class MyGame:
    def __init__(self):
        # Create window
        window_config = WindowConfig(
            title="My First Game",
            width=320,
            height=240,
            scale=2
        )
        self.window = Window(window_config)

        # Load sprite
        self.sprite_sheet = SpriteSheet("player.png")
        self.sprite = Sprite(
            self.sprite_sheet,
            SpriteConfig(x=160, y=120)
        )

        # Create game loop
        self.game_loop = GameLoop(
            update_func=self.update,
            render_func=self.render,
            config=GameLoopConfig(fps=60)
        )

    def update(self, dt: float) -> None:
        # Update game state
        pass

    def render(self) -> None:
        # Clear screen
        self.window.clear()

        # Draw sprite
        self.sprite.draw(self.window.surface)

        # Update display
        self.window.present()

    def run(self) -> None:
        self.game_loop.run()

if __name__ == "__main__":
    game = MyGame()
    game.run()
```

## Next Steps

- Check out the [examples](../../examples/README.md) for more complex game implementations
- Read the [API Reference](../api/index.md) for detailed documentation
- Learn about the [Entity Component System](../guides/ecs.md)
- See [Best Practices](../guides/best_practices.md) for tips and guidelines

## Core Concepts

### GameLoop

The `GameLoop` class manages the game's main loop, handling:
- Window creation and management
- Scene management
- Input processing
- Frame timing

### Scene

Scenes represent different states or levels in your game:
- `update(delta_time)`: Called every frame to update game logic
- `draw(surface)`: Called every frame to render graphics
- `on_enter()`: Called when the scene becomes active
- `on_exit()`: Called when leaving the scene

### Sprite

The `Sprite` class handles image rendering with features like:
- Position and rotation
- Scale and flipping
- Animation support
- Collision detection

### Input

The `Input` class provides methods to handle:
- Keyboard input
- Mouse input
- Gamepad support

### Physics

The physics system includes:
- Collision detection
- Gravity simulation
- Velocity and acceleration

## Common Issues

### Game runs slowly
- Check your sprite sizes and number of objects
- Use sprite sheets for animations
- Implement object pooling for multiple objects

### Collision detection issues
- Ensure sprite hitboxes are properly set
- Use debug rendering to visualize collisions
- Check for proper object cleanup

### Memory usage grows over time
- Properly dispose of unused resources
- Clear sprite references when removing objects
- Use the scene cleanup methods

## Getting Help

If you run into issues:
1. Check the documentation
2. Search existing GitHub issues

3. Open a new GitHub issue

Happy game development! 🎮
