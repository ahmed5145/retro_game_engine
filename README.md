# Retro Game Engine

A lightweight, authentic 8-bit and 16-bit style game development framework focused on delivering pixel-perfect retro gaming experiences.

## Features (Planned)

- Pixel-perfect 2D rendering with multiple resolution modes
- Sprite system with animation support
- Tile-based map system
- Collision detection system
- Physics system with retro-appropriate constraints
- Input handling (keyboard, mouse, gamepad)
- Audio system with chiptune support
- Scene management
- Entity-Component System
- Development tools (Sprite Editor, Tilemap Editor)

## Development Status

Currently in initial development phase. See [ROADMAP.md](./ROADMAP.md) for detailed plans.

## Requirements

- Python 3.11+
- Poetry (for dependency management)
- Pygame 2.5.0+
- pytest for testing

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/ahmed5145/retro_game_engine.git
cd retro_game_engine
```

2. Install dependencies:

```bash
poetry install
```

3. Run tests:

```bash
poetry run pytest
```

## Project Structure

```text
retro_game_engine/
├── src/                  # Source code
│   ├── core/            # Core engine components
│   ├── graphics/        # Rendering and visual systems
│   └── utils/           # Utility functions
├── tests/               # Test suite
├── docs/                # Documentation
├── examples/            # Example games and demos
└── tools/               # Development tools
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](./LICENSE) for details.
