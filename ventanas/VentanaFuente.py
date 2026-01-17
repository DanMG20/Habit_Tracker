import customtkinter as ctk 
from tkinter import font

class VentanaFuente(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Selector de Fuente")
        self.index_actual = 0  # índice sincronizado
        self.crear_frame()

    def crear_frame(self):
        self.grab_set() 
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        ancho, alto = 400, 400
        x = (pantalla_ancho // 2) - (ancho // 2) + 143
        y = (pantalla_alto // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.fuente_seleccionada = "Arial"

        # Label de ejemplo
        self.label = ctk.CTkLabel(self, text="Texto de ejemplo", font=(self.fuente_seleccionada, 20))
        self.label.pack(pady=20)

        # Buscar
        self.buscar_entry = ctk.CTkEntry(self, placeholder_text="Buscar fuente...")
        self.buscar_entry.pack(pady=5, fill="x", padx=10)
        self.buscar_entry.bind("<KeyRelease>", self.filtrar_fuentes)

        # Fuentes
        self.fuentes_disponibles = sorted(list(font.families()))
        self.fuentes_filtradas = self.fuentes_disponibles[:]

        # ComboBox
        self.combo_fuente = ctk.CTkComboBox(
            self,
            values=self.fuentes_filtradas,
            command=self._on_combo_change  # sincroniza índice cuando el usuario selecciona
        )
        # valor inicial + índice sincronizado
        if self.fuente_seleccionada in self.fuentes_filtradas:
            self.index_actual = self.fuentes_filtradas.index(self.fuente_seleccionada)
        else:
            self.index_actual = 0
            self.fuente_seleccionada = self.fuentes_filtradas[0]
        self.combo_fuente.set(self.fuente_seleccionada)
        self.combo_fuente.pack(pady=10, fill="x", padx=10)

        # Enlaces de rueda (Windows/macOS)
        self.combo_fuente.bind("<MouseWheel>", self._on_wheel)     # sobre el combobox
        # Intenta también sobre el entry interno (según versión de customtkinter)
        try:
            self.combo_fuente._entry.bind("<MouseWheel>", self._on_wheel)
        except Exception:
            pass

        # Enlaces para Linux (scroll arriba/abajo)
        self.combo_fuente.bind("<Button-4>", self._on_wheel_up)    # rueda arriba
        self.combo_fuente.bind("<Button-5>", self._on_wheel_down)  # rueda abajo
        try:
            self.combo_fuente._entry.bind("<Button-4>", self._on_wheel_up)
            self.combo_fuente._entry.bind("<Button-5>", self._on_wheel_down)
        except Exception:
            pass

        # Botones
   
        self.btn_aplicar = ctk.CTkButton(self, text="Aplicar cambios", command=self.aplicar_fuente)
        self.btn_aplicar.pack(pady=10)

    # ==== Lógica de filtrado ====
    def filtrar_fuentes(self, event=None):
        texto = self.buscar_entry.get().lower()
        self.fuentes_filtradas = [f for f in self.fuentes_disponibles if texto in f.lower()]
        if not self.fuentes_filtradas:
            self.fuentes_filtradas = self.fuentes_disponibles[:]

        self.combo_fuente.configure(values=self.fuentes_filtradas)

        # reset a la primera coincidencia
        self.index_actual = 0
        self.fuente_seleccionada = self.fuentes_filtradas[0]
        self.combo_fuente.set(self.fuente_seleccionada)
        self._aplicar_preview()  # vista previa inmediata

    # ==== Sincroniza índice cuando el usuario elige en el dropdown ====
    def _on_combo_change(self, valor):
        try:
            self.index_actual = self.fuentes_filtradas.index(valor)
        except ValueError:
            self.index_actual = 0
        self.fuente_seleccionada = valor
        self._aplicar_preview()

    # ==== Manejo de rueda ====
    def _move_index(self, paso):
        if not self.fuentes_filtradas:
            return
        self.index_actual = max(0, min(len(self.fuentes_filtradas) - 1, self.index_actual + paso))
        nueva = self.fuentes_filtradas[self.index_actual]
        self.combo_fuente.set(nueva)
        self.fuente_seleccionada = nueva
        self._aplicar_preview()

    def _on_wheel(self, event):
        # Windows/macOS: event.delta > 0 (arriba), < 0 (abajo)
        paso = -1 if event.delta > 0 else 1
        self._move_index(paso)
        return "break"  # evita comportamiento por defecto

    # Linux: eventos separados para arriba/abajo
    def _on_wheel_up(self, event):
        self._move_index(-1)
        return "break"

    def _on_wheel_down(self, event):
        self._move_index(1)
        return "break"

    # ==== Aplicaciones ====
    def _aplicar_preview(self):
        self.label.configure(font=(self.fuente_seleccionada, 20))

    def aplicar_fuente(self):
        self.fuente_seleccionada = self.combo_fuente.get()
        print(self.fuente_seleccionada)
        # Llama a tus métodos del master:
        self.master.controller.change_font(self.fuente_seleccionada)
        self.master.reiniciar_app()
