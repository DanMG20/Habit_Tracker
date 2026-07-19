"""
Module defining the application state and operational modes.

This module provides the enumerations and state management classes 
necessary to control the current view or interaction mode of the application.
"""

from enum import Enum, auto


class AppMode(Enum):
    """
    Enumeration representing the different modes of the application.

    Attributes:
        NORMAL: The standard operational mode (e.g., viewing the main habit board).
        ADD_HABIT: Mode active when the user is creating a new habit.
        UPDATE_HABIT: Mode active when the user is editing an existing habit.
        MONTHLY_GRAPH: Mode active when viewing the monthly statistics graph.
        YEARLY_GRAPH: Mode active when viewing the yearly statistics graph.
    """
    NORMAL = auto()
    ADD_HABIT = auto()
    UPDATE_HABIT = auto()
    MONTHLY_GRAPH = auto()
    YEARLY_GRAPH = auto()


class AppState:
    """
    Represents the current state of the application.

    This class acts as a centralized state container, ensuring that 
    controllers and views can reliably query or update the current application mode.
    """

    def __init__(self) -> None:
        """
        Initializes the AppState with the default NORMAL mode.
        """
        self.mode: AppMode = AppMode.NORMAL