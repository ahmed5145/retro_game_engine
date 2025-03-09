"""Audio clip for playing sound effects and music."""
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
    """Audio clip that can be loaded and played."""

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
        """Load the audio file.

        Raises:
            RuntimeError: If the file cannot be loaded
        """
        try:
            self._sound = pygame.mixer.Sound(self.path)
        except pygame.error as e:
            raise RuntimeError(f"Failed to load audio file '{self.path}': {e}") from e

    def play(
        self, channel: Optional[pygame.mixer.Channel] = None
    ) -> Optional[pygame.mixer.Channel]:
        """Play the audio clip.

        Args:
            channel: Optional channel to play on (default: None)

        Returns:
            Channel the sound is playing on, or None if playback failed

        Raises:
            RuntimeError: If the clip hasn't been loaded
        """
        if not self._sound:
            raise RuntimeError("Audio clip must be loaded before playing")

        try:
            # Store previous channel and find new one
            prev_channel = self._channel
            self._channel = channel or pygame.mixer.find_channel()

            # Handle channel allocation failure
            if not self._channel:
                print(f"No available channels to play audio clip '{self.path}'")
                return None

            # Configure and play the sound
            self._channel.set_volume(self.config.volume)
            self._channel.play(self._sound, loops=-1 if self.config.loop else 0)
            if self.config.loop:
                self._channel.set_endevent(-1)  # Disable end event for looping

            # Stop previous channel if different
            if prev_channel and prev_channel != self._channel:
                prev_channel.stop()

            return self._channel

        except pygame.error as e:
            print(f"Failed to play audio clip '{self.path}': {e}")
            return None

    def stop(self) -> None:
        """Stop playing the audio clip."""
        if self._channel:
            self._channel.stop()

    def set_volume(self, volume: float) -> None:
        """Set the volume of the audio clip.

        Args:
            volume: Volume level between 0.0 and 1.0

        Raises:
            ValueError: If volume is not between 0.0 and 1.0
        """
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0")

        self.config.volume = volume
        if self._sound:
            self._sound.set_volume(volume)

    def is_playing(self) -> bool:
        """Check if the audio clip is currently playing.

        Returns:
            True if playing, False otherwise
        """
        return bool(self._channel and self._channel.get_busy())

    def unload(self) -> None:
        """Unload the audio clip."""
        self.stop()
        self._sound = None
