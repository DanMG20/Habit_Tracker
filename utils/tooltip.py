
import customtkinter as ctk
import styles as styles

class Tooltip:
    def __init__(self, widget, texto, fg_color="#333", text_color="#fff", delay=500):
        self.widget = widget
        self.texto = texto
        self.fg_color = fg_color
        self.font = styles.FUENTE_PEQUEÑA
        self.text_color = text_color
        self.delay = delay
        self.tooltip = None
        self.after_id = None

        widget.bind("<Enter>", self.schedule)
        widget.bind("<Leave>", self.cancel)
        widget.bind("<Motion>", self.mover)

    def schedule(self, event=None):
        self.cancel()  # cancelar cualquier plan previo
        self.after_id = self.widget.after(self.delay, lambda e=event: self.mostrar(e))

    def mostrar(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
        self.tooltip = ctk.CTkToplevel(self.widget)
        self.tooltip.overrideredirect(True)
        self.tooltip.attributes('-topmost', True)
        try:
            self.tooltip.attributes('-alpha', 0.9)  # Transparencia
        except:
            pass  # Algunos sistemas no soportan alpha

        label = ctk.CTkLabel(
            self.tooltip,
            text=self.texto,
            fg_color=self.fg_color,
            text_color=self.text_color,
            font=self.font,
            corner_radius=8,
            padx=10,
            pady=5
        )
        label.pack()
        self.mover(event)

    def mover(self, event):
        if self.tooltip and self.tooltip.winfo_exists():
            x = event.x_root + 10
            y = event.y_root + 10
            self.tooltip.geometry(f"+{x}+{y}")

    def cancel(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        if self.tooltip and self.tooltip.winfo_exists():
            self.tooltip.destroy()
            self.tooltip = None
