# Examples

This directory contains example projects demonstrating different features of the Retro Game Engine.

## Basic Game Loop
[basic_game_loop/](basic_game_loop/) - A minimal example showing how to set up the game loop and handle basic window creation and rendering.

## Platformer
[platformer/](platformer/) - A complete 2D platformer game demonstrating physics, collision detection, sprite animation, and sound effects.

## Sprite Animation
[sprite_test/](sprite_test/) - Shows how to use the sprite system, including loading sprite sheets, animation, and sprite rendering.

## Tilemap
[tilemap_test/](tilemap_test/) - Demonstrates the tilemap system, including loading tilemaps, scrolling, and collision detection.

## Input Handling
[input_test/](input_test/) - Shows how to handle keyboard and gamepad input, including input mapping and state management.

## Audio
[audio_demo/](audio_demo/) - Demonstrates the audio system, including playing sound effects and background music.

## Running the Examples

Each example can be run from its directory:

```bash
# Install dependencies first
poetry install

# Run an example
poetry run python -m examples.platformer
poetry run python -m examples.sprite_test
# etc...
```

## Example Structure

Each example follows this structure:
```
example_name/
├── README.md           # Documentation and tutorial
├── assets/            # Game assets (sprites, audio, etc.)
│   ├── sprites/
│   ├── audio/
│   └── ...
├── src/              # Source code
│   ├── __init__.py   # Main game code
│   ├── components/   # Custom components
│   └── systems/      # Game systems
└── requirements.txt  # Additional dependencies
```
