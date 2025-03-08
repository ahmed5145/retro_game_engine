# Retro Game Engine

A lightweight, feature-rich game development framework designed for creating authentic 8-bit and 16-bit style games. Built with Python and Pygame, this engine provides a robust set of tools while maintaining the aesthetic and technical constraints that defined the retro gaming era.

## Features

### Core Engine Components

- **Rendering System**
  - Pixel-perfect 2D rendering
  - Multiple resolution modes
  - Layer support with configurable depth
  - Parallax scrolling effects
  - Screen-space effects (screen shake, flash, fade)

- **Sprite System**
  - Sprite sheet support with variable-sized frames
  - Sprite flipping and rotation
  - Z-ordering and transparency
  - Batched sprite rendering for performance
  - Animation support

- **Tile System**
  - Multiple background layers with scrolling
  - Tile-based collision maps
  - Auto-tiling support
  - Animated tiles
  - Efficient culling of off-screen tiles

- **Physics & Collision**
  - Rectangle and circle collision detection
  - Spatial partitioning for performance
  - Raycast collision detection
  - Platform physics (gravity, jumping, etc.)
  - Collision groups and masks

- **Audio System**
  - Sound effect and music support
  - Multiple audio channels
  - Volume control per channel
  - Sound priority system

- **Input System**
  - Keyboard and mouse support
  - Gamepad integration
  - Input buffering
  - Configurable key bindings

### Entity Component System (ECS)

- Component-based architecture
- Predefined components (Transform, Sprite, etc.)
- Entity templates/prefabs
- Event system for entity communication
- Efficient entity queries and updates

### Scene Management

- Multiple scene support
- Scene transitions
- Scene persistence
- Environment variables per scene
- Camera system with various behaviors

### User Interface

- Text rendering with bitmap fonts
- Menu system
- HUD elements
- Dialog boxes with text animation
- Screen-space UI anchoring

## Installation

1. Ensure you have Python 3.8+ installed
2. Install Poetry (dependency management):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Clone the repository:
   ```bash
   git clone https://github.com/ahmed5145/retro-game-engine.git
   cd retro-game-engine
   ```
4. Install dependencies:
   ```bash
   poetry install
   ```

## Quick Start

1. Create a new game project:
```python
from src.core import Game, Scene, Entity
from src.core.ecs.components import SpriteRenderer, Transform

class MyGame(Game):
    def __init__(self):
        super().__init__(width=320, height=240, title="My Retro Game")

        # Create a scene
        scene = Scene("main")

        # Create an entity
        player = Entity("player")
        player.add_component(Transform(x=160, y=120))
        player.add_component(SpriteRenderer("player.png"))

        # Add entity to scene
        scene.add_entity(player)

        # Set as active scene
        self.scene_manager.push_scene(scene)

if __name__ == "__main__":
    game = MyGame()
    game.run()
```

## Documentation

### Core Concepts

#### Entity Component System

The engine uses an ECS architecture where:
- **Entities** are containers for components
- **Components** hold data and behavior
- **Systems** process entities with specific components

Example:
```python
# Create an entity
player = Entity("player")

# Add components
transform = Transform(x=100, y=100)
sprite = SpriteRenderer("player.png")
player.add_component(transform)
player.add_component(sprite)
```

#### Scene Management

Scenes represent different game states or levels:
```python
class GameScene(Scene):
    def on_enter(self):
        # Setup when scene becomes active
        self.create_player()
        self.load_level()

    def on_exit(self):
        # Cleanup when scene is removed
        self.clear()

    def update(self, dt):
        # Update logic
        self.process_input()
        self.update_entities(dt)
```

#### Collision Detection

The engine provides various collision detection methods:
```python
# Rectangle collision
if physics.check_collision(rect1, rect2):
    handle_collision()

# Tilemap collision
collision = tilemap.check_collision(player_rect)
if collision:
    normal, penetration = collision
    resolve_collision(normal, penetration)
```

### Best Practices

1. **Scene Organization**
   - Keep scenes focused on a single responsibility
   - Use scene transitions for loading/unloading
   - Implement proper cleanup in `on_exit`

2. **Component Design**
   - Keep components small and focused
   - Use composition over inheritance
   - Cache component references when needed

3. **Performance**
   - Use spatial partitioning for large worlds
   - Implement object pooling for frequent creation/destruction
   - Batch similar operations (rendering, physics)

4. **Memory Management**
   - Clear resources when scenes exit
   - Unload unused assets
   - Use weak references for event listeners

## Testing

Run the test suite:
```bash
poetry run pytest
```

Run with coverage:
```bash
poetry run pytest --cov=src
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure they pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Pygame](https://www.pygame.org/)
- Inspired by classic game engines and retro gaming systems
