# Building a Simple Platformer

In this tutorial, we'll create a basic platformer game using Retro Game Engine. You'll learn how to:
- Set up a game scene
- Create a player character with physics
- Handle keyboard input
- Add platforms and collision detection

## Project Setup

1. Create a new directory for your project:
```bash
mkdir platformer-game
cd platformer-game
```

2. Create the following file structure:
```
platformer-game/
├── assets/
│   ├── player.png
│   └── platform.png
└── main.py
```

3. Add simple placeholder images for the player (32x32 pixels) and platform (64x16 pixels).

## Basic Game Structure

Create `main.py` with the following code:

```python
from retro_game_engine import GameLoop, Scene, Sprite
from retro_game_engine.core.input import Input
from retro_game_engine.core.physics import Physics

class Player:
    def __init__(self, x: float, y: float):
        self.sprite = Sprite("assets/player.png")
        self.sprite.config.x = x
        self.sprite.config.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False

    def update(self, delta_time: float):
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += 800 * delta_time  # Gravity

        # Move player
        self.sprite.config.x += self.velocity_x * delta_time
        self.sprite.config.y += self.velocity_y * delta_time

    def draw(self, surface):
        self.sprite.draw(surface)

class Platform:
    def __init__(self, x: float, y: float):
        self.sprite = Sprite("assets/platform.png")
        self.sprite.config.x = x
        self.sprite.config.y = y

    def draw(self, surface):
        self.sprite.draw(surface)

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        # Create player
        self.player = Player(400, 300)

        # Create platforms
        self.platforms = [
            Platform(400, 500),  # Ground
            Platform(300, 400),  # Platform 1
            Platform(500, 400),  # Platform 2
        ]

    def update(self, delta_time: float):
        # Handle input
        if Input.is_key_pressed(pygame.K_LEFT):
            self.player.velocity_x = -300
        elif Input.is_key_pressed(pygame.K_RIGHT):
            self.player.velocity_x = 300
        else:
            self.player.velocity_x = 0

        # Jump when on ground
        if Input.is_key_pressed(pygame.K_SPACE) and self.player.on_ground:
            self.player.velocity_y = -500
            self.player.on_ground = False

        # Update player
        self.player.update(delta_time)

        # Check collisions
        self.player.on_ground = False
        for platform in self.platforms:
            if self._check_collision(self.player.sprite, platform.sprite):
                self._resolve_collision(self.player, platform)

    def draw(self, surface):
        # Draw platforms
        for platform in self.platforms:
            platform.draw(surface)

        # Draw player
        self.player.draw(surface)

    def _check_collision(self, sprite1: Sprite, sprite2: Sprite) -> bool:
        # Simple AABB collision
        r1 = sprite1.get_rect()
        r2 = sprite2.get_rect()
        return (r1.left < r2.right and
                r1.right > r2.left and
                r1.top < r2.bottom and
                r1.bottom > r2.top)

    def _resolve_collision(self, player: Player, platform: Platform):
        # Get rectangles
        player_rect = player.sprite.get_rect()
        platform_rect = platform.sprite.get_rect()

        # Calculate overlap
        dx = (player_rect.centerx - platform_rect.centerx)
        dy = (player_rect.centery - platform_rect.centery)

        # Resolve collision
        if abs(dx) > abs(dy):
            # Horizontal collision
            if dx > 0:
                player.sprite.config.x = platform_rect.right
            else:
                player.sprite.config.x = platform_rect.left - player_rect.width
            player.velocity_x = 0
        else:
            # Vertical collision
            if dy > 0:
                player.sprite.config.y = platform_rect.bottom
                player.velocity_y = 0
            else:
                player.sprite.config.y = platform_rect.top - player_rect.height
                player.velocity_y = 0
                player.on_ground = True

def main():
    game = GameLoop()
    game.window_title = "Platformer Game"
    game.window_width = 800
    game.window_height = 600
    game.current_scene = GameScene()
    game.run()

if __name__ == "__main__":
    main()
```

## Understanding the Code

### Player Class
The `Player` class manages the player character:
- Stores position and velocity
- Handles gravity
- Tracks ground contact

### Platform Class
Simple class for platform objects:
- Stores position
- Renders platform sprite

### GameScene Class
Main game scene that:
- Creates player and platforms
- Handles input
- Updates game logic
- Manages collisions
- Renders game objects

### Collision System
The collision system uses two main methods:
- `_check_collision`: Detects overlapping sprites
- `_resolve_collision`: Pushes objects apart and updates physics

## Running the Game

Run your game with:
```bash
python main.py
```

Use the arrow keys to move and space to jump!

## Next Steps

Try these enhancements:
1. Add double jumping
2. Create moving platforms
3. Add collectible items
4. Implement a level system
5. Add sound effects

## Common Issues

### Player gets stuck in platforms
- Check collision resolution order
- Ensure proper collision response
- Add debug visualization

### Jumping feels wrong
- Adjust gravity and jump velocity
- Add variable jump height
- Implement coyote time

### Movement feels stiff
- Add acceleration/deceleration
- Implement air control
- Add animation

## Complete Example

You can find the complete example with additional features in the [examples/platformer](../../examples/platformer) directory.

## Resources

- [Physics Tutorial](../guides/physics.md)
- [Animation Guide](../guides/animation.md)
- [Input Handling](../guides/input.md)
- [Game Design Tips](../guides/game_design.md)
