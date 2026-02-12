from core.view_manager.views import Views


class ViewManager:
    def __init__(self):
        self._stack = [Views.TODAY]  # vista raíz

    @property
    def current_view(self):
        return self._stack[-1]

    def open_view(self, view: Views):
        # Evita duplicar la misma vista encima
        if self.current_view != view:
            self._stack.append(view)
        return self.current_view

    def go_back(self):
        if len(self._stack) > 1:
            self._stack.pop()
        return self.current_view
