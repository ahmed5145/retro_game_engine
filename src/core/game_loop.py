"""Game loop implementation for managing game timing and updates."""
import time
from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass
class GameLoopConfig:
    """Configuration for the game loop."""

    target_fps: int
    fixed_update_fps: int
    max_frame_time: float = 0.25  # Maximum time to prevent spiral of death
    fps_sample_size: int = 60  # Number of frames for FPS calculation


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

    def __init__(self, config: GameLoopConfig):
        """Initialize the game loop.

        Args:
            config: Configuration for the game loop
        """
        self._config = config
        self._is_running = False
        self._last_time = 0.0
        self._frame_times: List[float] = []
        self._accumulator = 0.0
        self._last_metrics_update = 0.0
        self._metrics = PerformanceMetrics()

        self.target_fps = config.target_fps
        self.fixed_update_fps = config.fixed_update_fps
        self.fixed_update_time = 1.0 / config.fixed_update_fps

        # Callbacks
        self._update_callback: Optional[Callable[[], None]] = None
        self._fixed_update_callback: Optional[Callable[[], None]] = None
        self._render_callback: Optional[Callable[[], None]] = None

    @property
    def is_running(self) -> bool:
        """Get whether the game loop is currently running.

        Returns:
            bool: True if the game loop is running, False otherwise.
        """
        return self._is_running

    @property
    def max_frame_time(self) -> float:
        """Get the maximum allowed frame time.

        Returns:
            float: The maximum frame time in seconds.
        """
        return self._config.max_frame_time

    @property
    def fixed_delta_time(self) -> float:
        """Get the fixed update time step.

        Returns:
            float: The fixed update time step in seconds.
        """
        return self.fixed_update_time

    @property
    def accumulator(self) -> float:
        """Get the fixed update accumulator.

        Returns:
            float: The current accumulator value in seconds.
        """
        return self._accumulator

    @property
    def last_metrics_update(self) -> float:
        """Get the time of the last metrics update.

        Returns:
            float: The time of the last metrics update in seconds.
        """
        return self._last_metrics_update

    @property
    def last_time(self) -> float:
        """Get the time of the last frame.

        Returns:
            float: The time of the last frame in seconds.
        """
        return self._last_time

    @property
    def metrics(self) -> PerformanceMetrics:
        """Get the current performance metrics.

        Returns:
            Current performance metrics
        """
        return self._metrics

    @property
    def update(self) -> Optional[Callable[[], None]]:
        """Get the update callback.

        Returns:
            Current update callback or None
        """
        return self._update_callback

    @update.setter
    def update(self, callback: Callable[[], None]) -> None:
        """Set the update callback.

        Args:
            callback: Function to call for variable timestep updates
        """
        self._update_callback = callback

    @property
    def fixed_update(self) -> Optional[Callable[[], None]]:
        """Get the fixed update callback.

        Returns:
            Current fixed update callback or None
        """
        return self._fixed_update_callback

    @fixed_update.setter
    def fixed_update(self, callback: Callable[[], None]) -> None:
        """Set the fixed update callback.

        Args:
            callback: Function to call for fixed timestep updates
        """
        self._fixed_update_callback = callback

    @property
    def render(self) -> Optional[Callable[[], None]]:
        """Get the render callback.

        Returns:
            Current render callback or None
        """
        return self._render_callback

    @render.setter
    def render(self, callback: Callable[[], None]) -> None:
        """Set the render callback.

        Args:
            callback: Function to call for rendering
        """
        self._render_callback = callback

    def start(self) -> None:
        """Start the game loop."""
        self._is_running = True
        self._last_time = time.perf_counter()
        self._accumulator = 0.0

    def stop(self) -> None:
        """Stop the game loop."""
        self._is_running = False

    def _update_timing(self) -> None:
        """Update timing calculations for this frame."""
        current_time = time.perf_counter()
        frame_time = current_time - self._last_time
        self._last_time = current_time

        # Clamp frame time to prevent spiral of death
        frame_time = min(frame_time, self.max_frame_time)

        # Update frame time history
        self._frame_times.append(frame_time)
        if len(self._frame_times) > self._config.fps_sample_size:
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

    def _start_timing(self) -> None:
        """Start timing a section of the game loop."""
        self._last_time = time.perf_counter()

    def _end_timing(self, metric_name: str) -> None:
        """End timing a section and update the corresponding metric.

        Args:
            metric_name: Name of the metric to update
        """
        duration = time.perf_counter() - self._last_time
        setattr(self._metrics, metric_name, duration)

    def _process_fixed_updates(self) -> None:
        """Process all pending fixed updates."""
        self._start_timing()
        while self._accumulator >= self.fixed_delta_time:
            if self._fixed_update_callback:
                self._fixed_update_callback()
            self._accumulator -= self.fixed_delta_time
        self._end_timing("fixed_update_time")

    def run_one_frame(self) -> None:
        """Run a single frame of the game loop."""
        self._last_time = time.perf_counter()

        # Update timing
        self._update_timing()
        self._update_metrics()

        # Fixed update
        self._process_fixed_updates()

        # Variable update
        self._start_timing()
        if self._update_callback:
            self._update_callback()
        self._end_timing("update_time")

        # Render
        self._start_timing()
        if self._render_callback:
            self._render_callback()
        self._end_timing("render_time")

        # Calculate idle time
        frame_end = time.perf_counter()
        total_frame_time = frame_end - self._last_time
        target_frame_time = 1.0 / self.target_fps
        self._metrics.idle_time = max(0.0, target_frame_time - total_frame_time)

    def run(self) -> None:
        """Run the game loop continuously."""
        self.start()

        try:
            while self._is_running:
                self.run_one_frame()

                # Sleep to maintain target frame rate
                if self._metrics.idle_time > 0:
                    time.sleep(self._metrics.idle_time)
        except KeyboardInterrupt:
            self.stop()
