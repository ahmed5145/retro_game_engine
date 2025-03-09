# Retro Game Engine 🎮

[![CI](https://github.com/ahmed5145/retro_game_engine/actions/workflows/ci.yml/badge.svg)](https://github.com/ahmed5145/retro_game_engine/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/retro-game-engine.svg)](https://badge.fury.io/py/retro-game-engine)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modern Python game development framework for creating authentic 8-bit and 16-bit style games. Built with performance and developer experience in mind, it provides a robust set of tools while maintaining the aesthetic and technical constraints that defined the retro gaming era.

<p align="center">
  <img src="docs/images/logo.svg" alt="Retro Game Engine Logo" width="200"/>
</p>

## ✨ Features

### 🎨 Core Engine
- **High-Performance Rendering**: Pixel-perfect 2D graphics with hardware acceleration
- **Flexible Sprite System**: Animation, batching, and effects
- **Tile-Based Maps**: Scrolling, auto-tiling, and efficient culling
- **Robust Physics**: Collision detection and resolution
- **Audio Management**: Sound effects and music with priority system
- **Input Handling**: Keyboard, mouse, and gamepad support

### 🏗️ Architecture
- **Entity Component System**: Modular and efficient game object management
- **Scene Management**: Easy state transitions and persistence
- **Event System**: Flexible communication between components
- **UI Framework**: Text, menus, and HUD elements

[View all features →](docs/features.md)

## 🚀 Quick Start

### Installation

```bash
pip install retro-game-engine
```

### Create Your First Game

```python
from retro_game_engine import Game, Scene, Entity
from retro_game_engine.components import Transform, SpriteRenderer

class MyGame(Game):
    def __init__(self):
        super().__init__(width=320, height=240, title="My Retro Game")

        # Create and setup your game scene
        scene = Scene("main")
        player = Entity("player")
        player.add_component(Transform(x=160, y=120))
        player.add_component(SpriteRenderer("player.png"))
        scene.add_entity(player)

        # Start the game
        self.scene_manager.push_scene(scene)

if __name__ == "__main__":
    MyGame().run()
```

[Get Started Guide →](docs/getting-started.md)

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Tutorials](docs/tutorials/README.md)
- [API Reference](docs/api/README.md)
  - [Game Loop](docs/api/game_loop.md) - Core game loop and timing system
  - [Window](docs/api/window.md) - Window management and rendering
  - [Sprite](docs/api/sprite.md) - Sprite and animation system
  - [Input](docs/api/input.md) - Input handling system
- [Examples](docs/examples/README.md)
- [Best Practices](docs/guides/best-practices.md)
- [Migration Guide](docs/guides/migration.md)

## 🎮 Examples

- [Platformer Game](examples/platformer/README.md)
- [Top-down RPG](examples/rpg/README.md)
- [Shoot 'em up](examples/shmup/README.md)
- [Puzzle Game](examples/puzzle/README.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/ahmed5145/retro_game_engine.git
cd retro_game_engine
```

2. Install Poetry (dependency management):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies:
```bash
poetry install
```

4. Run tests:
```bash
poetry run pytest
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
## 🙏 Acknowledgments

- Built with [Pygame](https://www.pygame.org/)
- Inspired by classic game engines and retro gaming systems
- Thanks to all [contributors](https://github.com/ahmed5145/retro_game_engine/graphs/contributors)

## 📫 Contact & Support

- [GitHub Issues](https://github.com/ahmed5145/retro_game_engine/issues) for bug reports and feature requests
- [GitHub Discussions](https://github.com/ahmed5145/retro_game_engine/discussions) for questions and community discussions
- [Documentation](https://retro-game-engine.readthedocs.io/) for comprehensive guides and API reference
