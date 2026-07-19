"""
Package initialization for the view manager components.

Exposes the primary ViewManager and the PanelViews enum to provide a clean,
unified public API for external modules, decoupling them from the internal
file structure.
"""

from .view_manager import ViewManager
from .panel_views import PanelViews

# __all__ explicitly defines the public interface of this package layer
__all__ = [
    "ViewManager",
    "PanelViews",
]