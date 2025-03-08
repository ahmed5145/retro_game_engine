"""Tests for the AudioClip class."""
import os
from pathlib import Path
import pytest
import pygame
from src.core.audio import AudioClip, AudioConfig

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
    sound = pygame.mixer.Sound(buffer=bytes(num_samples * 2))  # 16-bit = 2 bytes per sample
    
    # Save to temporary file
    path = os.path.join(tmp_path, "test.wav")
    pygame.mixer.Sound.save(sound, path)
    
    return str(path)

def test_audio_clip_initialization(test_audio_file: str) -> None:
    """Test AudioClip initialization."""
    config = AudioConfig(volume=0.5, loop=True, priority=1)
    clip = AudioClip(test_audio_file, config)
    
    assert clip.path == test_audio_file
    assert clip.config == config
    assert not clip._loaded
    assert clip._sound is None
    assert clip._channel is None

def test_audio_clip_load(test_audio_file: str) -> None:
    """Test loading an audio clip."""
    clip = AudioClip(test_audio_file)
    clip.load()
    
    assert clip._loaded
    assert clip._sound is not None
    assert isinstance(clip._sound, pygame.mixer.Sound)

def test_audio_clip_play(test_audio_file: str) -> None:
    """Test playing an audio clip."""
    clip = AudioClip(test_audio_file)
    clip.load()
    
    # Play the clip
    channel = clip.play()
    assert channel is not None
    assert clip.is_playing()
    
    # Stop the clip
    clip.stop()
    assert not clip.is_playing()
    assert clip._channel is None

def test_audio_clip_volume(test_audio_file: str) -> None:
    """Test volume control."""
    clip = AudioClip(test_audio_file)
    clip.load()
    
    # Test volume setting
    clip.set_volume(0.5)
    assert clip.config.volume == 0.5
    
    # Test volume clamping
    clip.set_volume(1.5)
    assert clip.config.volume == 1.0
    clip.set_volume(-0.5)
    assert clip.config.volume == 0.0

def test_audio_clip_unload(test_audio_file: str) -> None:
    """Test unloading an audio clip."""
    clip = AudioClip(test_audio_file)
    clip.load()
    assert clip._loaded
    
    clip.unload()
    assert not clip._loaded
    assert clip._sound is None

def test_audio_clip_error_handling(test_audio_file: str) -> None:
    """Test error handling."""
    # Test playing before loading
    clip = AudioClip(test_audio_file)
    with pytest.raises(RuntimeError):
        clip.play()
    
    # Test loading non-existent file
    clip = AudioClip("non_existent.wav")
    with pytest.raises(pygame.error):
        clip.load() 