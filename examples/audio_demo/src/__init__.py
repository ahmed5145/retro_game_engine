"""Audio demo example."""
import sys
from pathlib import Path

import pygame

# Add the root directory to Python path
root_dir = str(Path(__file__).parent.parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.core.audio.audio_clip import AudioClip
from src.core.audio.audio_manager import AudioManager


def main() -> None:
    """Run the audio demo."""
    # Initialize pygame
    pygame.init()
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Audio Demo")

    # Create audio manager
    audio_manager = AudioManager()

    # Load audio clips
    sound_effects = {}
    sound_effects["jump"] = audio_manager.load_clip("assets/audio/jump.wav")
    sound_effects["coin"] = audio_manager.load_clip("assets/audio/coin.wav")
    sound_effects["hit"] = audio_manager.load_clip("assets/audio/hit.wav")

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if sound_effects["jump"] is not None:
                        audio_manager.play_sound(sound_effects["jump"])
                elif event.key == pygame.K_c:
                    if sound_effects["coin"] is not None:
                        audio_manager.play_sound(sound_effects["coin"])
                elif event.key == pygame.K_h:
                    if sound_effects["hit"] is not None:
                        audio_manager.play_sound(sound_effects["hit"])
                elif event.key == pygame.K_m:
                    audio_manager.play_music("assets/audio/background.wav")
                elif event.key == pygame.K_p:
                    audio_manager.pause_music()
                elif event.key == pygame.K_r:
                    audio_manager.resume_music()
                elif event.key == pygame.K_s:
                    audio_manager.stop_music()

        # Update display
        pygame.display.flip()

    # Cleanup
    audio_manager.cleanup()
    pygame.quit()


if __name__ == "__main__":
    main()
