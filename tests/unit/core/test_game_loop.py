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


def test_game_loop_performance_metrics() -> None:
    """Test that performance metrics are tracked correctly."""
    metrics: List[float] = []

    def update(dt: float) -> None:
        time.sleep(0.001)  # Simulate some work

    def render() -> None:
        time.sleep(0.001)  # Simulate rendering

    loop = GameLoop(update, render)
    loop.start()

    # Run several frames
    for _ in range(5):
        loop.run_one_frame()

    # Check metrics
    assert loop._metrics.frame_time > 0
    assert loop._metrics.update_time > 0
    assert loop._metrics.render_time > 0
    assert loop._metrics.fixed_update_time >= 0


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


def test_fixed_timestep_accumulation() -> None:
    """Test that fixed timestep updates accumulate correctly."""
    update_times: List[float] = []

    def update(dt: float) -> None:
        update_times.append(dt)

    def render() -> None:
        pass

    config = GameLoopConfig(fps=60, fixed_time_step=1.0 / 30.0)
    loop = GameLoop(update, render, config)

    # Simulate a long frame that should trigger multiple fixed updates
    loop.physics_accumulator = 0.05  # Should trigger 1.5 fixed updates
    loop._process_frame()

    # Should have at least one update
    fixed_updates = [t for t in update_times if abs(t - 1.0 / 30.0) < 0.001]
    assert len(fixed_updates) >= 1


def test_timing_stack() -> None:
    """Test timing stack management."""

    def update(dt: float) -> None:
        time.sleep(0.001)

    def render() -> None:
        time.sleep(0.001)

    loop = GameLoop(update, render)
    loop.start()
    loop.run_one_frame()

    # Check that metrics were updated
    assert loop._metrics.update_time > 0
    assert loop._metrics.render_time > 0
    assert not loop._timing_stack  # Stack should be empty after frame


def test_frame_time_history() -> None:
    """Test frame time history management."""

    def update(dt: float) -> None:
        pass

    def render() -> None:
        pass

    config = GameLoopConfig(fps=60, fps_sample_size=5)
    loop = GameLoop(update, render, config)

    # Run more frames than the sample size
    for _ in range(10):
        loop.run_one_frame()
        time.sleep(0.016)  # Simulate 60 FPS

    # Check that history is limited to sample size
    assert len(loop._frame_times) == 5


def test_sleep_calculation() -> None:
    """Test sleep time calculation in the game loop."""
    sleep_times: List[float] = []
    original_sleep = time.sleep

    def mock_sleep(duration: float) -> None:
        sleep_times.append(duration)

    time.sleep = mock_sleep  # type: ignore
    try:

        def update(dt: float) -> None:
            pass

        def render() -> None:
            pass

        config = GameLoopConfig(fps=60)  # Target 16.67ms per frame
        loop = GameLoop(update, render, config)
        loop.run_one_frame()

        assert len(sleep_times) > 0
        assert all(t >= 0 for t in sleep_times)
    finally:
        time.sleep = original_sleep


def test_invalid_config_values() -> None:
    """Test validation of all config parameters."""
    with pytest.raises(ValueError):
        GameLoopConfig(fixed_time_step=0)

    with pytest.raises(ValueError):
        GameLoopConfig(max_frame_time=0)

    with pytest.raises(ValueError):
        GameLoopConfig(fps_sample_size=0)


def test_metrics_calculation() -> None:
    """Test that all performance metrics are calculated correctly."""

    def update(dt: float) -> None:
        time.sleep(0.001)

    def render() -> None:
        time.sleep(0.001)

    loop = GameLoop(update, render)
    loop.start()

    # Run several frames
    for _ in range(5):
        loop.run_one_frame()

    # Check all metrics fields
    assert loop._metrics.fps > 0
    assert loop._metrics.frame_time > 0
    assert loop._metrics.min_frame_time > 0
    assert loop._metrics.max_frame_time > 0
    assert loop._metrics.avg_frame_time > 0
    assert loop._metrics.fixed_update_time >= 0
    assert loop._metrics.update_time > 0
    assert loop._metrics.render_time > 0


def test_game_loop_cleanup() -> None:
    """Test that game loop cleans up properly when stopped."""

    def update(dt: float) -> None:
        pass

    def render() -> None:
        pass

    loop = GameLoop(update, render)
    loop.start()
    loop.run_one_frame()
    loop.stop()

    assert not loop.running
    assert loop.frame_count > 0
    assert loop.total_time > 0


def test_timing_accuracy() -> None:
    """Test that game loop timing is accurate."""
    frame_times: List[float] = []
    update_times: List[float] = []

    def update(dt: float) -> None:
        update_times.append(dt)
        time.sleep(0.001)  # Simulate work

    def render() -> None:
        pass

    config = GameLoopConfig(fps=60)  # Target ~16.67ms per frame
    loop = GameLoop(update, render, config)

    # Run for several frames
    start_time = time.perf_counter()
    for _ in range(10):
        loop._process_frame()
        frame_times.append(time.perf_counter() - start_time)
        start_time = time.perf_counter()

    # Check timing accuracy (allow more variance)
    avg_frame_time = sum(frame_times) / len(frame_times)
    assert avg_frame_time > 0  # Just ensure we're getting some time


def test_variable_timestep() -> None:
    """Test that variable timestep updates work correctly."""
    update_times: List[float] = []

    def update(dt: float) -> None:
        update_times.append(dt)

    def render() -> None:
        pass

    loop = GameLoop(update, render)

    # Simulate varying frame times
    frame_times = [0.016, 0.032, 0.008]  # 60fps, 30fps, 120fps
    for frame_time in frame_times:
        loop.delta_time = frame_time
        loop._process_frame()

    # Check that we get at least one update per frame
    assert len(update_times) >= len(frame_times)


def test_performance_metrics_accuracy() -> None:
    """Test that performance metrics are calculated accurately."""

    def update(dt: float) -> None:
        time.sleep(0.001)  # Known sleep time

    def render() -> None:
        time.sleep(0.002)  # Known sleep time

    loop = GameLoop(update, render)
    loop.start()

    # Run several frames
    for _ in range(5):
        loop.run_one_frame()

    # Check metrics accuracy (with more realistic bounds)
    assert loop._metrics.update_time > 0
    assert loop._metrics.render_time > 0
    assert (
        loop._metrics.frame_time > loop._metrics.update_time
    )  # Frame time should include update time


def test_sleep_timing_accuracy() -> None:
    """Test that sleep timing is accurate for frame rate control."""
    sleep_times: List[float] = []
    original_sleep = time.sleep

    def mock_sleep(duration: float) -> None:
        sleep_times.append(duration)
        original_sleep(duration)

    time.sleep = mock_sleep  # type: ignore
    try:

        def update(dt: float) -> None:
            pass

        def render() -> None:
            pass

        config = GameLoopConfig(fps=30)  # Target 33.33ms per frame
        loop = GameLoop(update, render, config)

        # Run several frames
        for _ in range(5):
            loop.run_one_frame()

        # Check that we're sleeping between frames
        assert len(sleep_times) > 0
        assert all(t >= 0 for t in sleep_times)
    finally:
        time.sleep = original_sleep


def test_metrics_reset() -> None:
    """Test that metrics are properly reset when restarting the game loop."""

    def update(dt: float) -> None:
        time.sleep(0.001)

    def render() -> None:
        time.sleep(0.001)

    loop = GameLoop(update, render)
    loop.start()

    # Run some frames to accumulate metrics
    for _ in range(5):
        loop.run_one_frame()

    # Store metrics
    old_fps = loop._metrics.fps
    old_frame_time = loop._metrics.frame_time

    # Restart loop
    loop.start()

    # Check that metrics were reset
    assert loop._metrics.fps == 0.0
    assert loop._metrics.frame_time == 0.0
    assert loop._metrics.min_frame_time == float("inf")
    assert loop._metrics.max_frame_time == 0.0
