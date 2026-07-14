"""
Module responsible for managing the navigation state and active views.
"""

from typing import List
from core.view_manager.panel_views import PanelViews


class ViewManager:
    """
    Manages the navigation stack of the application views.
    
    Ensures that the application knows which view is currently active 
    and maintains a unique history stack to allow structured navigation 
    without duplicate entries.
    """

    def __init__(self) -> None:
        """
        Initializes the ViewManager with a default starting view.
        """
        self._stack: List[PanelViews] = [PanelViews.TODAY]

    @property
    def current_view(self) -> PanelViews:
        """
        Retrieves the currently active view.

        Returns:
            Views: The view enum at the top of the navigation stack.
        """
        return self._stack[-1]

    def open_view(self, view: PanelViews) -> PanelViews:
        """
        Opens a new view, bringing it to the top of the navigation stack.

        If the view is already the current view, no action is taken.
        If the view exists lower in the stack, it is removed and placed 
        at the top to prevent duplicate history entries (MRU behavior).

        Args:
            view (Views): The target view to be opened.

        Returns:
            Views: The newly set current view.
        """
        if self.current_view == view:
            return self.current_view

        if view in self._stack:
            self._stack.remove(view)

        self._stack.append(view)
        return self.current_view