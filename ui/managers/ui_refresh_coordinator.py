from infrastructure.logging.logger import get_logger
from core.app_state.app_state import AppMode
from core.view_manager.views import Views
logger = get_logger(__name__)


class UIRefreshCoordinator:

    def __init__(self):
        self._groups = {}

    def register(self, component, group="default"):
        if group not in self._groups:
            self._groups[group] = []
        self._groups[group].append(component)

    def _map_mode(self, app_mode):
        mapping = {
            AppMode.NORMAL: "weekly",
            AppMode.MONTHLY_GRAPH: "monthly",
            AppMode.YEARLY_GRAPH: "yearly",
        }
        return mapping.get(app_mode)

    def refresh_all(self, view_state, app_mode, current_view = None):
        self._prepare_active_state(view_state, app_mode, current_view)

        for group in self._groups.values():
            self._refresh_group_components(group, view_state)

    def refresh_group(self, group_name, view_state, app_mode):
        self._prepare_active_state(view_state, app_mode)

        group = self._groups.get(group_name, [])
        self._refresh_group_components(group, view_state)

    def _prepare_active_state(self, view_state, app_mode, current_view=None):

        key = self._map_mode(app_mode)

        view_state["active_performance"] = (
            view_state["performances"].get(key)
            if key else None
        )

        view_state["headers"]["active"] = (
            view_state["headers"].get(key)
            if key else None
        )
        logger.info(current_view)
        # 🔥 NUEVO: date header depende de internal view
        if current_view == Views.YESTERDAY:
            view_state["date_header"] = view_state["headers"]["yesterday"]
        else:
            view_state["date_header"] = view_state["headers"]["today"]


    def _refresh_group_components(self, components, view_state):
        for component in components:

            if not hasattr(component, "refresh"):
                continue

            state_key = getattr(component, "state_key", None)

            if state_key:
                state_slice = self._resolve_state(view_state, state_key)
                component.refresh(state_slice)
            else:
                component.refresh(view_state)

    def _resolve_state(self, state, key_path):
        keys = key_path.split(".")
        current = state

        for key in keys:
            if not isinstance(current, dict):
                return None
            current = current.get(key)
            if current is None:
                return None

        return current
