"""Tests for the audio manager."""
import os
from typing import Generator
from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.core.audio import Audio


@pytest.fixture(autouse=True)
def setup_pygame_audio() -> Generator[None, None, None]:
    """Set up pygame audio for testing."""
    # Initialize pygame with dummy audio driver
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    pygame.mixer.init()
    yield None
    pygame.mixer.quit()


def test_play_sound() -> None:
    """Test playing a sound effect."""
    with patch("pygame.mixer.Sound") as mock_sound:
        # Create a mock sound object
        mock_sound_obj = MagicMock()
        mock_sound.return_value = mock_sound_obj

        # Test playing sound
        Audio.play_sound("test.wav")

        # Verify sound was created and played
        mock_sound.assert_called_once_with("test.wav")
        mock_sound_obj.play.assert_called_once()

        # Test volume setting
        Audio.play_sound("test.wav", volume=0.5)
        mock_sound_obj.set_volume.assert_called_with(0.5)


def test_play_music() -> None:
    """Test playing background music."""
    with patch("pygame.mixer.music") as mock_music:
        # Test playing music
        Audio.play_music("test.wav")

        # Verify music was loaded and played
        mock_music.load.assert_called_once_with("test.wav")
        mock_music.play.assert_called_once_with(-1)  # -1 for looping

        # Test volume setting
        Audio.play_music("test.wav", volume=0.5, loop=False)
        mock_music.set_volume.assert_called_with(0.5)
        mock_music.play.assert_called_with(0)  # 0 for no looping


def test_stop_music() -> None:
    """Test stopping background music."""
    with patch("pygame.mixer.music") as mock_music:
        # Test stopping music
        Audio.stop_music()
        mock_music.stop.assert_called_once()


def test_pause_music() -> None:
    """Test pausing background music."""
    with patch("pygame.mixer.music") as mock_music:
        # Test pausing music
        Audio.pause_music()
        mock_music.pause.assert_called_once()


def test_unpause_music() -> None:
    """Test unpausing background music."""
    with patch("pygame.mixer.music") as mock_music:
        # Test unpausing music
        Audio.unpause_music()
        mock_music.unpause.assert_called_once()


def test_set_music_volume() -> None:
    """Test setting music volume."""
    with patch("pygame.mixer.music") as mock_music:
        # Test setting volume
        Audio.set_music_volume(0.5)
        mock_music.set_volume.assert_called_once_with(0.5)

        # Test invalid volume
        with pytest.raises(ValueError):
            Audio.set_music_volume(-0.1)
        with pytest.raises(ValueError):
            Audio.set_music_volume(1.1)


def test_get_music_volume() -> None:
    """Test getting music volume."""
    with patch("pygame.mixer.music") as mock_music:
        # Mock volume return value
        mock_music.get_volume.return_value = 0.5

        # Test getting volume
        volume = Audio.get_music_volume()
        assert volume == 0.5
        mock_music.get_volume.assert_called_once()


def test_is_music_playing() -> None:
    """Test checking if music is playing."""
    with patch("pygame.mixer.music") as mock_music:
        # Mock busy state
        mock_music.get_busy.return_value = True

        # Test checking play state
        assert Audio.is_music_playing() is True
        mock_music.get_busy.assert_called_once()


def test_fade_out_music() -> None:
    """Test fading out music."""
    with patch("pygame.mixer.music") as mock_music:
        # Test fading out
        Audio.fade_out_music(1000)  # 1 second fade
        mock_music.fadeout.assert_called_once_with(1000)


def test_queue_music() -> None:
    """Test queuing next music track."""
    with patch("pygame.mixer.music") as mock_music:
        # Test queuing music
        Audio.queue_music("next.wav")
        mock_music.queue.assert_called_once_with("next.wav")


def test_set_music_position() -> None:
    """Test setting music position."""
    with patch("pygame.mixer.music") as mock_music:
        # Test setting position
        Audio.set_music_position(1.5)  # 1.5 seconds
        mock_music.set_pos.assert_called_once_with(1.5)


def test_error_handling() -> None:
    """Test error handling in audio operations."""
    with patch("pygame.mixer.Sound") as mock_sound:
        # Simulate file not found error
        mock_sound.side_effect = FileNotFoundError
        with pytest.raises(FileNotFoundError):
            Audio.play_sound("nonexistent.wav")

    with patch("pygame.mixer.music") as mock_music:
        # Simulate pygame error
        mock_music.load.side_effect = pygame.error
        with pytest.raises(pygame.error):
            Audio.play_music("invalid.wav")
