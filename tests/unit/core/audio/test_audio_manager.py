"""Tests for the AudioManager class."""
import os
import wave
from pathlib import Path
from typing import Generator

import pygame
import pytest

from src.core.audio.audio_clip import AudioClip
from src.core.audio.audio_manager import AudioManager


@pytest.fixture(autouse=True)
def setup_audio() -> Generator[None, None, None]:
    """Set up audio for testing."""
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    pygame.mixer.init()
    yield None
    pygame.mixer.quit()


@pytest.fixture
def audio_manager() -> Generator[AudioManager, None, None]:
    """Create an AudioManager instance for testing."""
    # Set dummy audio driver before any pygame initialization
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.environ["SDL_VIDEODRIVER"] = "dummy"

    try:
        pygame.mixer.init()
        manager = AudioManager()
        yield manager
    except pygame.error as e:
        pytest.skip(f"Could not initialize audio: {e}")
    finally:
        try:
            pygame.mixer.quit()
        except pygame.error:
            pass


@pytest.fixture
def test_audio_file() -> Generator[str, None, None]:
    """Create a test audio file."""
    test_file = "test.wav"
    if not os.path.exists(test_file):
        # Create a simple WAV file for testing
        with wave.open(test_file, "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(44100)  # 44.1kHz
            wav_file.writeframes(b"\x00" * 44100)  # 1 second of silence
    yield test_file
    # Stop any playing music and unload it
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        # Small delay to ensure resources are released
        pygame.time.wait(100)
    except pygame.error:
        pass
    if os.path.exists(test_file):
        os.remove(test_file)


def test_audio_manager_initialization() -> None:
    """Test AudioManager initialization."""
    # Set dummy audio driver before any pygame initialization
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.environ["SDL_VIDEODRIVER"] = "dummy"

    try:
        pygame.mixer.init()
        manager = AudioManager()
        assert manager is not None
    except pygame.error as e:
        pytest.skip(f"Could not initialize audio: {e}")
    finally:
        try:
            pygame.mixer.quit()
        except pygame.error:
            pass


def test_load_clip(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test loading an audio clip."""
    clip = audio_manager.load_clip(path=test_audio_file)
    assert clip is not None
    assert isinstance(clip, AudioClip)


def test_play_sound(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test playing a sound effect."""
    clip = audio_manager.load_clip(path=test_audio_file)
    assert clip is not None, "Failed to load audio clip"
    channel = audio_manager.play_sound(clip)
    assert channel is not None
    assert channel.get_busy()


def test_play_music(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test playing music."""
    audio_manager.play_music(test_audio_file)
    assert pygame.mixer.music.get_busy()


def test_music_controls(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test music playback controls."""
    audio_manager.play_music(test_audio_file)
    assert pygame.mixer.music.get_busy()

    audio_manager.pause_music()
    assert not pygame.mixer.music.get_busy()

    audio_manager.resume_music()
    assert pygame.mixer.music.get_busy()

    audio_manager.stop_music()
    assert not pygame.mixer.music.get_busy()


def test_volume_control(audio_manager: AudioManager) -> None:
    """Test volume control."""
    # Test master volume
    audio_manager.set_master_volume(0.5)
    assert audio_manager._master_volume == 0.5

    # Test music volume
    audio_manager.set_music_volume(0.7)
    assert audio_manager._music_volume == 0.7

    # Test sound volume
    audio_manager.set_sound_volume(0.3)
    assert audio_manager._sound_volume == 0.3

    # Test invalid values
    with pytest.raises(ValueError):
        audio_manager.set_master_volume(-0.1)
    with pytest.raises(ValueError):
        audio_manager.set_music_volume(1.1)
    with pytest.raises(ValueError):
        audio_manager.set_sound_volume(float("inf"))


def test_channel_allocation(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test channel allocation for sound effects."""
    clip = audio_manager.load_clip(path=test_audio_file)
    assert clip is not None, "Failed to load audio clip"
    channels = []
    # Play multiple sounds
    for _ in range(pygame.mixer.get_num_channels()):
        channel = audio_manager.play_sound(clip)
        if channel is not None:
            channels.append(channel)

    # All channels should be busy
    assert len(channels) > 0
    assert all(channel.get_busy() for channel in channels)


def test_stop_all(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test stopping all sounds."""
    clip = audio_manager.load_clip(path=test_audio_file)
    assert clip is not None, "Failed to load audio clip"
    channels = []
    # Play multiple sounds
    for _ in range(4):
        channel = audio_manager.play_sound(clip)
        if channel is not None:
            channels.append(channel)

    # Stop all sounds
    audio_manager.stop_all()
    assert all(not channel.get_busy() for channel in channels)


def test_cleanup(audio_manager: AudioManager, test_audio_file: str) -> None:
    """Test cleanup of audio resources."""
    clip = audio_manager.load_clip(path=test_audio_file)
    assert clip is not None, "Failed to load audio clip"
    audio_manager.play_sound(clip)
    audio_manager.play_music(test_audio_file)

    # Cleanup should stop all sounds and music
    audio_manager.cleanup()
    assert not pygame.mixer.music.get_busy()
    assert not any(
        pygame.mixer.Channel(i).get_busy()
        for i in range(pygame.mixer.get_num_channels())
    )
