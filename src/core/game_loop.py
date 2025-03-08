from dataclasses import dataclass
import time
from typing import Callable, Optional, List, Dict
from collections import deque

@dataclass
class GameLoopConfig:
    """Configuration for the game loop."""
    target_fps: int
    fixed_update_fps: int
    max_frame_time: float = 0.25  # Maximum time between frames to prevent spiral of death
    fps_sample_size: int = 60  # Number of frames to average for FPS calculation

@dataclass
class PerformanceMetrics:
    """Performance metrics for the game loop."""
    fps: float = 0.0
    frame_time: float = 0.0
    min_frame_time: float = float('inf')
    max_frame_time: float = 0.0
    avg_frame_time: float = 0.0
    fixed_update_time: float = 0.0
    update_time: float = 0.0
    render_time: float = 0.0
    idle_time: float = 0.0

class GameLoop:
    """
    Game loop implementation using a fixed timestep for updates and variable timestep for rendering.
    This provides consistent physics/game logic updates while allowing for smooth rendering.
    """

    def __init__(self, config: GameLoopConfig):
        """Initialize the game loop with the given configuration.
        
        Args:
            config: GameLoopConfig object containing loop settings
            
        Raises:
            ValueError: If target_fps or fixed_update_fps are invalid
        """
        if config.target_fps <= 0:
            raise ValueError("Target FPS must be positive")
        if config.fixed_update_fps <= 0:
            raise ValueError("Fixed update FPS must be positive")

        self.target_fps = config.target_fps
        self.fixed_update_fps = config.fixed_update_fps
        self.max_frame_time = config.max_frame_time

        self.is_running = False
        self.delta_time = 0.0  # Time since last frame
        self.fixed_delta_time = 1.0 / self.fixed_update_fps  # Time between fixed updates

        self._last_time = time.perf_counter()
        self._accumulator = 0.0  # Accumulates time for fixed updates

        # Performance monitoring
        self._frame_times: deque = deque(maxlen=config.fps_sample_size)
        self._metrics = PerformanceMetrics()
        self._last_metrics_update = time.perf_counter()
        self._metrics_update_interval = 0.5  # Update metrics every 0.5 seconds

        # Timing breakdowns
        self._frame_start = 0.0
        self._phase_start = 0.0

        # Callbacks
        self._update: Optional[Callable[[], None]] = None
        self._fixed_update: Optional[Callable[[], None]] = None
        self._render: Optional[Callable[[], None]] = None

    @property
    def metrics(self) -> PerformanceMetrics:
        """Get the current performance metrics."""
        return self._metrics

    @property
    def update(self) -> Optional[Callable[[], None]]:
        """Get the update callback."""
        return self._update

    @update.setter
    def update(self, callback: Callable[[], None]) -> None:
        """Set the update callback.
        
        Args:
            callback: Function to call for variable timestep updates
        """
        self._update = callback

    @property
    def fixed_update(self) -> Optional[Callable[[], None]]:
        """Get the fixed update callback."""
        return self._fixed_update

    @fixed_update.setter
    def fixed_update(self, callback: Callable[[], None]) -> None:
        """Set the fixed update callback.
        
        Args:
            callback: Function to call for fixed timestep updates
        """
        self._fixed_update = callback

    @property
    def render(self) -> Optional[Callable[[], None]]:
        """Get the render callback."""
        return self._render

    @render.setter
    def render(self, callback: Callable[[], None]) -> None:
        """Set the render callback.
        
        Args:
            callback: Function to call for rendering
        """
        self._render = callback

    def start(self) -> None:
        """Start the game loop."""
        self.is_running = True
        self._last_time = time.perf_counter()
        self._accumulator = 0.0
        self._frame_times.clear()
        self._metrics = PerformanceMetrics()

    def stop(self) -> None:
        """Stop the game loop."""
        self.is_running = False

    def _update_timing(self) -> None:
        """Update timing variables for this frame."""
        current_time = time.perf_counter()
        frame_time = current_time - self._last_time
        self._last_time = current_time

        # Clamp frame time to prevent spiral of death
        self.delta_time = min(frame_time, self.max_frame_time)
        self._accumulator += self.delta_time

        # Update frame time statistics
        self._frame_times.append(frame_time)

        # Update metrics periodically
        if current_time - self._last_metrics_update >= self._metrics_update_interval:
            self._update_metrics()
            self._last_metrics_update = current_time

    def _update_metrics(self) -> None:
        """Update performance metrics."""
        if not self._frame_times:
            return

        # Calculate FPS and frame times
        avg_frame_time = sum(self._frame_times) / len(self._frame_times)
        self._metrics.fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
        self._metrics.frame_time = self._frame_times[-1]
        self._metrics.min_frame_time = min(self._frame_times)
        self._metrics.max_frame_time = max(self._frame_times)
        self._metrics.avg_frame_time = avg_frame_time

    def _start_timing(self) -> None:
        """Start timing a phase of the game loop."""
        self._phase_start = time.perf_counter()

    def _end_timing(self, metric_name: str) -> None:
        """End timing a phase and update the corresponding metric.
        
        Args:
            metric_name: Name of the metric to update
        """
        phase_time = time.perf_counter() - self._phase_start
        setattr(self._metrics, metric_name, phase_time)

    def _process_fixed_updates(self) -> None:
        """Process all pending fixed updates."""
        self._start_timing()
        while self._accumulator >= self.fixed_delta_time:
            if self._fixed_update:
                self._fixed_update()
            self._accumulator -= self.fixed_delta_time
        self._end_timing('fixed_update_time')

    def run_one_frame(self) -> None:
        """Run a single frame of the game loop."""
        if not self.is_running:
            return

        self._frame_start = time.perf_counter()
        self._update_timing()

        # Process fixed updates
        self._process_fixed_updates()

        # Process variable update
        self._start_timing()
        if self._update:
            self._update()
        self._end_timing('update_time')

        # Render
        self._start_timing()
        if self._render:
            self._render()
        self._end_timing('render_time')

        # Calculate idle time
        frame_end = time.perf_counter()
        total_frame_time = frame_end - self._frame_start
        target_frame_time = 1.0 / self.target_fps
        self._metrics.idle_time = max(0.0, target_frame_time - total_frame_time)

    def run(self) -> None:
        """Run the game loop continuously."""
        self.start()

        try:
            while self.is_running:
                self.run_one_frame()

                # Sleep to maintain target frame rate
                if self._metrics.idle_time > 0:
                    time.sleep(self._metrics.idle_time)
        except KeyboardInterrupt:
            self.stop()
