import customtkinter as ctk
from infrastructure.config import defaults as df


class BaseModalWindow(ctk.CTkToplevel):

    DEFAULT_WIDTH = 500
    DEFAULT_HEIGHT = 400

    def __init__(
        self,
        master,
        styles,
        width=None,
        height=None,
        title=None,
        show_close_button=True
    ):
        super().__init__(master)

        self.WIDTH = width or self.DEFAULT_WIDTH
        self.HEIGHT = height or self.DEFAULT_HEIGHT
        self.colors = styles["colors"]
        # Quitar barra nativa
        self.overrideredirect(True)

        # Modal
        self.grab_set()
        self.focus_force()

        # Configuración base
        self._configure_window()
        self._create_container(show_close_button)

        if title:
            self.set_title(title)

        self._center_window()
        self._bind_escape()



    # =========================================================
    # CONFIGURACIÓN BASE
    # =========================================================

    def _configure_window(self):
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)


    def _create_container(self, show_close_button):
        """
        Frame principal que contendrá todo el contenido
        Las clases hijas deben agregar widgets a self.container
        """

        self.container = ctk.CTkFrame(
            self,
            corner_radius=df.CORNER_RADIUS
        )
        self.container.pack(fill="both", expand=True, padx=2, pady=2)

        # Header opcional
        self.header = ctk.CTkFrame(
            self.container,
            height=df.WINDOW_HEADER_HEIGHT,
            corner_radius=0
        )
        self.header.pack(fill="x")

        self.header.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            self.header,
            text="",
            font=("Arial", 14)
        )
        self.title_label.pack(side="left", padx=15)

        if show_close_button:
            self.close_button = ctk.CTkButton(
                self.header,
                text="✕",
                fg_color=self.colors["top_frame"],
                hover_color="red",
                width=40,
                command=self.destroy,
                corner_radius=0,
            )
            self.close_button.pack(side="right")

        # Área donde van los widgets reales
        self.body = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )
        self.body.pack(fill="both", expand=True, padx=df.PADX, pady=df.PADY)

        self._make_draggable()


    # =========================================================
    # UTILIDADES
    # =========================================================

    def set_title(self, text):
        self.title_label.configure(text=text)


    def _center_window(self):
        self.update_idletasks()

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        x = (screen_w - self.WIDTH) // 2
        y = (screen_h - self.HEIGHT) // 2

        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")


    # =========================================================
    # DRAG WINDOW
    # =========================================================

    def _make_draggable(self):
        self.header.bind("<Button-1>", self._start_move)
        self.header.bind("<B1-Motion>", self._on_move)

    # =========================================================
    # ESC CLOSE
    # =========================================================

    def _bind_escape(self):
        self.bind("<Escape>", lambda event: self.destroy())

    def _start_move(self, event):
        self._x = event.x
        self._y = event.y

    def _on_move(self, event):
        x = self.winfo_pointerx() - self._x
        y = self.winfo_pointery() - self._y
        self.geometry(f"+{x}+{y}")
