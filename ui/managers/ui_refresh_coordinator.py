from infrastructure.logging.logger import get_logger
from core.app_state.app_state import AppMode
logger = get_logger(__name__)


class UIRefreshCoordinator:

    def __init__(self):
        self._components = []
        self._groups = {}
        self._panel_keys = {}

    def register(self, component, group="default", panel_key=None):
        """
        panel_key: str | None -> la clave en view_state['panels'] que este panel maneja.
        """
        if group not in self._groups:
            self._groups[group] = []
        self._groups[group].append(component)
        if panel_key:
            self._panel_keys[component] = panel_key

    def _map_mode(self, app_mode):

        mapping = {
            AppMode.NORMAL: "weekly",
            AppMode.MONTHLY_GRAPH: "monthly",
            AppMode.YEARLY_GRAPH: "yearly",
        }

        return mapping.get(app_mode)

    def refresh_all(self, view_state, app_mode):
        performance_key = self._map_mode(app_mode)
        view_state["active_performance"] = (
            view_state["performances"].get(performance_key)
            if performance_key else None
        )

        header_key = self._map_mode(app_mode)
        view_state["headers"]["active"] = (
            view_state["headers"].get(header_key)
            if header_key else None
        )

        for group in self._groups.values():
            for component in group:

                if not hasattr(component, "refresh"):
                    continue

                panel_key = self._panel_keys.get(component)
                if panel_key:
                    panel_state = view_state["panels"].get(panel_key)
                    component.refresh(panel_state)
                else:
                    component.refresh(view_state)