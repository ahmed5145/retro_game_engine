"""Tests for the AudioManager class."""
import pygame
import pytest

from src.core.audio import AudioConfig, AudioManager
from tests.unit.core.audio.test_utils import (  # Import fixtures
    setup_audio,
    test_audio_file,
)


@pytest.fixture
def audio_manager() -> AudioManager:
    """Create an audio manager for testing."""
    return AudioManager(num_channels=4)


def test_audio_manager_initialization(audio_manager: AudioManager) -> None:
    """Test audio manager initialization."""
    assert len(audio_manager._channels) == 4
    assert audio_manager._master_volume == 1.0
    assert audio_manager._music_volume == 1.0
    assert audio_manager._sfx_volume == 1.0
    assert audio_manager._current_music is None


def test_load_clip(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test loading audio clips."""
    # Test loading valid clip
    audio_manager.load_clip("test", test_audio_file)
    assert "test" in audio_manager._clips

    # Test loading with config
    config = AudioConfig(volume=0.5, loop=True)
    audio_manager.load_clip("test2", test_audio_file, config)
    assert "test2" in audio_manager._clips
    assert audio_manager._clips["test2"].config == config

    # Test loading invalid file
    audio_manager.load_clip("invalid", "nonexistent.wav")
    assert "invalid" not in audio_manager._clips


def test_play_sound(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test playing sound effects."""
    # Load test clip
    audio_manager.load_clip("test", test_audio_file)

    # Test playing valid sound
    channel = audio_manager.play_sound("test")
    assert channel is not None
    assert channel.get_busy()

    # Test playing non-existent sound
    channel = audio_manager.play_sound("nonexistent")
    assert channel is None


def test_play_music(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test playing background music."""
    # Load test clip
    audio_manager.load_clip("music", test_audio_file)

    # Test playing music
    audio_manager.play_music("music")
    assert audio_manager._current_music == "music"

    # Test playing different music
    audio_manager.load_clip("music2", test_audio_file)
    audio_manager.play_music("music2")
    assert audio_manager._current_music == "music2"

    # Test playing non-existent music
    audio_manager.play_music("nonexistent")
    assert audio_manager._current_music == "music2"  # Should not change


def test_volume_control(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test volume control."""
    # Load test clips
    audio_manager.load_clip("sfx", test_audio_file)
    audio_manager.load_clip("music", test_audio_file)

    # Test master volume
    audio_manager.set_master_volume(0.5)
    assert audio_manager._master_volume == 0.5

    # Test music volume
    audio_manager.set_music_volume(0.7)
    assert audio_manager._music_volume == 0.7

    # Test sfx volume
    audio_manager.set_sfx_volume(0.3)
    assert audio_manager._sfx_volume == 0.3

    # Test volume clamping
    audio_manager.set_master_volume(1.5)
    assert audio_manager._master_volume == 1.0

    audio_manager.set_master_volume(-0.5)
    assert audio_manager._master_volume == 0.0


def test_music_controls(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test music playback controls."""
    # Load and play music
    audio_manager.load_clip("music", test_audio_file)
    audio_manager.play_music("music")

    # Test pause/resume
    audio_manager.pause_music()
    # Would test channel state here if we had access to it

    audio_manager.resume_music()
    # Would test channel state here if we had access to it

    # Test stop
    audio_manager.stop_music()
    assert audio_manager._current_music is None


def test_channel_allocation(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test channel allocation strategy."""
    # Load test clips with different priorities
    config_low = AudioConfig(priority=1)
    config_high = AudioConfig(priority=10)

    audio_manager.load_clip("low", test_audio_file, config_low)
    audio_manager.load_clip("high", test_audio_file, config_high)

    # Fill all channels with low priority sounds
    channels = []
    for _ in range(4):
        channel = audio_manager.play_sound("low")
        assert channel is not None
        channels.append(channel)

    # Play high priority sound - should replace a low priority one
    channel = audio_manager.play_sound("high")
    assert channel is not None


def test_cleanup(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test cleanup."""
    # Load and play some clips
    audio_manager.load_clip("test", test_audio_file)
    audio_manager.play_sound("test")

    # Cleanup
    audio_manager.cleanup()
    assert len(audio_manager._clips) == 0
    assert len(audio_manager._channels) == 0


def test_stop_all(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test stopping all sounds."""
    # Load and play clips
    audio_manager.load_clip("sfx", test_audio_file)
    audio_manager.load_clip("music", test_audio_file)

    audio_manager.play_sound("sfx")
    audio_manager.play_music("music")

    # Stop all
    audio_manager.stop_all()
    assert audio_manager._current_music is None
    # Would verify all channels are stopped if we had access to them
