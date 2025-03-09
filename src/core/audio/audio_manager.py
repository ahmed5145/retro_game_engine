"""Audio system manager."""
from typing import Dict, List, Optional

import pygame

from .audio_clip import AudioClip, AudioConfig


class AudioManager:
    """Manages audio playback and channel allocation."""

    def __init__(self, num_channels: int = 8) -> None:
        """Initialize the audio manager.

        Args:
            num_channels: Number of audio channels to allocate
        """
        # Initialize pygame mixer if not already done
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            except pygame.error as e:
                print(f"Failed to initialize audio system: {e}")
                return

        # Configure channels
        pygame.mixer.set_num_channels(num_channels)

        # Initialize state
        self._clips: Dict[str, AudioClip] = {}
        self._master_volume: float = 1.0
        self._music_volume: float = 1.0
        self._sfx_volume: float = 1.0
        self._current_music: Optional[str] = None
        self._channels: List[pygame.mixer.Channel] = [
            pygame.mixer.Channel(i) for i in range(num_channels)
        ]

    def load_clip(
        self, name: str, path: str, config: Optional[AudioConfig] = None
    ) -> None:
        """Load an audio clip.

        Args:
            name: Name to reference the clip by
            path: Path to the audio file
            config: Optional configuration for the clip

        Raises:
            ValueError: If a clip with the given name already exists
        """
        if name in self._clips:
            raise ValueError(f"Audio clip '{name}' already exists")

        clip = AudioClip(path, config)
        try:
            clip.load()
            self._clips[name] = clip
        except RuntimeError as e:
            print(f"Failed to load audio clip '{name}': {e}")

    def play_sound(
        self, name: str, channel: Optional[pygame.mixer.Channel] = None
    ) -> Optional[pygame.mixer.Channel]:
        """Play a sound effect.

        Args:
            name: Name of the clip to play
            channel: Optional specific channel to play on

        Returns:
            Channel the sound is playing on, or None if playback failed

        Raises:
            KeyError: If the clip doesn't exist
        """
        if name not in self._clips:
            raise KeyError(f"Audio clip '{name}' not found")

        clip = self._clips[name]

        # Try to find a channel if none specified
        if not channel:
            channel = self._find_channel(clip.config.priority)

        # Play the sound
        if channel:
            channel = clip.play(channel)
            if channel:
                channel.set_volume(self._sfx_volume * self._master_volume)
                return channel

        return None

    def play_music(self, name: str) -> None:
        """Play background music.

        Args:
            name: Name of the clip to play as music

        Raises:
            KeyError: If the clip doesn't exist
        """
        if name not in self._clips:
            raise KeyError(f"Audio clip '{name}' not found")

        clip = self._clips[name]

        try:
            if clip._sound:
                pygame.mixer.music.load(clip.path)
                pygame.mixer.music.set_volume(
                    clip.config.volume * self._music_volume * self._master_volume
                )
                pygame.mixer.music.play(-1 if clip.config.loop else 0)
        except pygame.error as e:
            print(f"Failed to play music '{name}': {e}")

    def stop_music(self) -> None:
        """Stop currently playing music."""
        try:
            pygame.mixer.music.stop()
        except pygame.error as e:
            print(f"Failed to stop music: {e}")

    def pause_music(self) -> None:
        """Pause currently playing music."""
        pygame.mixer.music.pause()

    def resume_music(self) -> None:
        """Resume paused music."""
        pygame.mixer.music.unpause()

    def set_master_volume(self, volume: float) -> None:
        """Set master volume level.

        Args:
            volume: Volume level between 0.0 and 1.0

        Raises:
            ValueError: If volume is not between 0.0 and 1.0
        """
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0")

        self._master_volume = volume
        self._update_volumes()

    def set_music_volume(self, volume: float) -> None:
        """Set music volume level.

        Args:
            volume: Volume level between 0.0 and 1.0

        Raises:
            ValueError: If volume is not between 0.0 and 1.0
        """
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0")

        self._music_volume = volume
        self._update_volumes()

    def set_sfx_volume(self, volume: float) -> None:
        """Set sound effects volume level.

        Args:
            volume: Volume level between 0.0 and 1.0

        Raises:
            ValueError: If volume is not between 0.0 and 1.0
        """
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0")

        self._sfx_volume = volume
        self._update_volumes()

    def stop_all(self) -> None:
        """Stop all playing sounds and music."""
        pygame.mixer.stop()
        self.stop_music()

    def _update_volumes(self) -> None:
        """Update volume levels for all active sounds."""
        # Update music volume
        try:
            pygame.mixer.music.set_volume(self._music_volume * self._master_volume)
        except pygame.error:
            pass

        # Update sound effect volumes
        for channel in self._channels:
            if channel.get_busy():
                channel.set_volume(self._sfx_volume * self._master_volume)

    def _find_channel(self, priority: int = 0) -> Optional[pygame.mixer.Channel]:
        """Find an available channel for playback.

        Args:
            priority: Priority level for channel allocation

        Returns:
            Available channel, or None if none available
        """
        # Try to find a free channel
        channel = pygame.mixer.find_channel()
        if channel:
            return channel

        # If no free channels and priority is 0, give up
        if priority == 0:
            return None

        # Look for a channel playing a lower priority sound
        lowest_priority = priority
        lowest_channel = None

        for i in range(pygame.mixer.get_num_channels()):
            channel = pygame.mixer.Channel(i)
            if channel in self._channels:
                chan_priority = self._channels.index(channel)
                if chan_priority < lowest_priority:
                    lowest_priority = chan_priority
                    lowest_channel = channel

        # Stop the lowest priority sound if found
        if lowest_channel:
            lowest_channel.stop()
            return lowest_channel

        return None

    def cleanup(self) -> None:
        """Clean up audio resources."""
        self.stop_all()
        for clip in self._clips.values():
            clip.unload()
        self._clips.clear()
        self._channels.clear()
