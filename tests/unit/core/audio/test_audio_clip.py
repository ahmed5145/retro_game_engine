"""Tests for the AudioClip class."""
import os
import wave
from typing import Generator

import pygame
import pytest

from src.core.audio import AudioClip, AudioClipConfig


@pytest.fixture
def test_audio_file(tmp_path: str) -> Generator[str, None, None]:
    """Create a test WAV file."""
    file_path = os.path.join(tmp_path, "test.wav")

    # Create a simple WAV file
    with wave.open(file_path, "w") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(44100)  # 44.1kHz
        wav_file.writeframes(b"\x00" * 44100)  # 1 second of silence

    yield file_path

    # Cleanup
    if os.path.exists(file_path):
        os.remove(file_path)


def test_audio_clip_initialization(test_audio_file: str) -> None:
    """Test audio clip initialization."""
    clip = AudioClip(test_audio_file)
    assert clip.path == test_audio_file
    assert clip.config == AudioClipConfig()
    assert clip._sound is None
    assert clip._channel is None


def test_audio_clip_load(test_audio_file: str) -> None:
    """Test loading an audio clip."""
    clip = AudioClip(test_audio_file)
    clip.load()
    assert clip._sound is not None

    # Test loading again (should not raise)
    clip.load()


def test_audio_clip_play(test_audio_file: str) -> None:
    """Test playing an audio clip."""
    clip = AudioClip(test_audio_file)
    clip.load()

    # Play without specific channel
    channel = clip.play()
    assert channel is not None
    assert clip.is_playing()

    # Stop and verify
    clip.stop()
    assert not clip.is_playing()

    # Play on specific channel
    specific_channel = pygame.mixer.Channel(0)
    channel = clip.play(specific_channel)
    assert channel == specific_channel
    assert clip.is_playing()


def test_audio_clip_volume(test_audio_file: str) -> None:
    """Test volume control."""
    clip = AudioClip(test_audio_file)
    clip.load()

    # Test valid volume values
    clip.set_volume(0.5)
    assert clip.config.volume == 0.5
    if clip._sound is not None:
        assert abs(clip._sound.get_volume() - 0.5) < 0.001

    # Test volume clamping
    with pytest.raises(ValueError):
        clip.set_volume(1.5)  # Should raise ValueError

    with pytest.raises(ValueError):
        clip.set_volume(-0.5)  # Should raise ValueError


def test_audio_clip_unload(test_audio_file: str) -> None:
    """Test unloading an audio clip."""
    clip = AudioClip(test_audio_file)
    clip.load()

    # Play and then unload
    channel = clip.play()
    assert channel is not None

    clip.stop()  # Stop before unloading
    clip.unload()
    assert clip._sound is None
    assert clip._channel is None


def test_audio_clip_error_handling(test_audio_file: str) -> None:
    """Test error handling in audio clip."""
    # Test loading non-existent file
    clip = AudioClip("nonexistent.wav")
    with pytest.raises(FileNotFoundError):
        clip.load()

    # Test playing without loading
    clip = AudioClip(test_audio_file)
    with pytest.raises(RuntimeError):
        clip.play()


def test_audio_clip_invalid_volume(test_audio_file: str) -> None:
    """Test setting invalid volume values."""
    clip = AudioClip(test_audio_file)
    clip.load()

    # Test invalid volume values
    with pytest.raises(ValueError):
        clip.set_volume(float("inf"))

    with pytest.raises(ValueError):
        clip.set_volume(float("nan"))

    with pytest.raises(ValueError):
        clip.set_volume(-1.0)
