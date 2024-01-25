import csv
import os
from datetime import datetime, timedelta

# Variables globales que usaremos en este módulo
lista_turnos = []
ruta_archivo_turnos = 'turnos.csv'

def inicializar_turnos():
    if os.path.exists(ruta_archivo_turnos):
        importar_datos_desde_csv(ruta_archivo_turnos)

def importar_datos_desde_csv(ruta_archivo):
    global lista_turnos
    lista_turnos = []
    with open(ruta_archivo, newline='', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile)
        # Variable para controlar si ya se leyó la primera fila de encabezados
        primera_fila = True
        for row in reader:
            # Si es la primera fila, omítela y marca que ya se leyó
            if primera_fila:
                primera_fila = False
                continue
            if len(row) >= 4:
                id_medico = int(row[0])
                id_paciente = int(row[1])
                hora_turno = row[2].strip()
                fecha_solicitud = row[3].strip()

                fecha_solicitud_time = convertir_a_fecha(fecha_solicitud)
                # Crear un diccionario con los datos procesados
                datos = {'id_medico': id_medico, 'id_paciente': id_paciente, 'hora_turno': hora_turno,
                         'fecha_solicitud': fecha_solicitud_time.date()}
                lista_turnos.append(datos)
            
def exportar_a_csv():
    global lista_turnos
    with open(ruta_archivo_turnos, 'w', newline='', encoding='utf8') as csvfile:
        campo_nombres = ['id_medico','id_paciente','hora_turno','fecha_solicitud']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for turno in lista_turnos:
            writer.writerow(turno)

def obtener_turnos_por_id_medico(id_medico):
    """
    Obtiene los turnos de un médico en particular.
    """
    global lista_turnos
    return [turno for turno in lista_turnos if turno['id_medico'] == id_medico]

def convertir_a_fecha(fecha_str):
    """
    Convierte una fecha en formato string a un objeto datetime.
    """
    fecha_str = fecha_str.strip() #Corroboramos que no queden espacios
    fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
    return fecha_obj

def obtener_turnos_pendientes_por_id_medico(id_medico):
    #devuelve los turnos pendientes que tiene un médico en específico
    turnos_pendientes = []
    for turno in lista_turnos:
        if turno['id_medico'] == id_medico:
            fecha_hoy = datetime.now().date()
            fecha_turno = turno['fecha_solicitud']
            #si la fecha del turno es mayor o igual al día de la fecha, cuenta como turno pendiente
            if fecha_hoy <= fecha_turno:
                turnos_pendientes.append(turno)
    #si no hay turnos pendientes retornamos None
    if len(turnos_pendientes)>0:
        return turnos_pendientes
    else:
        return None
def obtener_turnos_pendientes_por_id_paciente(id_paciente):
    #devuelve los turnos pendientes que tiene un médico en específico
    turnos_pendientes = []
    for turno in lista_turnos:
        if turno['id_paciente'] == id_paciente:
            fecha_hoy = datetime.now().date()
            fecha_turno = turno['fecha_solicitud']
            #si la fecha del turno es mayor o igual al día de la fecha, cuenta como turno pendiente
            if fecha_hoy <= fecha_turno:
                turnos_pendientes.append(turno)
    #si no hay turnos pendientes retornamos None
    if len(turnos_pendientes)>0:
        return turnos_pendientes
    else:
        return None
    
def turno_cada_quince(hora_turno):
    """
    Verifica si el turno está programado cada 15 minutos.
    """
    hora, minuto = hora_turno.split(":")
    hora = int(hora)
    minuto = int(minuto)
    if minuto % 15 == 0:
        return True
    else:
        return False
    
def turno_en_menos_de_30_dias(fecha_solicitud):
    #verifica que el turno sea en menos de 30 días
    fecha_hoy = datetime.now().date()
    fecha_turno = convertir_a_fecha(fecha_solicitud).date()
    # Calcular la diferencia entre las fechas
    diferencia = fecha_turno - fecha_hoy
    print(diferencia)
    if diferencia <= timedelta(days=30) and diferencia.days >= 0:
        return True
    else:
        return False
    
def fecha_valida(fecha_solicitud):
    """
    Verifica si una fecha es válida, o sea, mayor al día de hoy.
    """
    fecha_solicitud_time = convertir_a_fecha(fecha_solicitud)
    if fecha_solicitud_time > datetime.now():
                return True
    return False
     
def turno_disponible(id_medico, hora_turno):
    """
    Verifica si un turno está disponible para un médico en particular.
    """
    global lista_turnos
    turnos_medico = obtener_turnos_pendientes_por_id_medico(id_medico)
    if turnos_medico is None:
        return True
    else:
        for turno in turnos_medico:
            if turno['hora_turno'] == hora_turno:
                return False
        return True

def agendar_turno(id_medico, id_paciente, hora_turno, fecha_solicitud):
    #agrega el turno a la lista de turnos
    fecha_solicitud_time = convertir_a_fecha(fecha_solicitud)
    turno_a_agregar ={
        "id_medico": id_medico,
        "id_paciente": id_paciente,
        "hora_turno": hora_turno,
        "fecha_solicitud": fecha_solicitud_time.date()
    }
    lista_turnos.append(turno_a_agregar)
    exportar_a_csv()
    return lista_turnos[-1]

def buscar_y_eliminar_turno(id_medico, id_paciente, hora_turno, fecha_solicitud):
    #busca un turno y si lo encuentra lo elimina
    global lista_turnos
    fecha_solicitud = convertir_a_fecha(fecha_solicitud)
    #verifica que todos los datos coincidan y, si así es, se elimina el turno
    for turno in lista_turnos:
        if (turno['id_medico'] == id_medico and
            turno['id_paciente'] == id_paciente and
            turno['hora_turno'] == hora_turno and
            turno['fecha_solicitud'] == fecha_solicitud.date()):
            lista_turnos.remove(turno)  
            exportar_a_csv()
            return turno
    return False
        