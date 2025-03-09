"""Tests for the game loop system."""
import time

import pytest

from src.core.game_loop import GameLoop, GameLoopConfig, PerformanceMetrics


class MockGame:
    """Mock game class for testing."""

    def __init__(self) -> None:
        self.update_called = 0
        self.fixed_update_called = 0
        self.render_called = 0
        self.last_dt = 0.0
        self.should_stop = False

    def update(self) -> None:
        """Track update calls."""
        self.update_called += 1

    def fixed_update(self) -> None:
        """Track fixed update calls."""
        self.fixed_update_called += 1

    def render(self) -> None:
        """Track render calls."""
        self.render_called += 1


def test_game_loop_config() -> None:
    """Test game loop configuration."""
    config = GameLoopConfig(target_fps=60, fixed_update_fps=50, max_frame_time=0.25)
    assert config.target_fps == 60
    assert config.fixed_update_fps == 50
    assert config.max_frame_time == 0.25


def test_game_loop_custom_config() -> None:
    """Test game loop with custom configuration."""
    config = GameLoopConfig(
        target_fps=30, fixed_update_fps=30, max_frame_time=0.5, fps_sample_size=30
    )
    loop = GameLoop(config)

    assert loop.target_fps == 30
    assert loop.fixed_update_fps == 30
    assert loop.max_frame_time == 0.5


def test_game_loop_single_frame() -> None:
    """Test running a single frame of the game loop."""
    config = GameLoopConfig(target_fps=60, fixed_update_fps=50)
    loop = GameLoop(config)
    game = MockGame()

    # Set up callbacks
    loop.update = game.update
    loop.fixed_update = game.fixed_update
    loop.render = game.render

    # Start the loop and run one frame
    loop.start()

    # Force accumulator to have enough time for a fixed update
    loop._accumulator = loop.fixed_delta_time
    loop.run_one_frame()

    assert game.update_called == 1
    assert game.fixed_update_called == 1
    assert game.render_called == 1


def test_game_loop_metrics() -> None:
    """Test game loop metrics tracking."""
    config = GameLoopConfig(
        target_fps=60,
        fixed_update_fps=50,
        fps_sample_size=3,  # Small sample size for testing
    )
    loop = GameLoop(config)
    game = MockGame()

    # Set up callbacks
    loop.update = game.update
    loop.fixed_update = game.fixed_update
    loop.render = game.render

    # Start the loop and process frames
    loop.start()

    # Force metrics update by setting last update time back
    loop._last_metrics_update = time.perf_counter() - 1.0

    # Run frames with consistent timing
    frame_time = 1.0 / 60.0
    for _ in range(3):
        loop._last_time = time.perf_counter() - frame_time
        loop.run_one_frame()

    # Metrics should be updated
    assert loop.metrics.frame_time > 0
    assert loop.metrics.update_time >= 0
    assert loop.metrics.render_time >= 0
    assert loop.metrics.idle_time >= 0


def test_game_loop_stop() -> None:
    """Test stopping the game loop."""
    config = GameLoopConfig(target_fps=60, fixed_update_fps=50)
    loop = GameLoop(config)
    game = MockGame()

    # Set up callbacks
    loop.update = game.update
    loop.fixed_update = game.fixed_update
    loop.render = game.render

    # Start the loop but immediately stop it
    def stop_after_frame() -> None:
        loop.stop()

    # Override update to stop after first frame
    loop.update = stop_after_frame

    loop.run()
    assert not loop.is_running


def test_game_loop_invalid_fps() -> None:
    """Test that invalid FPS values raise ValueError."""
    with pytest.raises(ValueError):
        config = GameLoopConfig(target_fps=0, fixed_update_fps=50)  # Invalid
        GameLoop(config)

    with pytest.raises(ValueError):
        config = GameLoopConfig(target_fps=60, fixed_update_fps=-1)  # Invalid
        GameLoop(config)
