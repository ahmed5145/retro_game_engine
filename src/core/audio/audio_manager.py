"""Audio management system for handling sound effects and music."""
from typing import Dict, Optional
import pygame
from .audio_clip import AudioClip, AudioConfig

class AudioManager:
    """Manages audio playback and channel allocation."""

    def __init__(self, num_channels: int = 8) -> None:
        """Initialize the audio manager.
        
        Args:
            num_channels: Number of audio channels to allocate (default: 8)
            
        Raises:
            pygame.error: If pygame.mixer cannot be initialized
        """
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # Set up channels
        pygame.mixer.set_num_channels(num_channels)
        self._channels = [pygame.mixer.Channel(i) for i in range(num_channels)]

        # Audio clips
        self._clips: Dict[str, AudioClip] = {}

        # Volume settings
        self._master_volume = 1.0
        self._music_volume = 1.0
        self._sfx_volume = 1.0

        # Current background music
        self._current_music: Optional[AudioClip] = None

    def load_clip(self, name: str, path: str, config: Optional[AudioConfig] = None) -> None:
        """Load an audio clip.
        
        Args:
            name: Name to reference the clip by
            path: Path to the audio file
            config: Optional configuration for the clip
            
        Raises:
            pygame.error: If the audio file cannot be loaded
        """
        clip = AudioClip(path, config)
        clip.load()
        self._clips[name] = clip

    def play_sound(self, name: str) -> Optional[pygame.mixer.Channel]:
        """Play a sound effect.
        
        Args:
            name: Name of the clip to play
            
        Returns:
            Channel the sound is playing on, or None if playback failed
            
        Raises:
            KeyError: If the clip doesn't exist
        """
        if name not in self._clips:
            raise KeyError(f"Audio clip '{name}' not found")

        clip = self._clips[name]

        # Find a free channel or one with lower priority
        channel = self._find_channel(clip.config.priority)
        if channel:
            return clip.play(channel)
        return None

    def play_music(self, name: str) -> None:
        """Play background music.
        
        Args:
            name: Name of the clip to play
            
        Raises:
            KeyError: If the clip doesn't exist
        """
        if name not in self._clips:
            raise KeyError(f"Audio clip '{name}' not found")

        # Stop current music if any
        if self._current_music:
            self._current_music.stop()

        # Play new music
        clip = self._clips[name]
        clip.config.loop = True  # Music should loop by default
        clip.play()
        self._current_music = clip

    def stop_music(self) -> None:
        """Stop the currently playing background music."""
        if self._current_music:
            self._current_music.stop()
            self._current_music = None

    def pause_music(self) -> None:
        """Pause the currently playing background music."""
        if self._current_music and self._current_music.is_playing():
            pygame.mixer.pause()

    def resume_music(self) -> None:
        """Resume the paused background music."""
        if self._current_music:
            pygame.mixer.unpause()

    def set_master_volume(self, volume: float) -> None:
        """Set the master volume level.
        
        Args:
            volume: Volume level from 0.0 to 1.0
        """
        self._master_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_music_volume(self, volume: float) -> None:
        """Set the music volume level.
        
        Args:
            volume: Volume level from 0.0 to 1.0
        """
        self._music_volume = max(0.0, min(1.0, volume))
        if self._current_music:
            self._current_music.set_volume(self._master_volume * self._music_volume)

    def set_sfx_volume(self, volume: float) -> None:
        """Set the sound effects volume level.
        
        Args:
            volume: Volume level from 0.0 to 1.0
        """
        self._sfx_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def stop_all(self) -> None:
        """Stop all playing audio."""
        pygame.mixer.stop()
        self._current_music = None

    def _update_volumes(self) -> None:
        """Update volume levels for all playing sounds."""
        for clip in self._clips.values():
            if clip != self._current_music and clip.is_playing():
                clip.set_volume(self._master_volume * self._sfx_volume)

    def _find_channel(self, priority: int) -> Optional[pygame.mixer.Channel]:
        """Find a free channel or one with lower priority.
        
        Args:
            priority: Priority level of the sound to play
            
        Returns:
            Available channel or None if none found
        """
        # First try to find a free channel
        for channel in self._channels:
            if not channel.get_busy():
                return channel

        # If no free channels, look for one with lower priority
        lowest_priority = priority
        lowest_channel = None

        for channel in self._channels:
            # TODO: Track priorities of playing sounds to implement this properly
            if not lowest_channel:
                lowest_channel = channel

        return lowest_channel

    def cleanup(self) -> None:
        """Clean up audio resources."""
        self.stop_all()
        for clip in self._clips.values():
            clip.unload()
        self._clips.clear()
        pygame.mixer.quit()
