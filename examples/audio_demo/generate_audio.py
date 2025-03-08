"""Generate placeholder WAV files for testing."""
import os
from typing import Any
import numpy as np
from scipy.io import wavfile

def generate_sine_wave(frequency: float, duration: float, sample_rate: int = 44100) -> Any:
    """Generate a sine wave.
    
    Args:
        frequency: Frequency in Hz
        duration: Duration in seconds
        sample_rate: Sample rate in Hz
        
    Returns:
        Numpy array containing the audio samples
    """
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    samples = np.sin(2 * np.pi * frequency * t)
    return (samples * 32767).astype(np.int16)

def generate_background_music(output_path: str) -> None:
    """Generate a simple background music track."""
    sample_rate = 44100
    duration = 5.0  # 5 seconds
    
    # Generate a simple melody
    melody = generate_sine_wave(440, duration)  # A4 note
    harmony = generate_sine_wave(554.37, duration)  # C#5 note
    bass = generate_sine_wave(220, duration)  # A3 note
    
    # Mix the tracks
    mixed = (melody + harmony + bass) // 3
    
    # Save to file
    wavfile.write(output_path, sample_rate, mixed)

def generate_jump_sound(output_path: str) -> None:
    """Generate a jump sound effect."""
    sample_rate = 44100
    duration = 0.3  # 300ms
    
    # Generate a rising frequency sweep
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    frequency = 440 + 880 * t / duration
    samples = np.sin(2 * np.pi * frequency * t)
    
    # Apply envelope
    envelope = np.exp(-4 * t / duration)
    samples = samples * envelope
    
    # Convert to 16-bit PCM
    samples = (samples * 32767).astype(np.int16)
    
    # Save to file
    wavfile.write(output_path, sample_rate, samples)

def generate_coin_sound(output_path: str) -> None:
    """Generate a coin collection sound effect."""
    sample_rate = 44100
    duration = 0.2  # 200ms
    
    # Generate two tones
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone1 = np.sin(2 * np.pi * 880 * t)  # A5
    tone2 = np.sin(2 * np.pi * 1108.73 * t)  # C#6
    
    # Mix tones and apply envelope
    samples = (tone1 + tone2) / 2
    envelope = np.exp(-8 * t / duration)
    samples = samples * envelope
    
    # Convert to 16-bit PCM
    samples = (samples * 32767).astype(np.int16)
    
    # Save to file
    wavfile.write(output_path, sample_rate, samples)

def main() -> None:
    """Generate all audio files."""
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # Generate audio files
    generate_background_music(os.path.join(assets_dir, "background.wav"))
    generate_jump_sound(os.path.join(assets_dir, "jump.wav"))
    generate_coin_sound(os.path.join(assets_dir, "coin.wav"))
    
    print("Audio files generated successfully!")

if __name__ == "__main__":
    main() 