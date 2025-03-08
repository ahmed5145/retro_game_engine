"""Audio system manager."""
from typing import Dict, Optional

import pygame

from .audio_clip import AudioClip, AudioConfig


class AudioManager:
    """Manages audio playback and channel allocation."""

    def __init__(self, num_channels: int = 8) -> None:
        """Initialize the audio manager.

        Args:
            num_channels: Number of audio channels to allocate
        """
        # Initialize instance variables
        self._initialized = False
        self._clips: Dict[str, AudioClip] = {}
        self._channels: Dict[int, Optional[str]] = {}
        self._master_volume = 1.0
        self._music_volume = 1.0
        self._sfx_volume = 1.0
        self._current_music: Optional[str] = None

        # Initialize pygame mixer
        try:
            if pygame.mixer.get_init():
                pygame.mixer.quit()  # Ensure clean state
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            pygame.mixer.set_num_channels(num_channels)
            self._channels = {i: None for i in range(num_channels)}
            self._initialized = True
        except pygame.error:
            print("Warning: Failed to initialize audio system")

    def load_clip(
        self, name: str, path: str, config: Optional[AudioConfig] = None
    ) -> None:
        """Load an audio clip.

        Args:
            name: Identifier for the clip
            path: Path to the audio file
            config: Audio configuration
        """
        if not self._initialized:
            print("Warning: Audio system not initialized")
            return

        clip = AudioClip(path, config)
        try:
            clip.load()
            self._clips[name] = clip
        except RuntimeError as e:
            print(f"Error loading audio clip '{name}': {e}")

    def play_sound(self, name: str) -> Optional[pygame.mixer.Channel]:
        """Play a sound effect.

        Args:
            name: Name of the clip to play

        Returns:
            Channel the sound is playing on, or None if playback failed
        """
        if not self._initialized:
            return None

        if name not in self._clips:
            print(f"Warning: Audio clip '{name}' not found")
            return None

        clip = self._clips[name]
        priority = clip.config.priority if clip.config else 0

        # Find available channel
        channel = self._find_channel(priority)
        if not channel:
            return None

        # Play the sound
        try:
            channel = clip.play(channel)
            if channel:
                # Store clip name in channel mapping
                for i, ch in enumerate(self._channels):
                    if ch == channel:
                        self._channels[i] = name
                        break
            return channel
        except RuntimeError as e:
            print(f"Error playing audio clip '{name}': {e}")
            return None

    def play_music(self, name: str) -> None:
        """Play background music.

        Args:
            name: Name of the clip to play
        """
        if not self._initialized:
            return

        if name not in self._clips:
            print(f"Warning: Audio clip '{name}' not found")
            return

        # Stop current music if playing
        if self._current_music:
            self.stop_music()

        clip = self._clips[name]
        try:
            # Force looping for music
            if clip.config:
                clip.config.loop = True
            channel = clip.play()
            if channel:
                # Store clip name in channel mapping
                for i, ch in enumerate(self._channels):
                    if ch == channel:
                        self._channels[i] = name
                        break
                self._current_music = name
        except RuntimeError as e:
            print(f"Error playing music '{name}': {e}")

    def stop_music(self) -> None:
        """Stop currently playing music."""
        if not self._initialized:
            return

        if self._current_music and self._current_music in self._clips:
            self._clips[self._current_music].stop()
            self._current_music = None

    def pause_music(self) -> None:
        """Pause currently playing music."""
        if not self._initialized:
            return
        pygame.mixer.pause()

    def resume_music(self) -> None:
        """Resume paused music."""
        if not self._initialized:
            return
        pygame.mixer.unpause()

    def set_master_volume(self, volume: float) -> None:
        """Set master volume level.

        Args:
            volume: Volume level between 0.0 and 1.0
        """
        if not self._initialized:
            return
        self._master_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_music_volume(self, volume: float) -> None:
        """Set music volume level.

        Args:
            volume: Volume level between 0.0 and 1.0
        """
        if not self._initialized:
            return
        self._music_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_sfx_volume(self, volume: float) -> None:
        """Set sound effects volume level.

        Args:
            volume: Volume level between 0.0 and 1.0
        """
        if not self._initialized:
            return
        self._sfx_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def stop_all(self) -> None:
        """Stop all playing sounds."""
        if not self._initialized:
            return
        pygame.mixer.stop()
        self._current_music = None

    def _update_volumes(self) -> None:
        """Update volume levels for all channels."""
        if not self._initialized:
            return
        for name, clip in self._clips.items():
            if clip.config:
                base_volume = clip.config.volume
                if name == self._current_music:
                    clip.set_volume(
                        base_volume * self._master_volume * self._music_volume
                    )
                else:
                    clip.set_volume(
                        base_volume * self._master_volume * self._sfx_volume
                    )

    def _find_channel(self, priority: int) -> Optional[pygame.mixer.Channel]:
        """Find an available channel for playback.

        Args:
            priority: Priority level for channel allocation

        Returns:
            Available channel or None if no channel is available
        """
        if not self._initialized:
            return None

        # First try to find a free channel
        for i in range(pygame.mixer.get_num_channels()):
            channel = pygame.mixer.Channel(i)
            if not channel.get_busy():
                return channel

        # If no free channel, try to find one with lower priority
        lowest_priority = priority
        lowest_channel = None

        for i in range(pygame.mixer.get_num_channels()):
            channel = pygame.mixer.Channel(i)
            clip_name = self._channels.get(i)
            if clip_name and clip_name in self._clips:
                clip = self._clips[clip_name]
                if clip.config and clip.config.priority < lowest_priority:
                    lowest_priority = clip.config.priority
                    lowest_channel = channel

        return lowest_channel

    def cleanup(self) -> None:
        """Clean up audio resources."""
        if not self._initialized:
            return
        self.stop_all()
        for clip in self._clips.values():
            clip.unload()
        self._clips.clear()
        self._channels.clear()
        pygame.mixer.quit()
