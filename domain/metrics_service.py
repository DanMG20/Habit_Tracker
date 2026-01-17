from datetime import timedelta,datetime
from calendar import calendar,monthrange
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)

class MetricsService:
    def __init__(self,db,calendar_service):
        self.db = db
        self.calendar  = calendar_service # Aun no se si temporal 
        
        
    def calc_weekly_performance(self):
        ejecuciones = self.db.cargar_ejecuciones()
        week_start = self.calendar.calculate_week_start()  # Domingo
 
        habitos_totales = 0
        habitos_cumplidos = 0

        for habit in self.db.habitos:
            fecha_creacion = datetime.strptime(habit["Fecha_creacion"], "%Y-%m-%d")
            dias_ejecucion = habit["dias_ejecucion"]  # lista de 7 elementos [0|1]

            for i in range(7):
                day = week_start + timedelta(days=i)
                if day < fecha_creacion.date():
                    continue  # Ignorar días antes de la creación

                # Obtener índice correcto según weekday: domingo=0, lunes=1, ...
                # Si tu lista empieza en lunes, ajusta: weekday=dia_semana.weekday()
                if dias_ejecucion[i] == 1:  # Día programado
                    habitos_totales += 1
                    # Buscar si se cumplió
                    ejecucion = next(
                        (e for e in ejecuciones if e["nombre_habito"] == habit["nombre_habito"]
                        and e["fecha_ejecucion"] == day.strftime("%Y-%m-%d")),
                        None
                    )
                    if ejecucion and ejecucion.get("completado", False):
                        habitos_cumplidos += 1

        rendimiento = (habitos_cumplidos / habitos_totales * 100) if habitos_totales > 0 else 0
        rendimiento_redondeado = round(rendimiento)
        logger.info("weekly performance calculated")
        return rendimiento_redondeado
    
    def rendimiento_meses_anio(self):
        rendimiento_meses = []
        anio = self.dia_hoy_variable_3.year
        # número de días en el mes
        meses = [month for month in range(1, 13)]
        for mes in meses:
            rango = calendar.monthrange(anio,mes)[1]
            total=0
            for day in range(1, rango + 1):
                fecha = datetime(anio, mes, day)
                rendimiento = self.calcular_rendimiento_diario(fecha)
                total += rendimiento
                rendimiento_mes = total/rango
            rendimiento_meses.append(round(rendimiento_mes))
        tot=0
        for rend in rendimiento_meses:
            tot +=rend
        rendimiento_anual = round(tot/12,2)
        logger.info("montly & yearly ,performance calculated") 
        return rendimiento_meses,rendimiento_anual
    
    def calcular_rendimiento_diario(self, fecha):
        """
        Calcula el rendimiento diario en % de hábitos cumplidos.
        La semana comienza en domingo (domingo=0 ... sábado=6).
        
        fecha: datetime (día a evaluar)
        """
        fecha_dia = fecha
        dia_semana = (fecha_dia.weekday() + 1) % 7  # domingo=0 ... sábado=6

        ejecuciones = self.db.cargar_ejecuciones()
        habitos = self.db.habitos

        habitos_totales = 0
        habitos_cumplidos = 0

        for habito in habitos:
            fecha_creacion = datetime.strptime(habito["Fecha_creacion"], "%Y-%m-%d")

            # Solo contar si el hábito existía en ese día
            if fecha_creacion <= fecha_dia:
                # Verificar si ese hábito se debe ejecutar en ese día de la semana
                if habito["dias_ejecucion"][dia_semana]:
                    habitos_totales += 1

                    # Verificar si fue cumplido en ejecuciones
                    for ejec in ejecuciones:
                        ejec_fecha = datetime.strptime(ejec["fecha_ejecucion"], "%Y-%m-%d")
                        if (
                            ejec["nombre_habito"] == habito["nombre_habito"]
                            and ejec_fecha == fecha_dia
                            and ejec["completado"]
                        ):
                            habitos_cumplidos += 1
                            break  # evitar duplicados

        if habitos_totales == 0:
            return 0
        #logger.info("daily performance calculated")
        return (habitos_cumplidos / habitos_totales) * 100


    def calc_daily_performance_in_month(self):
        """
        Devuelve un diccionario con el rendimiento (%) por cada día del mes.
        Usa la función calcular_rendimiento_diario.
        """
        year = self.calendar.current_month_date.year
        month = self.calendar.current_month_date.month
        # número de días en el mes
        
        num_days = monthrange(year, month)[1]
        resultados = {}

        for day in range(1, num_days + 1):
            fecha = datetime(year, month, day)
            rendimiento = self.calcular_rendimiento_diario(fecha)
            resultados[day] = rendimiento

        return resultados
    
    def calc_average_monthly_performance(self):
        rend_diario_mes = self.calc_daily_performance_in_month()
        rend_diario_mes_lista = []
        
        for valor in rend_diario_mes.values():
            rend_diario_mes_lista.append(valor)
        days = self.calendar.get_month_days_range()
        total=0

        for dia in rend_diario_mes_lista: 
            total += dia

        monthly_average = total/days

        return round(monthly_average)