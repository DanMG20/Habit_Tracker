"""
Module defining the available left-panel views for the application's user interface.

This enumeration is used by the ViewManager and UI coordinators to track,
identify, and swap the active component inside the screen's left container 
without relying on hardcoded layout structures.
"""

from enum import Enum, auto


class Views(Enum):
    """
    Enumeration of all distinct sub-panels rendered within the left side container.

    Attributes:
        TODAY: The primary panel showing today's habits.
        YESTERDAY: The fallback panel for logging and checking yesterday's habit data.
        DELETE: The control panel dedicated to remove an existing habit.
        GOAL: The management panel shows the goals of the current quarter
        UPDATE: Panel to select an habit to update it. 
    """
    TODAY = auto()
    YESTERDAY = auto()
    DELETE = auto()
    GOAL = auto()
    UPDATE = auto()