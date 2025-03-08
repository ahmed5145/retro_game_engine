"""Demo showcasing the audio system capabilities."""
import os
import sys
import pygame
from src.core.audio import AudioManager, AudioConfig

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Audio System Demo")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Font
font = pygame.font.Font(None, 36)

def draw_text(text: str, x: int, y: int, color: tuple[int, int, int] = WHITE) -> None:
    """Draw text on screen.
    
    Args:
        text: Text to draw
        x: X coordinate
        y: Y coordinate
        color: RGB color tuple
    """
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

def main() -> None:
    """Run the audio demo."""
    # Initialize audio manager
    audio_manager = AudioManager(num_channels=4)
    
    # Load audio clips
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    audio_manager.load_clip(
        "music",
        os.path.join(assets_dir, "background.wav"),
        AudioConfig(volume=0.7, loop=True)
    )
    audio_manager.load_clip(
        "jump",
        os.path.join(assets_dir, "jump.wav"),
        AudioConfig(volume=0.5)
    )
    audio_manager.load_clip(
        "coin",
        os.path.join(assets_dir, "coin.wav"),
        AudioConfig(volume=0.6)
    )
    
    # Start background music
    audio_manager.play_music("music")
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    music_paused = False
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    audio_manager.play_sound("jump")
                elif event.key == pygame.K_c:
                    audio_manager.play_sound("coin")
                elif event.key == pygame.K_p:
                    if music_paused:
                        audio_manager.resume_music()
                        music_paused = False
                    else:
                        audio_manager.pause_music()
                        music_paused = True
                elif event.key == pygame.K_UP:
                    current_volume = audio_manager._master_volume
                    audio_manager.set_master_volume(min(current_volume + 0.1, 1.0))
                elif event.key == pygame.K_DOWN:
                    current_volume = audio_manager._master_volume
                    audio_manager.set_master_volume(max(current_volume - 0.1, 0.0))
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw instructions
        draw_text("Audio System Demo", SCREEN_WIDTH // 2, 50)
        draw_text("Space: Play jump sound", SCREEN_WIDTH // 2, 150)
        draw_text("C: Play coin sound", SCREEN_WIDTH // 2, 200)
        draw_text("P: Pause/Resume music", SCREEN_WIDTH // 2, 250)
        draw_text("Up/Down: Adjust volume", SCREEN_WIDTH // 2, 300)
        draw_text("ESC: Exit", SCREEN_WIDTH // 2, 350)
        
        # Draw volume bar
        volume = audio_manager._master_volume
        bar_width = 300
        bar_height = 20
        x = (SCREEN_WIDTH - bar_width) // 2
        y = 400
        pygame.draw.rect(screen, GRAY, (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, WHITE, (x, y, int(bar_width * volume), bar_height))
        draw_text(f"Volume: {int(volume * 100)}%", SCREEN_WIDTH // 2, 450)
        
        # Draw music status
        status = "PAUSED" if music_paused else "PLAYING"
        draw_text(f"Music: {status}", SCREEN_WIDTH // 2, 500)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    # Cleanup
    audio_manager.cleanup()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 