# Retro Game Engine

A modern Python game engine built with Pygame, designed for creating retro-style 2D games.

## Features

- **Modern Game Loop**: Fixed and variable timestep updates
- **Entity Component System**: Flexible and efficient game object management
- **Scene Management**: Easy state transitions and game flow control
- **Input System**: Keyboard and gamepad support with action mapping
- **Physics System**: 2D collision detection and resolution
- **Audio System**: Sound effects and music playback
- **Sprite System**: Animation and rendering utilities
- **Tilemap Support**: Efficient tile-based level design
- **UI System**: Buttons, text, and other UI elements

## Quick Start

```bash
# Install the engine
pip install retro-game-engine

# Create a simple game
from retro_game_engine import Game, Scene

class MyGame(Scene):
    def update(self, dt: float):
        # Update game logic
        pass

    def render(self):
        # Render game objects
        pass

game = Game()
game.run(MyGame())
```

## Example Games

Check out our example games to see what you can build:

- [Platformer](tutorials/platformer.md): A simple platformer game
- More examples coming soon!

## Getting Started

- [Installation Guide](installation.md): Get up and running
- [Tutorials](tutorials/README.md): Learn through examples
- [API Reference](api/index.md): Detailed documentation

## Community

- [GitHub Issues](https://github.com/ahmed5145/retro_game_engine/issues): Report bugs or request features
- [GitHub Discussions](https://github.com/ahmed5145/retro_game_engine/discussions): Ask questions and share ideas

## Contributing

We welcome contributions! See our [Contributing Guide](https://github.com/ahmed5145/retro_game_engine/blob/main/CONTRIBUTING.md) to get started.
