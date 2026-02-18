from infrastructure.logging.logger import get_logger
from core.app_state.app_state import AppMode
from core.view_manager.views import Views

logger = get_logger(__name__)


class UIRefreshCoordinator:

    def __init__(self):
        self._components = []

    # =========================================================
    # REGISTRO SIMPLE (sin grupos)
    # =========================================================
    def register(self, component):
        if component not in self._components:
            self._components.append(component)

    # =========================================================
    # REFRESH PRINCIPAL BASADO EN EVENTOS
    # =========================================================
    def refresh(
        self,
        view_state,
        app_mode,
        current_view=None,
        event=None
    ):
        """
        event puede ser:
            - "habit_changed"
            - "view_changed"
            - "day_changed"
            - "goal_changed"
            - etc.
        """

        self._prepare_active_state(view_state, app_mode, current_view)

        for component in self._components:

            if not hasattr(component, "refresh"):
                continue

            # 🔥 Si el componente declara eventos, filtramos
            component_events = getattr(component, "events", None)

            if component_events is not None:
                if event not in component_events:
                    continue

            state_key = getattr(component, "state_key", None)

            if state_key:
                state_slice = self._resolve_state(view_state, state_key)
                component.refresh(state_slice)
            else:
                component.refresh(view_state)

    # =========================================================
    # PREPARACIÓN DE ESTADO ACTIVO
    # =========================================================
    def _map_mode(self, app_mode):
        mapping = {
            AppMode.NORMAL: "weekly",
            AppMode.MONTHLY_GRAPH: "monthly",
            AppMode.YEARLY_GRAPH: "yearly",
        }
        return mapping.get(app_mode)

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

        if current_view == Views.YESTERDAY:
            view_state["date_header"] = view_state["headers"]["yesterday"]
        else:
            view_state["date_header"] = view_state["headers"]["today"]

    # =========================================================
    # RESOLUCIÓN DE STATE_KEY
    # =========================================================
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
