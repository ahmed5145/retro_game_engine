"""Tests for the AudioClip class."""
import pygame
import pytest

from src.core.audio import AudioClip, AudioConfig
from tests.unit.core.audio.test_utils import (  # Import fixtures
    setup_audio,
    test_audio_file,
)


def test_audio_clip_initialization(test_audio_file: str) -> None:
    """Test audio clip initialization."""
    config = AudioConfig(volume=0.5, loop=True, priority=1)
    clip = AudioClip(test_audio_file, config)

    assert clip.path == test_audio_file
    assert clip.config == config
    assert clip._sound is None
    assert clip._channel is None


def test_audio_clip_load(test_audio_file: str) -> None:
    """Test loading an audio clip."""
    clip = AudioClip(test_audio_file)
    clip.load()

    assert clip._sound is not None
    assert isinstance(clip._sound, pygame.mixer.Sound)


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

    # Test volume setting
    clip.set_volume(0.5)
    assert clip.config.volume == 0.5
    if clip._sound is not None:
        assert abs(clip._sound.get_volume() - 0.5) < 0.001

    # Test volume clamping
    clip.set_volume(1.5)  # Should clamp to 1.0
    assert clip.config.volume == 1.0
    if clip._sound is not None:
        assert abs(clip._sound.get_volume() - 1.0) < 0.001

    clip.set_volume(-0.5)  # Should clamp to 0.0
    assert clip.config.volume == 0.0
    if clip._sound is not None:
        assert abs(clip._sound.get_volume() - 0.0) < 0.001


def test_audio_clip_unload(test_audio_file: str) -> None:
    """Test unloading an audio clip."""
    clip = AudioClip(test_audio_file)
    clip.load()

    # Play and then unload
    channel = clip.play()
    assert channel is not None

    clip.unload()
    assert clip._sound is None
    assert clip._channel is None
    assert not clip.is_playing()


def test_audio_clip_error_handling(test_audio_file: str) -> None:
    """Test error handling in audio clip."""
    # Test loading non-existent file
    clip = AudioClip("nonexistent.wav")
    with pytest.raises(RuntimeError):
        clip.load()

    # Test playing without loading
    clip = AudioClip(test_audio_file)
    with pytest.raises(RuntimeError):
        clip.play()


def test_audio_clip_config_defaults() -> None:
    """Test audio clip configuration defaults."""
    clip = AudioClip("test.wav")
    assert clip.config is not None
    assert clip.config.volume == 1.0
    assert not clip.config.loop
    assert clip.config.priority == 0


def test_audio_clip_play_while_playing(test_audio_file: str) -> None:
    """Test playing a clip that's already playing."""
    clip = AudioClip(test_audio_file)
    clip.load()

    # First play
    channel1 = clip.play()
    assert channel1 is not None

    # Second play should stop first and start new
    channel2 = clip.play()
    assert channel2 is not None
    assert not channel1.get_busy()  # First play should be stopped


def test_audio_clip_play_looping(test_audio_file: str) -> None:
    """Test playing a looping audio clip."""
    config = AudioConfig(loop=True)
    clip = AudioClip(test_audio_file, config)
    clip.load()

    channel = clip.play()
    assert channel is not None
    assert clip.is_playing()

    # Verify loop setting was applied
    assert channel.get_endevent() == -1  # No end event means looping


def test_audio_clip_invalid_volume(test_audio_file: str) -> None:
    """Test setting invalid volume values."""
    clip = AudioClip(test_audio_file)
    clip.load()

    # Test invalid volume values
    clip.set_volume(float("inf"))
    assert clip.config.volume == 1.0

    clip.set_volume(float("nan"))
    assert clip.config.volume == 1.0

    clip.set_volume(float("-inf"))
    assert clip.config.volume == 0.0
