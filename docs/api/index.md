# API Reference

## Core Components

### Window Management
- [Window](window.md) - Window creation and management
- [WindowConfig](window.md#windowconfig) - Window configuration options

### Game Loop
- [GameLoop](game_loop.md) - Main game loop implementation
- [GameLoopConfig](game_loop.md#gameloopconfig) - Game loop configuration
- [PerformanceMetrics](game_loop.md#performancemetrics) - Performance monitoring

### Sprites and Graphics
- [Sprite](sprite.md) - Sprite rendering and management
- [SpriteSheet](sprite.md#spritesheet) - Sprite sheet handling
- [SpriteConfig](sprite.md#spriteconfig) - Sprite configuration
- [SpriteRenderer](sprite_renderer.md) - Efficient sprite rendering system

### Input Handling
- [InputManager](input.md) - Input management system
- [InputAction](input.md#inputaction) - Input action configuration
- [InputBinding](input.md#inputbinding) - Key binding system

### Audio System
- [AudioManager](audio.md) - Audio playback and management
- [AudioClip](audio.md#audioclip) - Sound effect and music handling
- [AudioConfig](audio.md#audioconfig) - Audio configuration options

### Entity Component System
- [Entity](ecs/entity.md) - Base entity class
- [Component](ecs/component.md) - Component base class
- [World](ecs/world.md) - ECS world management

### Scene Management
- [Scene](scene.md) - Scene management
- [SceneManager](scene_manager.md) - Scene switching and stacking

### Physics
- [PhysicsBody](physics.md) - Physics simulation
- [PhysicsConfig](physics.md#physicsconfig) - Physics configuration
- [Vector2D](vector2d.md) - 2D vector operations

### Tilemap System
- [Tilemap](tilemap.md) - Tilemap management
- [TileConfig](tilemap.md#tileconfig) - Tile configuration
- [TileLayerConfig](tilemap.md#tilelayerconfig) - Layer configuration

### UI System
- [UIElement](ui/ui_element.md) - Base UI element
- [Button](ui/button.md) - Button implementation
- [Text](ui/text.md) - Text rendering
- [UIRect](ui/ui_element.md#uirect) - UI positioning

## Examples

See the [examples directory](../../examples/README.md) for practical usage examples of these components.
