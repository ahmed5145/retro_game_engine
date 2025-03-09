# Core API Reference

## GameLoop

The main game loop class that manages the game's execution.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| window_title | str | The title of the game window |
| window_width | int | The width of the game window in pixels |
| window_height | int | The height of the game window in pixels |
| current_scene | Scene | The currently active scene |
| target_fps | int | Target frames per second (default: 60) |
| is_running | bool | Whether the game loop is running |

### Methods

#### `__init__(self) -> None`
Initializes a new game loop instance.

#### `run(self) -> None`
Starts the game loop. This method blocks until the game is closed.

#### `stop(self) -> None`
Stops the game loop.

#### `change_scene(self, scene: Scene) -> None`
Changes the current scene to the specified scene.

## Scene

Base class for game scenes.

### Methods

#### `__init__(self) -> None`
Initializes a new scene instance.

#### `update(self, delta_time: float) -> None`
Updates the scene's logic. Called every frame.

Parameters:
- `delta_time`: Time elapsed since last frame in seconds

#### `draw(self, surface: pygame.Surface) -> None`
Draws the scene. Called every frame after update.

Parameters:
- `surface`: The surface to draw on

#### `on_enter(self) -> None`
Called when the scene becomes active.

#### `on_exit(self) -> None`
Called when the scene is being exited.

## Sprite

Class for handling sprite rendering and animation.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| config | SpriteConfig | Configuration for position, scale, rotation, etc. |
| texture | pygame.Surface | The sprite's texture |
| frames | List[SpriteFrame] | List of animation frames |
| current_frame | int | Index of current animation frame |

### Methods

#### `__init__(self, texture_path: str) -> None`
Initializes a new sprite instance.

Parameters:
- `texture_path`: Path to the sprite's texture file

#### `draw(self, surface: pygame.Surface) -> None`
Draws the sprite on the given surface.

Parameters:
- `surface`: The surface to draw on

#### `update(self, delta_time: float) -> None`
Updates the sprite's animation state.

Parameters:
- `delta_time`: Time elapsed since last frame in seconds

#### `add_frame(self, frame: SpriteFrame) -> None`
Adds an animation frame to the sprite.

Parameters:
- `frame`: The frame to add

#### `play_animation(self, speed: float = 1.0, loop: bool = True) -> None`
Starts playing the sprite's animation.

Parameters:
- `speed`: Animation playback speed multiplier
- `loop`: Whether to loop the animation

## Input

Static class for handling input.

### Methods

#### `@staticmethod is_key_pressed(key: int) -> bool`
Checks if a key is currently pressed.

Parameters:
- `key`: Pygame key constant

Returns:
- `bool`: True if the key is pressed

#### `@staticmethod is_mouse_button_pressed(button: int) -> bool`
Checks if a mouse button is currently pressed.

Parameters:
- `button`: Mouse button index (1: left, 2: middle, 3: right)

Returns:
- `bool`: True if the button is pressed

#### `@staticmethod get_mouse_position() -> Tuple[int, int]`
Gets the current mouse position.

Returns:
- `Tuple[int, int]`: (x, y) coordinates

## Physics

Class for handling physics calculations.

### Methods

#### `@staticmethod check_collision(sprite1: Sprite, sprite2: Sprite) -> bool`
Checks for collision between two sprites.

Parameters:
- `sprite1`: First sprite
- `sprite2`: Second sprite

Returns:
- `bool`: True if sprites are colliding

#### `@staticmethod apply_gravity(sprite: Sprite, gravity: float, delta_time: float) -> None`
Applies gravity to a sprite.

Parameters:
- `sprite`: The sprite to apply gravity to
- `gravity`: Gravity strength
- `delta_time`: Time elapsed since last frame

## Audio

Class for handling audio playback.

### Methods

#### `@staticmethod play_sound(sound_path: str, volume: float = 1.0) -> None`
Plays a sound effect.

Parameters:
- `sound_path`: Path to the sound file
- `volume`: Volume level (0.0 to 1.0)

#### `@staticmethod play_music(music_path: str, volume: float = 1.0, loop: bool = True) -> None`
Plays background music.

Parameters:
- `music_path`: Path to the music file
- `volume`: Volume level (0.0 to 1.0)
- `loop`: Whether to loop the music

#### `@staticmethod stop_music() -> None`
Stops currently playing music.

## UI

### Button

Class for creating interactive buttons.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| text | str | The button's text |
| position | Tuple[int, int] | Button position (x, y) |
| size | Tuple[int, int] | Button size (width, height) |
| is_hovered | bool | Whether the mouse is hovering over the button |
| is_pressed | bool | Whether the button is being pressed |

#### Methods

##### `__init__(self, text: str, position: Tuple[int, int], size: Tuple[int, int]) -> None`
Initializes a new button instance.

##### `update(self) -> None`
Updates the button's state based on input.

##### `draw(self, surface: pygame.Surface) -> None`
Draws the button on the given surface.

##### `on_click(self, callback: Callable[[], None]) -> None`
Sets the button's click callback function.
