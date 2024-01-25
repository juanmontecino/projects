import csv
import os
from datetime import datetime

lista_agenda = []
ruta_archivo = 'agenda_medicos.csv'

def inicializar_agenda():
    if os.path.exists(ruta_archivo):
        importar_datos_desde_csv(ruta_archivo)

def importar_datos_desde_csv(ruta_archivo):
    global lista_agenda
    lista_agenda = []
    
    with open(ruta_archivo, newline='', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile)
        
        # Variable para controlar si ya se leyó la primera fila de encabezados
        primera_fila = True
        
        for row in reader:
            # Si es la primera fila, omítela y marca que ya se leyó
            if primera_fila:
                primera_fila = False
                continue
            #si no es la primer fila, agrega los contenidos a la lista con sus correspondientes valores
            if len(row) >= 4:
                id_medico = int(row[0])
                dia_numero = int(row[1])
                hora_inicio = row[2].strip()
                hora_fin = row[3].strip()
                fecha_actualizacion = row[4].strip()

                # Crear un diccionario con los datos procesados
                datos = {'id_medico': id_medico, 'dia_numero': dia_numero, 'hora_inicio': hora_inicio, 'hora_fin': hora_fin, 'fecha_actualizacion': fecha_actualizacion}

                lista_agenda.append(datos)

def guardar_en_csv():
    with open("agenda_medicos.csv", "w", newline='', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        
        header = lista_agenda[0].keys()
        csv_writer.writerow(header)

        for row in lista_agenda:
            csv_writer.writerow(row.values())

def obtener_agenda_ordenada():
    #devuelve la agenda con todos los turnos ordenada de menor a mayor por id_medico, dia y hora_inicio
    global lista_agenda
    if len(lista_agenda) > 0:
        lista_medicos_ordenada = sorted(lista_agenda, key=lambda x: (x['id_medico'], x['dia_numero'], x['hora_inicio']))
        return lista_medicos_ordenada
    else:
        return None

def agregar_dia_horario(dia, horario_inicio, horario_fin, id_medico):
    #agrega un nuevo dia y horario para un medico en específico
    global lista_agenda
    # Obtener la fecha actual para actualizarla en el diccionario
    fecha_actualizacion = datetime.now().strftime('%Y-%d-%m')
    
    # Convertir las horas a objetos time y luego formatearlas como cadenas sin segundos
    hora_inicio = datetime.strptime(horario_inicio, '%H:%M').time()
    hora_fin = datetime.strptime(horario_fin, '%H:%M').time()
    # Agregar los datos a la lista de agenda
    lista_agenda.append({
        'id_medico': id_medico,
        'dia_numero': dia,
        'hora_inicio': hora_inicio.strftime('%H:%M'),
        'hora_fin': hora_fin.strftime('%H:%M'),
        'fecha_actualizacion': fecha_actualizacion
    })

    guardar_en_csv()
    return lista_agenda[-1]

def modificar_dia_de_atencion(dia, hora_inicio, hora_fin, hora_inicio_nuevo, hora_fin_nuevo, id_medico):
    #modifica un dia y horario de atencion de un medico en específico
    global lista_agenda

    for agenda in lista_agenda:
        #chequeamos que las horas proporcionadas coincidan con algún turno y, de ser así, las actualizamos
        if hora_inicio == agenda['hora_inicio'] and hora_fin == agenda['hora_fin']:
            agenda['hora_inicio'] = hora_inicio_nuevo
            agenda['hora_fin'] = hora_fin_nuevo
            guardar_en_csv()
            return agenda  # Devuelve el último elemento modificado
                
    return None  # Retorna None si no se encontró ninguna coincidencia o si no se modificó ningún elemento

def horas_validas_para_modificar(nuevo_inicio, nuevo_fin):
    #chequea que las horas de inicio proporcionadas no sean mayores que las horas de fin
    if nuevo_inicio < nuevo_fin:
        return True
    return False

def eliminar_dia_horario(dia, id_medico):
    #elimina todos los turnos que tenga un médico en específico en un día en específico
    global lista_agenda
    bandera = False
    for agenda in lista_agenda:
        if agenda['id_medico'] == id_medico:
            if agenda['dia_numero'] == dia:
                lista_agenda.remove(agenda)
                guardar_en_csv()
                bandera = True
    if bandera:
        return True
    return False

def fecha_que_trabaja(id_medico, fecha_solicitud):
    #retorna si un médico trabaja o no el día de fecha_solicitud
    global lista_agenda
    #pasamos la fecha al formato necesario para compararla
    fecha_str = fecha_solicitud.strip()
    fecha_solicitud = datetime.strptime(fecha_str, '%Y-%m-%d')
    for agenda in lista_agenda:
        if agenda['id_medico'] == id_medico:
            dia_de_la_semana = (fecha_solicitud.weekday() + 1) % 7#formatea el valor da los dias para que domingo valga 0 y lunes valga 1

            if agenda['dia_numero'] == dia_de_la_semana:
                print(dia_de_la_semana)
                return True
    return False

def horas_validas(id, dia, hora_inicio, hora_fin):
    #chequea que las horas proporcionadas no se pisen con otros turnos de un mismo médico
    global lista_agenda
    hora_inicio = datetime.strptime(hora_inicio, '%H:%M').time()
    hora_fin = datetime.strptime(hora_fin, '%H:%M').time()

    if not horas_validas_para_modificar(hora_inicio, hora_fin):
        return False
    
    for agenda in lista_agenda:
        if agenda['id_medico'] == id and agenda['dia_numero'] == dia:
            hora_inicio_agenda = datetime.strptime(str(agenda["hora_inicio"]), '%H:%M').time()
            hora_fin_agenda = datetime.strptime(str(agenda["hora_fin"]), '%H:%M').time()
            
            # Verifica que las nuevas horas no estén completamente contenidas dentro de una cita existente
            if hora_inicio_agenda <= hora_inicio < hora_fin_agenda or hora_inicio_agenda < hora_fin <= hora_fin_agenda:
                return False
    return True

def hora_que_trabaja(fecha_solicitud, hora_buscada, id_medico):
    #chequea si un medico trabaja en una fecha y hora específicas
    global lista_agenda
    fecha_str = fecha_solicitud.strip()
    fecha_solicitud = datetime.strptime(fecha_str, '%Y-%m-%d')
    dia_de_la_semana = (fecha_solicitud.weekday() + 1) % 7#formatea el valor da los dias para que domingo valga 0 y lunes valga 1
    for agenda in lista_agenda:
        if agenda['id_medico'] == id_medico:
            if agenda['dia_numero'] == dia_de_la_semana:
                hora_buscada = datetime.strptime(hora_buscada, '%H:%M').time()
                hora_inicio = datetime.strptime(agenda['hora_inicio'], '%H:%M').time()
                hora_fin = datetime.strptime(agenda['hora_fin'], '%H:%M').time()
                if hora_buscada >= hora_inicio and hora_buscada <= hora_fin:
                    return True
    return False

def dia_valido(dia):
    #chequea que el numero sea un dia valido
    if 0 <= dia <= 6: 
        return True
    return False

def dia_trabaja(id_medico, dia):
    #chequea si un medico trabaja en un día en específico
    global lista_agenda
    for agenda in lista_agenda:
        if agenda['id_medico'] == id_medico:
            if agenda['dia_numero'] == dia:
                return True
    return False