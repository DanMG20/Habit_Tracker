from infrastructure.config import defaults as df
class LayoutManager: 
        
    def __init__(self):
        self._layouts = {}


    def show(self, layout):

        for widget, config in layout:
            widget.grid(**config)

    def hide(self, layout): 

        for widget, config in layout:
            widget.grid_remove()

    def __init__(self):
        self._layouts = {}

    def register(self, name, layout):
        self._layouts[name] = layout

    def show(self, name):
        for widget, config in self._layouts.get(name, []):
            widget.grid(**config)

    def hide(self, name):
        for widget, _ in self._layouts.get(name, []):
            widget.grid_remove()

    