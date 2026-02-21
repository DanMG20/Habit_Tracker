from tkinter import font
from infrastructure.config import defaults as df
import customtkinter as ctk
from .base_window import BaseModalWindow

class FontWindow(BaseModalWindow):

    WIDTH = 400
    HEIGHT = 400
    PREVIEW_SIZE = 20

    def __init__(self, master, styles, update_font):
        super().__init__(master,
                         styles = styles, 
                         width=self.WIDTH,
                         height=self.HEIGHT,
                         title= "Selector de fuente"
                         )

  
        self._current_font = styles["current_font"]
        self.colors = styles["colors"]
        self._update_font_callback = update_font

        self.selected_font = self._current_font
        self.index_actual = 0

        self.fuentes_disponibles = sorted(font.families())
        self.filtered_fonts = self.fuentes_disponibles[:]

        self._build()

    # =============================
    # UI
    # =============================

    def _build(self):

        self.label_actual = ctk.CTkLabel(
            self.body,
            text=f"Fuente actual: {self._current_font}",
            fg_color=self.colors["top_frame"],
            font=(self._current_font, self.PREVIEW_SIZE),
            corner_radius= df.CORNER_RADIUS,

        )
        self.label_actual.pack(fill ="both", pady=10 , padx = df.PADX )

        self.label_preview = ctk.CTkLabel(
            self.body,
            text="Texto de ejemplo",
            font=(self.selected_font, self.PREVIEW_SIZE)
        )
        self.label_preview.pack(pady=20)
        self.draw_apply_button()
        self.draw_entry()
        self.draw_combobox()
        

    def draw_entry(self):
        self.buscar_entry = ctk.CTkEntry(
            self.body,
            placeholder_text="Buscar fuente..."
        )
        self.buscar_entry.pack(side ="bottom", pady=5, fill="x", padx=10)
        self.buscar_entry.bind("<KeyRelease>", self._filter_fonts)

    def draw_combobox(self): 
        self.combobox_font = ctk.CTkComboBox(
            self.body,
            values=self.filtered_fonts,
            command=self._on_combo_change
        )
        self.combobox_font.pack(side ="bottom", pady=10, fill="x", padx=10)
        self.combobox_font.set(self.selected_font)
        self._bind_mousewheel()

    def draw_apply_button(self):
  
        self.btn_aplicar = ctk.CTkButton(
            self.body,
            text="Aplicar cambios",
            command=self._apply_font
        )
        self.btn_aplicar.pack(side ="bottom", pady=25)

    # =============================
    # Font Logic
    # =============================

    def _filter_fonts(self, event=None):
        texto = self.buscar_entry.get().lower()

        self.filtered_fonts = [
            f for f in self.fuentes_disponibles
            if texto in f.lower()
        ] or self.fuentes_disponibles[:]

        self.combobox_font.configure(values=self.filtered_fonts)

        self.index_actual = 0
        self.selected_font = self.filtered_fonts[0]
        self.combobox_font.set(self.selected_font)

        self._apply_preview()

    def _on_combo_change(self, valor):
        if valor in self.filtered_fonts:
            self.index_actual = self.filtered_fonts.index(valor)

        self.selected_font = valor
        self._apply_preview()

    def _move_index(self, step):
        if not self.filtered_fonts:
            return

        self.index_actual = max(
            0,
            min(len(self.filtered_fonts) - 1,
                self.index_actual + step)
        )

        nueva = self.filtered_fonts[self.index_actual]
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
