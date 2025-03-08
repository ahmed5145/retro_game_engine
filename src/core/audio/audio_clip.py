"""Audio clip management."""
from dataclasses import dataclass
from typing import Optional

import pygame


@dataclass
class AudioConfig:
    """Configuration for an audio clip.

    Attributes:
        volume: Volume level between 0.0 and 1.0
        loop: Whether to loop the audio
        priority: Priority level for channel allocation (higher numbers = higher priority)
    """

    volume: float = 1.0
    loop: bool = False
    priority: int = 0


class AudioClip:
    """Manages a single audio clip (sound effect or music).

    Attributes:
        path: Path to the audio file
        config: Audio configuration
        _sound: Pygame Sound object
        _channel: Channel the sound is playing on
    """

    def __init__(self, path: str, config: Optional[AudioConfig] = None) -> None:
        """Initialize the audio clip.

        Args:
            path: Path to the audio file
            config: Audio configuration
        """
        self.path = path
        self.config = config or AudioConfig()
        self._sound: Optional[pygame.mixer.Sound] = None
        self._channel: Optional[pygame.mixer.Channel] = None

    def load(self) -> None:
        """Load the audio file into memory."""
        try:
            self._sound = pygame.mixer.Sound(self.path)
            self._sound.set_volume(self.config.volume)
        except pygame.error as e:
            raise RuntimeError(f"Failed to load audio file {self.path}: {e}")

    def play(
        self, channel: Optional[pygame.mixer.Channel] = None
    ) -> Optional[pygame.mixer.Channel]:
        """Play the audio clip.

        Args:
            channel: Channel to play on (if None, a free channel will be used)

        Returns:
            The channel the sound is playing on, or None if playback failed
        """
        if not self._sound:
            raise RuntimeError("Audio clip not loaded")

        if channel:
            self._channel = channel
        else:
            # Find a free channel
            self._channel = pygame.mixer.find_channel()
            if not self._channel:
                return None

        self._channel.play(self._sound, loops=-1 if self.config.loop else 0)
        return self._channel

    def stop(self) -> None:
        """Stop playback of the audio clip."""
        if self._channel and self._channel.get_busy():
            self._channel.stop()

    def set_volume(self, volume: float) -> None:
        """Set the volume of the audio clip.

        Args:
            volume: Volume level between 0.0 and 1.0
        """
        volume = max(0.0, min(1.0, volume))
        self.config.volume = volume
        if self._sound:
            self._sound.set_volume(volume)

    def is_playing(self) -> bool:
        """Check if the audio clip is currently playing.

        Returns:
            True if the clip is playing, False otherwise
        """
        return bool(self._channel and self._channel.get_busy())

    def unload(self) -> None:
        """Unload the audio clip from memory."""
        if self._channel and self._channel.get_busy():
            self._channel.stop()
        self._sound = None
        self._channel = None
