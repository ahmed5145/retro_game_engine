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
            self._sound.set_volume(self.config.volume)
        except (pygame.error, FileNotFoundError) as e:
            self._sound = None
            raise RuntimeError(f"Failed to load audio file '{self.path}': {e}") from e

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

        # Stop if already playing
        prev_channel = None
        if self._channel and self._channel.get_busy():
            prev_channel = self._channel
            prev_channel.stop()
            self._channel = None

        try:
            # Play on specified channel or any available channel
            if channel:
                self._channel = channel
            else:
                # Find an available channel
                self._channel = pygame.mixer.find_channel()
                if not self._channel:
                    print(f"No available channels to play audio clip '{self.path}'")
                    return None

            # Play the sound with proper looping
            self._channel.play(self._sound, loops=-1 if self.config.loop else 0)
            if self.config.loop:
                self._channel.set_endevent(-1)  # Disable end event for looping

            # Verify previous channel was stopped
            if prev_channel and prev_channel.get_busy():
                prev_channel.stop()

            return self._channel
        except pygame.error as e:
            print(f"Failed to play audio clip '{self.path}': {e}")
            self._channel = None
            return None

    def stop(self) -> None:
        """Stop playing the audio clip."""
        if self._channel and self._channel.get_busy():
            self._channel.stop()
        self._channel = None

    def set_volume(self, volume: float) -> None:
        """Set the volume level.

        Args:
            volume: Volume level between 0.0 and 1.0
        """
        # Clamp volume between 0 and 1
        volume = max(0.0, min(1.0, volume))
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
