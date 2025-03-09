"""Audio clip class for loading and playing sound effects."""
from dataclasses import dataclass
from typing import Optional

import pygame


@dataclass
class AudioConfig:
    """Configuration for audio clips.

    Attributes:
        volume: Volume level (0.0 to 1.0)
        loop: Whether to loop the audio
    """

    volume: float = 1.0
    loop: bool = False


class AudioClip:
    """Represents a single audio clip that can be loaded and played."""

    def __init__(self, path: str, config: Optional[AudioConfig] = None) -> None:
        """Initialize the audio clip.

        Args:
            path: Path to the audio file
            config: Optional audio configuration
        """
        self.path = path
        self.config = config or AudioConfig()
        self._sound: Optional[pygame.mixer.Sound] = None
        self._channel: Optional[pygame.mixer.Channel] = None

    def load(self) -> None:
        """Load the audio clip.

        Raises:
            FileNotFoundError: If the audio file doesn't exist
            RuntimeError: If the audio file can't be loaded
        """
        try:
            self._sound = pygame.mixer.Sound(self.path)
            self._sound.set_volume(self.config.volume)
        except FileNotFoundError:
            raise FileNotFoundError(f"Audio file not found: {self.path}")
        except pygame.error as e:
            raise RuntimeError(f"Failed to load audio file: {e}")

    def play(
        self, channel: Optional[pygame.mixer.Channel] = None
    ) -> Optional[pygame.mixer.Channel]:
        """Play the audio clip.

        Args:
            channel: Optional channel to play on

        Returns:
            Channel the sound is playing on, or None if playback failed

        Raises:
            RuntimeError: If the clip hasn't been loaded
        """
        if not self._sound:
            raise RuntimeError("Audio clip must be loaded before playing")

        if channel:
            self._channel = channel
        else:
            self._channel = pygame.mixer.find_channel()

        if self._channel:
            self._channel.play(self._sound, -1 if self.config.loop else 0)
            return self._channel

        return None

    def stop(self) -> None:
        """Stop playing the audio clip."""
        if self._channel:
            self._channel.stop()
            self._channel = None

    def is_playing(self) -> bool:
        """Check if the audio clip is currently playing.

        Returns:
            True if the clip is playing
        """
        return bool(self._channel and self._channel.get_busy())

    def set_volume(self, volume: float) -> None:
        """Set the volume level.

        Args:
            volume: Volume level (0.0 to 1.0)

        Raises:
            ValueError: If volume is not between 0.0 and 1.0
        """
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0")
        self.config.volume = volume
        if self._sound:
            self._sound.set_volume(volume)

    def unload(self) -> None:
        """Unload the audio clip."""
        # Stop playback first
        self.stop()

        # Release sound resource
        if self._sound:
            # Ensure the sound is stopped
            self._sound.stop()
            # Release the sound object
            self._sound = None

        # Clear channel reference
        self._channel = None
