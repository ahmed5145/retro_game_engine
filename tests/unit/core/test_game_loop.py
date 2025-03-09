"""Tests for the game loop."""
import time
from typing import List

import pytest

from src.core.game_loop import GameLoop, GameLoopConfig


def test_game_loop_config() -> None:
    """Test game loop configuration."""
    config = GameLoopConfig(fps=60)
    assert config.fps == 60
    assert config.fixed_time_step == 1.0 / 60.0
    assert config.max_frame_time == 0.25


def test_game_loop_custom_config() -> None:
    """Test game loop with custom configuration."""
    config = GameLoopConfig(fps=30, fixed_time_step=1.0 / 30.0, max_frame_time=0.5)
    assert config.fps == 30
    assert config.fixed_time_step == 1.0 / 30.0
    assert config.max_frame_time == 0.5


def test_game_loop_single_frame() -> None:
    """Test processing a single frame."""
    update_called = False
    render_called = False

    def update(dt: float) -> None:
        nonlocal update_called
        update_called = True
        assert dt > 0

    def render() -> None:
        nonlocal render_called
        render_called = True

    config = GameLoopConfig(fps=60)
    loop = GameLoop(update, render, config)
    loop._process_frame()

    assert update_called
    assert render_called


def test_game_loop_metrics() -> None:
    """Test game loop performance metrics."""
    frame_times: List[float] = []

    def update(dt: float) -> None:
        frame_times.append(dt)

    def render() -> None:
        pass

    config = GameLoopConfig(fps=60)
    loop = GameLoop(update, render, config)

    # Run for a few frames
    for _ in range(10):
        loop._process_frame()
        time.sleep(0.016)  # Simulate 60 FPS

    assert len(frame_times) > 0
    assert all(dt > 0 for dt in frame_times)
    assert loop.average_fps > 0


def test_game_loop_stop() -> None:
    """Test stopping the game loop."""
    update_count = 0

    def update(dt: float) -> None:
        nonlocal update_count
        update_count += 1
        if update_count >= 10:
            loop.stop()

    def render() -> None:
        pass

    config = GameLoopConfig(fps=60)
    loop = GameLoop(update, render, config)
    loop.start()

    # Run updates until stopped
    while loop.running:
        loop.run_one_frame()

    assert update_count >= 10


def test_game_loop_invalid_fps() -> None:
    """Test that invalid FPS values raise ValueError."""
    with pytest.raises(ValueError):
        GameLoopConfig(fps=0)

    with pytest.raises(ValueError):
        GameLoopConfig(fps=-1)
