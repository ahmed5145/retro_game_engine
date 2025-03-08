"""Tests for the AudioManager class."""
import os
from pathlib import Path

import pygame
import pytest

from src.core.audio import AudioConfig, AudioManager


@pytest.fixture
def test_audio_file(tmp_path: Path) -> str:
    """Create a test audio file.

    Args:
        tmp_path: Temporary directory path

    Returns:
        Path to the test audio file
    """
    # Create a simple WAV file for testing
    sample_rate = 44100
    duration = 0.1  # 100ms
    num_samples = int(sample_rate * duration)

    # Create a silent WAV file
    pygame.mixer.init(frequency=sample_rate, size=-16, channels=1)
    sound = pygame.mixer.Sound(
        buffer=bytes(num_samples * 2)
    )  # 16-bit = 2 bytes per sample

    # Save to temporary file
    path = os.path.join(tmp_path, "test.wav")
    pygame.mixer.Sound.save(sound, path)

    return str(path)


@pytest.fixture
def audio_manager() -> AudioManager:
    """Create an AudioManager instance."""
    return AudioManager(num_channels=4)


def test_audio_manager_initialization(audio_manager: AudioManager) -> None:
    """Test AudioManager initialization."""
    assert len(audio_manager._channels) == 4
    assert len(audio_manager._clips) == 0
    assert audio_manager._master_volume == 1.0
    assert audio_manager._music_volume == 1.0
    assert audio_manager._sfx_volume == 1.0
    assert audio_manager._current_music is None


def test_load_clip(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test loading audio clips."""
    # Load clip with default config
    audio_manager.load_clip("test1", test_audio_file)
    assert "test1" in audio_manager._clips

    # Load clip with custom config
    config = AudioConfig(volume=0.5, loop=True, priority=1)
    audio_manager.load_clip("test2", test_audio_file, config)
    assert "test2" in audio_manager._clips
    assert audio_manager._clips["test2"].config == config


def test_play_sound(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test playing sound effects."""
    audio_manager.load_clip("test", test_audio_file)

    # Play sound
    channel = audio_manager.play_sound("test")
    assert channel is not None
    assert channel.get_busy()

    # Test non-existent sound
    with pytest.raises(KeyError):
        audio_manager.play_sound("non_existent")


def test_play_music(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test playing background music."""
    audio_manager.load_clip("music", test_audio_file)

    # Play music
    audio_manager.play_music("music")
    assert audio_manager._current_music is not None
    assert audio_manager._current_music.is_playing()

    # Stop music
    audio_manager.stop_music()
    assert audio_manager._current_music is None


def test_volume_control(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test volume control."""
    audio_manager.load_clip("sfx", test_audio_file)
    audio_manager.load_clip("music", test_audio_file)

    # Test master volume
    audio_manager.set_master_volume(0.5)
    assert audio_manager._master_volume == 0.5

    # Test music volume
    audio_manager.set_music_volume(0.8)
    assert audio_manager._music_volume == 0.8

    # Test sfx volume
    audio_manager.set_sfx_volume(0.6)
    assert audio_manager._sfx_volume == 0.6

    # Test volume clamping
    audio_manager.set_master_volume(1.5)
    assert audio_manager._master_volume == 1.0
    audio_manager.set_master_volume(-0.5)
    assert audio_manager._master_volume == 0.0


def test_cleanup(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test cleanup."""
    audio_manager.load_clip("test", test_audio_file)
    audio_manager.play_sound("test")

    audio_manager.cleanup()
    assert len(audio_manager._clips) == 0
    assert not pygame.mixer.get_busy()


def test_pause_resume_music(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test pausing and resuming music."""
    audio_manager.load_clip("music", test_audio_file)

    # Play and pause
    audio_manager.play_music("music")
    audio_manager.pause_music()

    # Resume
    audio_manager.resume_music()
    assert audio_manager._current_music is not None
    assert audio_manager._current_music.is_playing()


def test_stop_all(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test stopping all audio."""
    audio_manager.load_clip("sfx", test_audio_file)
    audio_manager.load_clip("music", test_audio_file)

    audio_manager.play_sound("sfx")
    audio_manager.play_music("music")

    audio_manager.stop_all()
    assert not pygame.mixer.get_busy()
    assert audio_manager._current_music is None
