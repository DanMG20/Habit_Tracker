from calendar import monthrange
from datetime import date, timedelta

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class MetricsService:
    def __init__(self):
        pass
        

    def calc_weekly_performance(self,habits, executions, week_start):
        habitos_totales = 0
        habitos_cumplidos = 0

        for habit in habits:
            creation_date = habit["creation_date"]
            execution_days = habit["execution_days"]  # lista de 7 elementos [0|1] 
     
    
            for i in range(7):
                day = week_start + timedelta(days=i)
                if day < creation_date:
                    continue  # Ignorar días antes de la creación

                # Obtener índice correcto según weekday: domingo=0, lunes=1, ...
                # Si tu lista empieza en lunes, ajusta: weekday=dia_semana.weekday()
        
                if execution_days[i] == 1:  # Día programado
                    habitos_totales += 1
                    # Buscar si se cumplió
                   
                    execution = next(
                        (
                            e
                            for e in executions
                            if e["habit_id"] == habit["id"]
                            and e["execution_date"] == day
                        ),
                        None,
                    )


                    if execution and execution["executed"]:
                        habitos_cumplidos += 1
   
        rendimiento = (
            (habitos_cumplidos / habitos_totales * 100) if habitos_totales > 0 else 0
        )
        rendimiento_redondeado = round(rendimiento)
        return rendimiento_redondeado

    def calc_yearly_performance(self,get_year,executions, habits):
        rendimiento_meses = []
        year = get_year()
    

        meses = [month for month in range(1, 13)]
        for mes in meses:
            rango = monthrange(year, mes)[1]
            total = 0
            for day in range(1, rango + 1):
                fecha = date(year, mes, day)
                rendimiento = self.calc_daily_performance(fecha,executions, habits)
                total += rendimiento
                rendimiento_mes = total / rango
            rendimiento_meses.append(round(rendimiento_mes))
        tot = 0
        for rend in rendimiento_meses:
            tot += rend
        rendimiento_anual = round(tot / 12, 2)

        return {"monthly":rendimiento_meses,
                "yearly": rendimiento_anual
            }

    def calc_daily_performance(self, fecha, executions, habits):
        """
        Calcula el rendimiento diario en % de hábitos cumplidos.
        La semana comienza en domingo (domingo=0 ... sábado=6).

        fecha: datetime (día a evaluar)
        """
        fecha_dia = fecha
        dia_semana = (fecha_dia.weekday() + 1) % 7  # domingo=0 ... sábado=6

        ejecuciones = executions
        habitos = habits

        habitos_totales = 0
        habitos_cumplidos = 0

        for habito in habitos:
            fecha_creacion = habito["creation_date"]

            # Solo contar si el hábito existía en ese día
            if fecha_creacion <= fecha_dia:
                # Verificar si ese hábito se debe ejecutar en ese día de la semana
                if habito["execution_days"][dia_semana]:
                    habitos_totales += 1

                    # Verificar si fue cumplido en ejecuciones
                    for ejec in ejecuciones:
                        ejec_fecha = ejec["execution_date"]
                        if (
                            ejec["habit_id"] == habito["id"]
                            and ejec_fecha == fecha_dia
                            and ejec["executed"]
                        ):
                            habitos_cumplidos += 1
                            break  # evitar duplicados

        if habitos_totales == 0:
            return 0
        
        daily_performance = (habitos_cumplidos / habitos_totales) * 100
        return daily_performance

    def calc_daily_performance_in_month(self, get_month, get_year,executions,habits):
        """
        Devuelve un diccionario con el rendimiento (%) por cada día del mes.
        Usa la función calcular_rendimiento_diario.
        """
        year = get_year()
        month = get_month()
        # número de días en el mes

        num_days = monthrange(year, month)[1]
        resultados = {}

        for day in range(1, num_days + 1):
            fecha = date(year, month, day)
            rendimiento = self.calc_daily_performance(fecha,executions,habits)
            resultados[day] = rendimiento

        return resultados

    def calc_average_monthly_performance(self,get_month, get_year,get_month_range,executions,habits):
        rend_diario_mes = self.calc_daily_performance_in_month(get_month, get_year,executions,habits)
        rend_diario_mes_lista = []

        for valor in rend_diario_mes.values():
            rend_diario_mes_lista.append(valor)
        days = get_month_range()
        total = 0

        for dia in rend_diario_mes_lista:
            total += dia

        monthly_average = total / days

        return round(monthly_average)
