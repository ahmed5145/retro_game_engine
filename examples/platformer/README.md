# Platformer Example

A complete platformer game example using Retro Game Engine.

## Features

- Player movement and jumping with double jump ability
- Static and moving platforms
- Collectible coins with animations
- Sound effects and background music
- Score tracking

## Required Assets

Place the following assets in the `assets` directory:

### Images

1. `player.png`
   - Size: 128x32 pixels
   - Contains: 4 frames of player animation (32x32 each)
   - Format: PNG with transparency
   - Animation frames: idle, walk1, walk2, jump

2. `platform.png`
   - Size: 64x16 pixels
   - Contains: Single platform texture
   - Format: PNG with transparency
   - Style: Simple solid platform with optional decorative elements

3. `coin.png`
   - Size: 96x16 pixels
   - Contains: 6 frames of coin animation (16x16 each)
   - Format: PNG with transparency
   - Animation: Spinning coin effect

### Sound Effects

1. `jump.wav`
   - Duration: ~0.5 seconds
   - Type: Short jump sound effect
   - Format: WAV

2. `double_jump.wav`
   - Duration: ~0.5 seconds
   - Type: Alternative jump sound for double jump
   - Format: WAV

3. `coin.wav`
   - Duration: ~0.5 seconds
   - Type: Coin collection sound
   - Format: WAV

4. `death.wav`
   - Duration: ~1 second
   - Type: Player death/fall sound
   - Format: WAV

5. `music.wav`
   - Duration: 1-2 minutes (loops)
   - Type: Background music
   - Format: WAV

## Running the Example

1. Ensure all required assets are in the `assets` directory
2. Run the game:
```bash
python main.py
```

## Controls

- Left/Right Arrow: Move
- Space: Jump (press again for double jump)
- Escape: Quit

## Customization

You can modify various game parameters in `main.py`:

- `PLAYER_SPEED`: Movement speed (default: 300)
- `JUMP_FORCE`: Jump strength (default: 500)
- `GRAVITY`: Gravity strength (default: 800)
- `COIN_SCORE`: Points per coin (default: 100)

## Creating Your Own Assets

### Player Sprite
- Create a 128x32 image
- Divide into 4 32x32 frames
- Include these animations:
  1. Idle stance
  2. Walking frame 1
  3. Walking frame 2
  4. Jumping pose

### Platform Sprite
- Create a 64x16 image
- Use solid colors or textures
- Add highlights for depth
- Optional decorative elements

### Coin Sprite
- Create a 96x16 image
- Divide into 6 16x16 frames
- Design a spinning animation sequence
- Use bright colors and optional glow effects

## Tips

1. Keep the background color (100, 149, 237) in mind when designing sprites
2. Use transparency for smoother visuals
3. Test animations with different frame rates by adjusting the speed parameter
4. Balance sound effect volumes for a good mix with background music
