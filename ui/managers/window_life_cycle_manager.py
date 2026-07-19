import logging
from typing import Any, Callable, Optional

# --- Constants ---
DEBOUNCE_DELAY_MS: int = 300
MOVEMENT_THRESHOLD_PX: int = 5


class WindowLifeCycleManager:
    """Manages OS-level window events and coordinates heavy UI suspension.

    Filters OS noise by applying a coordinate threshold, preventing 
    infinite re-entrancy loops when the UI modifies its own layout.

    Attributes:
        _window (Any): The main Tkinter/CustomTkinter window.
        _on_suspend (Callable[[], None]): Logic to execute to hide heavy widgets.
        _on_resume (Callable[[], None]): Logic to execute to restore widgets.
        _logger (logging.Logger): The logger instance.
        _resize_timer (Optional[str]): Timer ID for the debounce logic.
        _is_suspended (bool): Tracks if the UI is currently in a suspended state.
        _last_x (int): Last recorded X coordinate of the window.
        _last_y (int): Last recorded Y coordinate of the window.
        _last_width (int): Last recorded width of the window.
        _last_height (int): Last recorded height of the window.
    """

    def __init__(
        self,
        main_window: Any,
        on_suspend: Callable[[], None],
        on_resume: Callable[[], None]
    ) -> None:
        """Initializes the manager and captures initial window metrics.

        Args:
            main_window (Any): The root window to monitor.
            on_suspend (Callable[[], None]): Action to hide complex components.
            on_resume (Callable[[], None]): Action to restore complex components.
        """
        self._window: Any = main_window
        self._on_suspend: Callable[[], None] = on_suspend
        self._on_resume: Callable[[], None] = on_resume
        self._logger: logging.Logger = logging.getLogger(__name__)

        self._resize_timer: Optional[str] = None
        self._is_suspended: bool = False

        # State tracking to prevent micro-jitter noise
        self._window.update_idletasks()
        self._last_x: int = self._window.winfo_x()
        self._last_y: int = self._window.winfo_y()
        self._last_width: int = self._window.winfo_width()
        self._last_height: int = self._window.winfo_height()

        self._bind_os_events()

    def _bind_os_events(self) -> None:
        """Binds window configuration events safely."""
        self._window.bind("<Configure>", self._handle_configure, add="+")

    def _handle_configure(self, event: Any) -> None:
        """Intercepts window events, filters noise, and manages suspension.
        
        Args:
            event (Any): The Tkinter event containing OS geometry data.
        """
        if event.widget != self._window:
            return

        current_x: int = self._window.winfo_x()
        current_y: int = self._window.winfo_y()
        current_w: int = self._window.winfo_width()
        current_h: int = self._window.winfo_height()

        delta_x: int = abs(current_x - self._last_x)
        delta_y: int = abs(current_y - self._last_y)
        delta_w: int = abs(current_w - self._last_width)
        delta_h: int = abs(current_h - self._last_height)

        # Early Return: Ignore noise if movement is under the threshold and size didn't change
        if (delta_x < MOVEMENT_THRESHOLD_PX and 
            delta_y < MOVEMENT_THRESHOLD_PX and 
            delta_w == 0 and 
            delta_h == 0):
            return

        # Update last known stable state
        self._last_x = current_x
        self._last_y = current_y
        self._last_width = current_w
        self._last_height = current_h

        # Manage Debounce Timer
        if self._resize_timer is not None:
            self._window.after_cancel(self._resize_timer)

        self._resize_timer = self._window.after(
            DEBOUNCE_DELAY_MS,
            self._on_window_settled
        )

        # Suspend only if not already suspended
        if not self._is_suspended:
            self._logger.debug("System UI: Threshold crossed. Suspending rendering.")
            self._is_suspended = True
            self._on_suspend()

    def _on_window_settled(self) -> None:
        """Resumes heavy UI operations once the window has stopped moving."""
        self._resize_timer = None
        self._is_suspended = False
        self._logger.debug("System UI: Transition settled. Resuming rendering.")
        self._on_resume()