"""Utilities for audio testing."""
import os
from typing import Generator

import pygame
import pytest


def create_test_audio_file(
    path: str, duration: float = 0.1, sample_rate: int = 44100
) -> None:
    """Create a test WAV file.

    Args:
        path: Path to save the WAV file
        duration: Duration in seconds
        sample_rate: Sample rate in Hz
    """
    # Create a silent WAV file
    num_samples = int(sample_rate * duration)
    buffer = bytes(num_samples * 2)  # 16-bit = 2 bytes per sample

    # Create a temporary file with .wav extension
    with open(path, "wb") as f:
        # WAV header
        f.write(b"RIFF")  # ChunkID
        f.write((36 + len(buffer)).to_bytes(4, "little"))  # ChunkSize
        f.write(b"WAVE")  # Format
        f.write(b"fmt ")  # Subchunk1ID
        f.write((16).to_bytes(4, "little"))  # Subchunk1Size
        f.write((1).to_bytes(2, "little"))  # AudioFormat (PCM)
        f.write((1).to_bytes(2, "little"))  # NumChannels (Mono)
        f.write(sample_rate.to_bytes(4, "little"))  # SampleRate
        f.write((sample_rate * 2).to_bytes(4, "little"))  # ByteRate
        f.write((2).to_bytes(2, "little"))  # BlockAlign
        f.write((16).to_bytes(2, "little"))  # BitsPerSample
        f.write(b"data")  # Subchunk2ID
        f.write(len(buffer).to_bytes(4, "little"))  # Subchunk2Size
        f.write(buffer)  # Data


@pytest.fixture(autouse=True)
def setup_audio() -> Generator[None, None, None]:
    """Set up pygame mixer for tests."""
    try:
        # Try to initialize with default driver
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    except pygame.error:
        # If default driver fails, try dummy driver for CI environment
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except pygame.error:
            # If both fail, skip audio tests
            pytest.skip("No audio device available")

    yield
    pygame.mixer.quit()


@pytest.fixture
def test_audio_file(tmp_path: str) -> str:
    """Create a temporary test audio file.

    Args:
        tmp_path: Temporary directory path

    Returns:
        Path to the test audio file
    """
    file_path = os.path.join(tmp_path, "test.wav")
    create_test_audio_file(file_path)
    return file_path
