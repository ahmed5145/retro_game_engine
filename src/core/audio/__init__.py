"""Audio system for the game engine."""
from typing import Dict, Optional

import pygame

from .audio_clip import AudioClip
from .audio_clip import AudioConfig as AudioClipConfig
from .audio_manager import AudioManager

__all__ = ["AudioClip", "AudioClipConfig", "AudioManager", "Audio"]

"""Audio management module."""


class Audio:
    """Static class for managing audio playback."""

    # Class variables for caching sounds
    _sounds: Dict[str, pygame.mixer.Sound] = {}
    _current_music: Optional[str] = None

    @classmethod
    def initialize(cls) -> None:
        """Initialize the audio system."""
        pygame.mixer.init()

    @classmethod
    def play_sound(cls, sound_path: str, volume: float = 1.0) -> None:
        """Play a sound effect.

        Args:
            sound_path: Path to the sound file
            volume: Volume level from 0.0 to 1.0
        """
        if not (0.0 <= volume <= 1.0):
            raise ValueError("Volume must be between 0.0 and 1.0")

        # Cache sound if not already loaded
        if sound_path not in cls._sounds:
            try:
                cls._sounds[sound_path] = pygame.mixer.Sound(sound_path)
            except FileNotFoundError:
                raise FileNotFoundError(f"Sound file not found: {sound_path}")
            except pygame.error as e:
                raise pygame.error(f"Error loading sound: {e}")

        # Play the sound
        sound = cls._sounds[sound_path]
        sound.set_volume(volume)
        sound.play()

    @classmethod
    def play_music(
        cls, music_path: str, volume: float = 1.0, loop: bool = True
    ) -> None:
        """Play background music.

        Args:
            music_path: Path to the music file
            volume: Volume level from 0.0 to 1.0
            loop: Whether to loop the music
        """
        if not (0.0 <= volume <= 1.0):
            raise ValueError("Volume must be between 0.0 and 1.0")

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1 if loop else 0)
            cls._current_music = music_path
        except FileNotFoundError:
            raise FileNotFoundError(f"Music file not found: {music_path}")
        except pygame.error as e:
            raise pygame.error(f"Error loading music: {e}")

    @classmethod
    def stop_music(cls) -> None:
        """Stop currently playing music."""
        pygame.mixer.music.stop()
        cls._current_music = None

    @classmethod
    def pause_music(cls) -> None:
        """Pause currently playing music."""
        pygame.mixer.music.pause()

    @classmethod
    def unpause_music(cls) -> None:
        """Unpause currently playing music."""
        pygame.mixer.music.unpause()

    @classmethod
    def set_music_volume(cls, volume: float) -> None:
        """Set the music volume.

        Args:
            volume: Volume level from 0.0 to 1.0
        """
        if not (0.0 <= volume <= 1.0):
            raise ValueError("Volume must be between 0.0 and 1.0")
        pygame.mixer.music.set_volume(volume)

    @classmethod
    def get_music_volume(cls) -> float:
        """Get the current music volume.

        Returns:
            float: Current volume level between 0.0 and 1.0
        """
        try:
            return float(pygame.mixer.music.get_volume())
        except pygame.error:
            return 0.0

    @classmethod
    def is_music_playing(cls) -> bool:
        """Check if music is currently playing.

        Returns:
            True if music is playing, False otherwise
        """
        return bool(pygame.mixer.music.get_busy())

    @classmethod
    def fade_out_music(cls, time_ms: int) -> None:
        """Fade out the currently playing music.

        Args:
            time_ms: Time to fade out in milliseconds
        """
        pygame.mixer.music.fadeout(time_ms)
        cls._current_music = None

    @classmethod
    def queue_music(cls, music_path: str) -> None:
        """Queue the next music track.

        Args:
            music_path: Path to the music file to queue
        """
        try:
            pygame.mixer.music.queue(music_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Music file not found: {music_path}")
        except pygame.error as e:
            raise pygame.error(f"Error queuing music: {e}")

    @classmethod
    def set_music_position(cls, position_seconds: float) -> None:
        """Set the position of the currently playing music.

        Args:
            position_seconds: Position in seconds
        """
        try:
            pygame.mixer.music.set_pos(position_seconds)
        except pygame.error as e:
            raise pygame.error(f"Error setting music position: {e}")

    @classmethod
    def cleanup(cls) -> None:
        """Clean up audio resources."""
        pygame.mixer.quit()
        cls._sounds.clear()
        cls._current_music = None
