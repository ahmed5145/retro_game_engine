"""Audio manager for handling sound effects and music."""
from typing import Dict, Optional

import pygame

from .audio_clip import AudioClip


class AudioManager:
    """Manages audio playback and resources."""

    def __init__(self) -> None:
        """Initialize audio manager."""
        pygame.mixer.init()
        self._clips: Dict[str, AudioClip] = {}
        self._channels: Dict[int, pygame.mixer.Channel] = {}
        self._master_volume = 1.0
        self._music_volume = 1.0
        self._sound_volume = 1.0
        self._next_channel_id = 0

    @property
    def master_volume(self) -> float:
        """Get master volume.

        Returns:
            Master volume level (0.0 to 1.0)
        """
        return self._master_volume

    @property
    def music_volume(self) -> float:
        """Get music volume.

        Returns:
            Music volume level (0.0 to 1.0)
        """
        return self._music_volume

    @property
    def sound_volume(self) -> float:
        """Get sound effects volume.

        Returns:
            Sound effects volume level (0.0 to 1.0)
        """
        return self._sound_volume

    def load_clip(self, path: str) -> Optional[AudioClip]:
        """Load an audio clip.

        Args:
            path: Path to audio file

        Returns:
            Loaded audio clip, or None if loading failed
        """
        try:
            clip = AudioClip(path)
            clip.load()
            self._clips[path] = clip
            return clip
        except Exception:
            return None

    def play_sound(self, clip: AudioClip) -> Optional[pygame.mixer.Channel]:
        """Play a sound effect.

        Args:
            clip: Audio clip to play

        Returns:
            Channel the sound is playing on, or None if playback failed
        """
        if not clip:
            return None

        # Find available channel
        channel = pygame.mixer.find_channel()
        if not channel:
            return None

        channel.set_volume(self._sound_volume * self._master_volume)
        result = clip.play(channel)
        if result:
            # Store channel with auto-incrementing ID
            self._channels[self._next_channel_id] = channel
            self._next_channel_id += 1
            return result
        return None

    def play_music(self, path: str) -> None:
        """Play background music."""
        if path not in self._clips:
            clip = self.load_clip(path)
            if not clip:
                return

        clip = self._clips[path]
        pygame.mixer.music.load(clip.path)
        pygame.mixer.music.set_volume(self._music_volume * self._master_volume)
        pygame.mixer.music.play(-1)  # Loop indefinitely

    def stop_music(self) -> None:
        """Stop background music."""
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def pause_music(self) -> None:
        """Pause background music."""
        pygame.mixer.music.pause()

    def unpause_music(self) -> None:
        """Resume background music."""
        pygame.mixer.music.unpause()

    def resume_music(self) -> None:
        """Resume background music (alias for unpause_music)."""
        self.unpause_music()

    def set_master_volume(self, volume: float) -> None:
        """Set master volume level.

        Args:
            volume: Volume level (0.0 to 1.0)

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
            volume: Volume level (0.0 to 1.0)

        Raises:
            ValueError: If volume is not between 0.0 and 1.0
        """
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0")
        self._music_volume = volume
        self._update_volumes()

    def set_sound_volume(self, volume: float) -> None:
        """Set sound effects volume level.

        Args:
            volume: Volume level (0.0 to 1.0)

        Raises:
            ValueError: If volume is not between 0.0 and 1.0
        """
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0")
        self._sound_volume = volume
        self._update_volumes()

    def _update_volumes(self) -> None:
        """Update all audio volumes."""
        # Update music volume
        pygame.mixer.music.set_volume(self._music_volume * self._master_volume)

        # Update sound effect volumes
        for channel in self._channels.values():
            channel.set_volume(self._sound_volume * self._master_volume)

    def cleanup(self) -> None:
        """Clean up audio resources."""
        # Stop all sounds first
        self.stop_all()

        # Stop and unload music
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        # Unload all clips
        for clip in self._clips.values():
            clip.unload()
        self._clips.clear()
        self._channels.clear()

        # Quit mixer last
        pygame.mixer.quit()

        # Reinitialize mixer for future use
        pygame.mixer.init()

    def stop_all(self) -> None:
        """Stop all sounds and music."""
        # Stop music first
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        # Then stop all sound effects
        for channel in self._channels.values():
            channel.stop()
        self._channels.clear()
