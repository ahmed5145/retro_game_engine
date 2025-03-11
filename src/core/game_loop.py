"""Game loop implementation for managing game timing and updates."""
import time
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple

import pygame


@dataclass
class GameLoopConfig:
    """Configuration for the game loop."""

    fps: int = 60
    """Target frames per second."""

    fixed_time_step: float = 1.0 / 60.0
    """Fixed time step for physics updates."""

    max_frame_time: float = 0.25
    """Maximum time to process in a single frame."""

    fps_sample_size: int = 60
    """Number of frames to sample for FPS calculation."""

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if self.fps <= 0:
            raise ValueError("FPS must be greater than 0")
        if self.fixed_time_step <= 0:
            raise ValueError("Fixed time step must be greater than 0")
        if self.max_frame_time <= 0:
            raise ValueError("Maximum frame time must be greater than 0")
        if self.fps_sample_size <= 0:
            raise ValueError("FPS sample size must be greater than 0")


@dataclass
class PerformanceMetrics:
    """Performance metrics for the game loop."""

    fps: float = 0.0
    frame_time: float = 0.0
    min_frame_time: float = float("inf")
    max_frame_time: float = 0.0
    avg_frame_time: float = 0.0
    fixed_update_time: float = 0.0
    update_time: float = 0.0
    render_time: float = 0.0
    idle_time: float = 0.0


class GameLoop:
    """Manages the game loop with fixed and variable timestep updates."""

    def __init__(
        self,
        update_func: Callable[[float], None],
        render_func: Callable[[], None],
        config: Optional[GameLoopConfig] = None,
    ) -> None:
        """Initialize the game loop."""
        self.update_func = update_func
        self.render_func = render_func
        self.config = config or GameLoopConfig()
        self.running = False
        self.frame_count = 0
        self.total_time = 0.0
        self.delta_time = 0.0
        self.physics_accumulator = 0.0
        self._frame_times: List[float] = []
        self._last_time: float = time.perf_counter()
        self._metrics = PerformanceMetrics()
        self._timing_stack: List[Tuple[str, float]] = []

    def start(self) -> None:
        """Start the game loop."""
        self.running = True
        self.frame_count = 0
        self.total_time = 0.0
        self.delta_time = 0.0
        self.physics_accumulator = 0.0
        self._frame_times = []
        self._last_time = time.perf_counter()
        self._metrics = PerformanceMetrics()

    def stop(self) -> None:
        """Stop the game loop."""
        self.running = False

    def run(self) -> None:
        """Run the game loop continuously."""
        self.start()
        try:
            while self.running:
                self.run_one_frame()
        except KeyboardInterrupt:
            self.stop()

    def run_one_frame(self) -> None:
        """Process a single frame."""
        frame_start = time.perf_counter()
        self._process_frame()

        # Calculate sleep time to maintain target FPS
        frame_time = time.perf_counter() - frame_start
        target_frame_time = 1.0 / self.config.fps
        sleep_time = max(0.0, target_frame_time - frame_time)

        if sleep_time > 0:
            time.sleep(sleep_time)
            self._metrics.idle_time = sleep_time

    def _process_frame(self) -> None:
        """Process a single frame of the game loop."""
        current_time = time.perf_counter()
        frame_time = current_time - self._last_time
        self._last_time = current_time

        # Clamp frame time
        frame_time = min(frame_time, self.config.max_frame_time)
        self.delta_time = frame_time
        self.total_time += frame_time
        self.frame_count += 1

        # Fixed timestep updates
        self._start_timing("fixed_update_time")
        self.physics_accumulator += frame_time
        fixed_updates = 0
        while self.physics_accumulator >= self.config.fixed_time_step:
            self.update_func(self.config.fixed_time_step)
            self.physics_accumulator -= self.config.fixed_time_step
            fixed_updates += 1
        self._end_timing("fixed_update_time")

        # Always do variable timestep update
        self._start_timing("update_time")
        self.update_func(frame_time)
        self._end_timing("update_time")

        # Render
        self._start_timing("render_time")
        self.render_func()
        self._end_timing("render_time")

        # Update metrics
        self._frame_times.append(frame_time)
        if len(self._frame_times) > self.config.fps_sample_size:
            self._frame_times.pop(0)
        self._update_metrics()

    def _start_timing(self, metric_name: str) -> None:
        """Start timing a section of the game loop."""
        start_time = time.perf_counter()
        self._timing_stack.append((metric_name, start_time))

    def _end_timing(self, metric_name: str) -> None:
        """End timing a section and update the corresponding metric."""
        if not self._timing_stack:
            return

        name, start_time = self._timing_stack.pop()
        if name != metric_name:
            return

        duration = time.perf_counter() - start_time
        # Use exponential moving average for smoother metrics
        alpha = 0.2  # Smoothing factor
        current_value = getattr(self._metrics, metric_name)
        new_value = (alpha * duration) + ((1 - alpha) * current_value)
        setattr(self._metrics, metric_name, new_value)

    def _update_metrics(self) -> None:
        """Update performance metrics."""
        if not self._frame_times:
            return

        current_frame_time = self._frame_times[-1]
        self._metrics.frame_time = current_frame_time
        self._metrics.min_frame_time = min(self._frame_times)
        self._metrics.max_frame_time = max(self._frame_times)
        self._metrics.avg_frame_time = sum(self._frame_times) / len(self._frame_times)
        self._metrics.fps = (
            1.0 / self._metrics.avg_frame_time
            if self._metrics.avg_frame_time > 0
            else 0.0
        )

    @property
    def average_fps(self) -> float:
        """Get the average FPS."""
        if self.total_time > 0:
            return self.frame_count / self.total_time
        return 0.0
