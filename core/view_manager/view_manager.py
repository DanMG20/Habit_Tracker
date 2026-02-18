from core.view_manager.views import Views


class ViewManager:
    def __init__(self):
        self._stack = [Views.TODAY]

    @property
    def current_view(self):
        return self._stack[-1]

    def open_view(self, view: Views):

        if self.current_view == view:
            return self.current_view

        if view in self._stack:
            self._stack.remove(view)

        self._stack.append(view)
        return self.current_view

    def go_back(self):
        if len(self._stack) > 1:
            self._stack.pop()
        return self.current_view
