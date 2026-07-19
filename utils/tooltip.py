"""Module responsible for rendering context-aware tooltips for UI widgets."""

import tkinter as tk
from typing import Any, Dict, Final, Optional
import customtkinter as ctk
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

DEFAULT_DELAY_MS: Final[int] = 450
OFFSET_X: Final[int] = 10
OFFSET_Y: Final[int] = 10
TOOLTIP_ALPHA: Final[float] = 0.9
CORNER_RADIUS: Final[int] = 8
PADDING_X: Final[int] = 10
PADDING_Y: Final[int] = 5


class Tooltip:
    """Hover-based contextual tooltip component for CustomTkinter widgets."""

    def __init__(
        self,
        widget: ctk.CTkBaseClass,
        text: str,
        styles: Dict[str, Any],
        delay: int = DEFAULT_DELAY_MS,
    ) -> None:
        """Initializes the Tooltip with associated widget and style configurations.

        Args:
            widget: The parent CustomTkinter component to bind.
            text: The message string to display inside the tooltip.
            styles: A dictionary containing aesthetic mappings ('colors' and 'fonts').
            delay: The timing delay in milliseconds before the tooltip appears.
        """
        self._widget: ctk.CTkBaseClass = widget
        self._text: str = text
        self._delay: int = delay


        colors: Dict[str, Any] = styles.get("colors", {})
        fonts: Dict[str, Any] = styles.get("fonts", {})

        self._fg_color: str = colors.get("frame", "#333333")
        self._text_color: str = colors.get("text", "#FFFFFF")
        self._font: tuple = fonts.get("SMALL", ("Arial", 11))

        self._tooltip: Optional[ctk.CTkToplevel] = None
        self._after_id: Optional[str] = None


        self._widget.bind("<Button-1>", self.cancel)
        self._widget.bind("<Enter>", self.schedule)
        self._widget.bind("<Leave>", self.cancel)
        self._widget.bind("<Motion>", self.move)

    def schedule(self, event: Optional[tk.Event] = None) -> None:
        """Schedules the display of the tooltip window after the defined delay.

        Args:
            event: The Tkinter event context triggered by the mouse action.
        """
        self.cancel()
        self._after_id = self._widget.after(
            self._delay, lambda: self.show(event)
        )

    def show(self, event: Optional[tk.Event] = None) -> None:
        """Creates and renders the tooltip top-level window layout.

        Args:
            event: The Tkinter event context containing screen pointer coordinates.
        """
        if self._tooltip:
            self.cancel()

        # Prevent building if the parent widget was destroyed mid-flight
        if not self._widget.winfo_exists():
            return

        self._tooltip = ctk.CTkToplevel(self._widget)
        self._tooltip.overrideredirect(True)
        self._tooltip.attributes("-topmost", True)

        try:
            self._tooltip.attributes("-alpha", TOOLTIP_ALPHA)
        except tk.TclError as tcl_err:
            logger.debug(f"Alpha attribute not supported on this platform: {tcl_err}")

        label = ctk.CTkLabel(
            self._tooltip,
            text=self._text,
            fg_color=self._fg_color,
            text_color=self._text_color,
            font=self._font,
            corner_radius=CORNER_RADIUS,
            padx=PADDING_X,
            pady=PADDING_Y,
        )
        label.pack()
        self.move(event)

    def move(self, event: Optional[tk.Event]) -> None:
        """Dynamically tracks and adjusts the tooltip window position on the screen.

        Args:
            event: The active tracking event containing current cursor coordinates.
        """
        if not event:
            return

        if self._tooltip and self._tooltip.winfo_exists():
            x: int = event.x_root + OFFSET_X
            y: int = event.y_root + OFFSET_Y
            self._tooltip.geometry(f"+{x}+{y}")

    def cancel(self, event: Optional[tk.Event] = None) -> None:
        """Cancels any pending schedule and safely destroys the active tooltip window."""
        if self._after_id:
            self._widget.after_cancel(self._after_id)
            self._after_id = None

        if self._tooltip:
            if self._tooltip.winfo_exists():
                self._tooltip.destroy()
            self._tooltip = None