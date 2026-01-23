from infrastructure.logging.logger import get_logger
from ui.check_panel_base import CheckPanelBase
logger = get_logger(__name__)



class DeleteHabitCheckPanel(CheckPanelBase):
    def __init__(
        self,
        master,
        fonts,
        theme_colors,
        habits,
        on_delete,
    ):
        super().__init__(
            master=master,
            fonts=fonts,
            theme_colors=theme_colors,
            date=None,
            habits=habits,
            completed_habits=set(),
            on_check=on_delete,
            title="Selecciona el hábito para eliminarlo",
            subtitle="ESTA ACCIÓN NO SE PUEDE DESHACER",
        )

        logger.info("Succesfully built")

    def refresh_panels(self):
        # refrescar este panel
        self.habits = self.db.habitos
        for w in self.scroll.winfo_children():
            w.destroy()
        self.build()

        # refrescar otros paneles
        self.master.listar_habitos()
        self.master.lista_habitos_frame_semana()
        self.master.listar_habitos_ayer()
