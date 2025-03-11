# Migration Guide

This guide helps you migrate your game projects between different versions of the Retro Game Engine.

## Migrating to 1.0.0

### Breaking Changes

1. Game Loop API Changes
   ```python
   # Old (0.x)
   game = Game()
   game.start()

   # New (1.0)
   game = Game()
   game.run()
   ```

2. Entity Component System
   ```python
   # Old (0.x)
   entity.add_component(Transform(x=0, y=0))

   # New (1.0)
   entity.add_component(Transform(position=Vector2(0, 0)))
   ```

3. Scene Management
   ```python
   # Old (0.x)
   game.change_scene("menu")

   # New (1.0)
   game.scene_manager.push_scene("menu")
   ```

### Deprecated Features

The following features are deprecated and will be removed in version 2.0:
- `Game.old_update()` - Use `Game.update()` instead
- `Sprite.set_position()` - Use `Transform.position` instead
- `Scene.add()` - Use `Scene.add_entity()` instead

### New Features

1. Improved Performance Metrics
   ```python
   game.metrics.fps  # Current FPS
   game.metrics.frame_time  # Time per frame
   ```

2. Enhanced Input System
   ```python
   input.bind_action("jump", Key.SPACE)
   input.is_action_pressed("jump")
   ```

3. Asset Management
   ```python
   assets.load_texture("player", "assets/player.png")
   sprite.texture = assets.get_texture("player")
   ```

## Migrating to 0.9.0

### Breaking Changes

1. Input System Changes
   ```python
   # Old (0.8.x)
   if input.is_key_pressed(Keys.SPACE):
       pass

   # New (0.9)
   if input.is_key_pressed(Key.SPACE):
       pass
   ```

2. Audio System
   ```python
   # Old (0.8.x)
   audio.play_sound("jump.wav")

   # New (0.9)
   audio.play("jump")
   ```

### Deprecated Features

- `Game.fixed_update` - Will be removed in 1.0
- Old collision system - Use new physics system instead

## Troubleshooting

### Common Migration Issues

1. **Missing Components**
   ```python
   # Solution: Add required components
   entity.add_component(Transform())
   entity.add_component(Renderer())
   ```

2. **Scene Loading Errors**
   ```python
   # Solution: Update scene registration
   game.scene_manager.register_scene("menu", MenuScene)
   ```

3. **Input Binding Issues**
   ```python
   # Solution: Update key constants
   input.bind_action("move_right", Key.D)  # Not Keys.D
   ```

### Automated Migration

We provide a migration script to help automate some changes:

```bash
python -m retro_game_engine.tools.migrate your_game_directory
```

## Version History

See our [CHANGELOG.md](../../CHANGELOG.md) for detailed version history and changes.

## Getting Help

If you encounter issues during migration:
1. Check our [GitHub Issues](https://github.com/ahmed5145/retro_game_engine/issues)
2. Join our [Discord community](https://discord.gg/retrogameengine)
3. Read the [API Reference](../api/README.md)
