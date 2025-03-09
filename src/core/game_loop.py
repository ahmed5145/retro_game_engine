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
    """Manages the game loop with fixed and variable timestep updates.

    The game loop handles timing, updates, and rendering with support for both
    fixed timestep physics/logic updates and variable timestep rendering.
    """

    def __init__(
        self,
        update_func: Callable[[float], None],
        render_func: Callable[[], None],
        config: Optional[GameLoopConfig] = None,
    ) -> None:
        """Initialize the game loop.

        Args:
            update_func: Function to call for game updates
            render_func: Function to call for rendering
            config: Optional configuration (default: None)
        """
        self.update_func = update_func
        self.render_func = render_func
        self.config = config or GameLoopConfig()
        self.running = False
        self.frame_count = 0
        self.total_time = 0.0
        self.delta_time = 0.0
        self.physics_accumulator = 0.0
        self._frame_times: List[float] = []
        self._accumulator: float = 0.0
        self._last_time: float = time.perf_counter()
        self._metrics = PerformanceMetrics()
        self._timing_stack: List[Tuple[str, float]] = []
        self._clock = pygame.time.Clock()

    def run(self) -> None:
        """Run the game loop continuously."""
        self.start()
        try:
            while self.running:
                self._process_frame()
                # Sleep to maintain target frame rate
                target_frame_time = 1.0 / self.config.fps
                current_time = time.perf_counter()
                frame_time = current_time - self._last_time
                sleep_time = max(0.0, target_frame_time - frame_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
        except KeyboardInterrupt:
            self.stop()

    def start(self) -> None:
        """Start the game loop."""
        self.running = True
        self.frame_count = 0
        self.total_time = 0.0
        self.delta_time = 0.0
        self.physics_accumulator = 0.0
        self._frame_times = []
        self._accumulator = 0.0
        self._last_time = time.perf_counter()
        self._metrics = PerformanceMetrics()

    def stop(self) -> None:
        """Stop the game loop."""
        self.running = False

    def _process_frame(self) -> None:
        """Process a single frame."""
        # Get frame time
        current_time = time.perf_counter()
        frame_time = current_time - self._last_time
        self._last_time = current_time

        # Clamp frame time to prevent spiral of death
        frame_time = min(frame_time, self.config.max_frame_time)
        self.delta_time = frame_time
        self.total_time += frame_time
        self.frame_count += 1

        # Update physics with fixed time step
        self.physics_accumulator += frame_time
        while self.physics_accumulator >= self.config.fixed_time_step:
            self._start_timing("fixed_update_time")
            self.update_func(self.config.fixed_time_step)
            self._end_timing("fixed_update_time")
            self.physics_accumulator -= self.config.fixed_time_step

        # Variable update
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

    @property
    def average_fps(self) -> float:
        """Get the average FPS.

        Returns:
            Average frames per second
        """
        if self.total_time > 0:
            return self.frame_count / self.total_time
        return 0.0

    def _update_timing(self) -> None:
        """Update timing calculations for this frame."""
        current_time = time.perf_counter()
        frame_time = current_time - self._last_time
        self._last_time = current_time

        # Clamp frame time to prevent spiral of death
        frame_time = min(frame_time, self.config.max_frame_time)

        # Update frame time history
        self._frame_times.append(frame_time)
        if len(self._frame_times) > self.config.fps_sample_size:
            self._frame_times.pop(0)

        # Update fixed update accumulator
        self._accumulator += frame_time

    def _update_metrics(self) -> None:
        """Update performance metrics."""
        if self._frame_times:
            self._metrics.frame_time = self._frame_times[-1]
            self._metrics.min_frame_time = min(self._frame_times)
            self._metrics.max_frame_time = max(self._frame_times)
            self._metrics.avg_frame_time = sum(self._frame_times) / len(
                self._frame_times
            )
            self._metrics.fps = 1.0 / self._metrics.avg_frame_time

    def _start_timing(self, metric_name: str) -> None:
        """Start timing a section of the game loop."""
        self._last_time = time.perf_counter()
        self._timing_stack.append((metric_name, self._last_time))

    def _end_timing(self, metric_name: str) -> None:
        """End timing a section and update the corresponding metric.

        Args:
            metric_name: Name of the metric to update
        """
        duration = time.perf_counter() - self._last_time
        setattr(self._metrics, metric_name, duration)
        self._timing_stack.pop()

    def _process_fixed_updates(self) -> None:
        """Process fixed timestep updates."""
        self._start_timing("fixed_update_time")
        while self._accumulator >= self.config.fixed_time_step:
            self.update_func(self.config.fixed_time_step)
            self._accumulator -= self.config.fixed_time_step
        self._end_timing("fixed_update_time")

    def run_one_frame(self) -> None:
        """Run a single frame of the game loop."""
        if not self.running:
            self.start()
        self._process_frame()
