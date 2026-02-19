from tkinter import font
from utils.paths import icon_path
from infrastructure.config import defaults as df
import customtkinter as ctk


class FontWindow(ctk.CTkToplevel):

    WIDTH = 400
    HEIGHT = 400
    PREVIEW_SIZE = 20

    def __init__(self, master, styles, update_font):
        super().__init__(master)

        self.after(201, self._set_custom_icon)

        self.title("Selector de Fuente")
        self.resizable(False, False)
        self.grab_set()

        self._current_font = styles["current_font"]
        self.colors = styles["colors"]
        self._update_font_callback = update_font

        self.selected_font = self._current_font
        self.index_actual = 0

        self.fuentes_disponibles = sorted(font.families())
        self.fuentes_filtradas = self.fuentes_disponibles[:]

        self._build()
        self._center_window()

    # =============================
    # UI
    # =============================

    def _build(self):

        self.label_actual = ctk.CTkLabel(
            self,
            text=f"Fuente actual: {self._current_font}",
            fg_color=self.colors["top_frame"],
            font=(self._current_font, self.PREVIEW_SIZE),
            corner_radius= df.CORNER_RADIUS,

        )
        self.label_actual.pack(fill ="both", pady=10 , padx = 10 )

        self.label_preview = ctk.CTkLabel(
            self,
            text="Texto de ejemplo",
            font=(self.selected_font, self.PREVIEW_SIZE)
        )
        self.label_preview.pack(pady=20)

        self.buscar_entry = ctk.CTkEntry(
            self,
            placeholder_text="Buscar fuente..."
        )
        self.buscar_entry.pack(pady=5, fill="x", padx=10)
        self.buscar_entry.bind("<KeyRelease>", self._filtrar_fuentes)

        self.combobox_font = ctk.CTkComboBox(
            self,
            values=self.fuentes_filtradas,
            command=self._on_combo_change
        )
        self.combobox_font.pack(pady=10, fill="x", padx=10)
        self.combobox_font.set(self.selected_font)

        self._bind_mousewheel()

        self.btn_aplicar = ctk.CTkButton(
            self,
            text="Aplicar cambios",
            command=self._apply_font
        )
        self.btn_aplicar.pack(pady=10)

    # =============================
    # Window Helpers
    # =============================

    def _center_window(self):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        x = (screen_w - self.WIDTH) // 2
        y = (screen_h - self.HEIGHT) // 2

        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

    def _set_custom_icon(self):
        self.iconbitmap(icon_path())

    # =============================
    # Font Logic
    # =============================

    def _filtrar_fuentes(self, event=None):
        texto = self.buscar_entry.get().lower()

        self.fuentes_filtradas = [
            f for f in self.fuentes_disponibles
            if texto in f.lower()
        ] or self.fuentes_disponibles[:]

        self.combobox_font.configure(values=self.fuentes_filtradas)

        self.index_actual = 0
        self.selected_font = self.fuentes_filtradas[0]
        self.combobox_font.set(self.selected_font)

        self._apply_preview()

    def _on_combo_change(self, valor):
        if valor in self.fuentes_filtradas:
            self.index_actual = self.fuentes_filtradas.index(valor)

        self.selected_font = valor
        self._apply_preview()

    def _move_index(self, step):
        if not self.fuentes_filtradas:
            return

        self.index_actual = max(
            0,
            min(len(self.fuentes_filtradas) - 1,
                self.index_actual + step)
        )

        nueva = self.fuentes_filtradas[self.index_actual]
        self.selected_font = nueva
        self.combobox_font.set(nueva)

        self._apply_preview()

    def _apply_preview(self):
        self.label_preview.configure(
            font=(self.selected_font, self.PREVIEW_SIZE)
        )

    def _apply_font(self):
        self._update_font_callback(self.selected_font)
        self.destroy()

    # =============================
    # Mousewheel Handling
    # =============================

    def _bind_mousewheel(self):
        widgets = [self.combobox_font]

        try:
            widgets.append(self.combobox_font._entry)
        except Exception:
            pass

        for w in widgets:
            w.bind("<MouseWheel>", self._on_wheel)
            w.bind("<Button-4>", lambda e: self._move_index(-1))
            w.bind("<Button-5>", lambda e: self._move_index(1))

    def _on_wheel(self, event):
        step = -1 if event.delta > 0 else 1
        self._move_index(step)
        return "break"
