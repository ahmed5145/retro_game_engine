# Getting Started with Retro Game Engine

Welcome to Retro Game Engine! This guide will help you get up and running with your first game project.

## Prerequisites

Before you begin, ensure you have:

- Python 3.8 or higher installed
- Poetry (dependency management tool)
- Basic understanding of Python programming
- A text editor or IDE (we recommend VS Code)

## Installation

1. Install the Retro Game Engine using pip:
```bash
pip install retro-game-engine
```

2. Or install using Poetry:
```bash
poetry add retro-game-engine
```

## Your First Game

Let's create a simple game with a bouncing sprite!

1. Create a new directory for your project:
```bash
mkdir my-first-game
cd my-first-game
```

2. Create a new Python file `main.py`:
```python
from retro_game_engine import GameLoop, Scene, Sprite
from retro_game_engine.core.input import Input
from retro_game_engine.core.physics import Physics

class MainScene(Scene):
    def __init__(self):
        super().__init__()
        # Create a bouncing sprite
        self.sprite = Sprite("assets/ball.png")
        self.sprite.config.x = 400
        self.sprite.config.y = 300
        self.velocity_y = 0
        self.gravity = 0.5

    def update(self, delta_time: float):
        # Apply gravity
        self.velocity_y += self.gravity
        self.sprite.config.y += self.velocity_y

        # Bounce when hitting bottom of screen
        if self.sprite.config.y > 550:
            self.sprite.config.y = 550
            self.velocity_y = -15

    def draw(self, surface):
        self.sprite.draw(surface)

def main():
    game = GameLoop()
    game.window_title = "My First Game"
    game.window_width = 800
    game.window_height = 600
    game.current_scene = MainScene()
    game.run()

if __name__ == "__main__":
    main()
```

3. Create an `assets` directory and add a ball image (you can use any small PNG file).

4. Run your game:
```bash
python main.py
```

Congratulations! You've created your first game with Retro Game Engine!

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

## Next Steps

1. Explore the [examples](../examples) directory for more game ideas
2. Read the [API documentation](../api) for detailed information
3. Check out the [tutorials](../tutorials) for guided learning
4. Join our community:
   - GitHub Discussions
   - Discord Server
   - Stack Overflow tag: `retro-game-engine`

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
1. Check the [documentation](https://retro-game-engine.readthedocs.io)
2. Search existing GitHub issues
3. Ask in our Discord community
4. Open a new GitHub issue

Happy game development! 🎮
