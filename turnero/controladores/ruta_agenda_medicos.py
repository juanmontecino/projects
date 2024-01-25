from flask import Blueprint, jsonify, request
from modelos.agenda_medicos import obtener_agenda_ordenada, agregar_dia_horario, eliminar_dia_horario, horas_validas, dia_valido, modificar_dia_de_atencion, horas_validas_para_modificar, dia_trabaja
from modelos.medicos import obtener_medico_por_id

#Crear blueprint
agenda_bp = Blueprint('agenda_bp', __name__)

@agenda_bp.route('/agenda_medicos', methods=['GET'])
def obtener_agenda_medicos():
    #devuelve la agenda de medicos ordenada por id_medico de menor a mayor
    agenda = obtener_agenda_ordenada()
    if agenda:
        return jsonify(agenda), 200
    else:
        return jsonify({'Error': 'No hay agenda de médicos'}), 404
    

@agenda_bp.route('/agenda_medicos/<int:id_medico>', methods=['POST'])
def agregar_dia_y_horario(id_medico):
    #agrega un dia y horario a la agenda de medicos
    if request.is_json:
        #chequeamos que se haya recibido un archivo JSON con los datos del dia y horario
        nuevo_dia = request.get_json()
        if 'dia_numero' in nuevo_dia and 'hora_inicio' in nuevo_dia and 'hora_fin' in nuevo_dia:
        #chequeamos que se adjunten todos los datos necesarios
            if obtener_medico_por_id(id_medico):
                if dia_valido(nuevo_dia["dia_numero"]): 
                    hora_inicio = nuevo_dia["hora_inicio"].strip()# quita los posibles espacios que recibe del json
                    hora_fin = nuevo_dia["hora_fin"].strip()
                    horas_son_validas = horas_validas(id_medico,nuevo_dia["dia_numero"],hora_inicio,hora_fin)# chequea que no exista un horario en ese dia y horario
                    if horas_son_validas:
                        # Llamada a la función para agregar día y horar
                        nuevo_horario = agregar_dia_horario(nuevo_dia["dia_numero"],hora_inicio,hora_fin, id_medico)
                        return jsonify(nuevo_horario,{"Mensaje": "Dia y horario agregados"}), 201
                    else:
                        return jsonify({'Error': 'La hora de inicio debe ser menor que la hora de fin o el medico ya esta cumpliendo un horario en ese momento'}), 400
                else:
                    return jsonify({'Error': 'El día debe ser un número entre 0 y 6'}), 400
            else:
                return jsonify({'Error': 'El médico no existe'}), 400
        else:
            return jsonify({'Error': 'Faltan datos'}), 400
    else:
        return jsonify({'Error': 'No se recibió información en formato JSON'}), 400
    
@agenda_bp.route('/agenda_medicos/<int:id_medico>', methods=['PUT'])
def modificar_agenda(id_medico):
    #modifica un turno de un día y un médico en específico
    if request.is_json:
        #chequea que se haya recibido un archivo JSON con los datos del dia y horario
        nuevo_dia = request.get_json()
        if 'dia_numero' in nuevo_dia and 'hora_inicio' in nuevo_dia and 'hora_fin' in nuevo_dia and 'nuevo_inicio' in nuevo_dia and 'nuevo_fin' in nuevo_dia:
            #chequea que se adjunten todos los datos necesarios
            if obtener_medico_por_id(id_medico): # chequea que el medico exista
                if dia_valido(nuevo_dia["dia_numero"]): #chequea que el numero sea un dia valido
                    if horas_validas_para_modificar(nuevo_dia["nuevo_inicio"],nuevo_dia["nuevo_fin"]):
                            if dia_trabaja(id_medico,nuevo_dia['dia_numero']):
                                agenda_formateada = modificar_dia_de_atencion(nuevo_dia['dia_numero'], nuevo_dia['hora_inicio'], nuevo_dia['hora_fin'], nuevo_dia["nuevo_inicio"], nuevo_dia["nuevo_fin"], id_medico)
                                if agenda_formateada:
                                    return jsonify(agenda_formateada,{'Mensaje': 'Agenda actualizada con éxito!!'}) , 201
                                else:
                                    return jsonify({'Error': 'No se encontro el horario'}), 404
                            else:
                                return jsonify({'Error': 'El día no existe en la agenda del médico'}), 400
                    else:
                        return jsonify({'Error': 'Las nueva hora fin no puede ser menor que la de inicio'}), 400
                else:
                    return jsonify({'Error': 'El día debe ser un número entre 0 y 6. Siendo 0 el día lunes.'}), 400
            else:
                return jsonify({'Error': 'El médico no existe'}), 400
        else:
            return jsonify({'Error': 'Datos incorrectos'}), 400
    else:
        return jsonify({'Error': 'No se recibió información en formato JSON'}), 400
    
@agenda_bp.route('/agenda_medicos/<int:id_medico>', methods=['DELETE'])
def eliminar_dia(id_medico):
    #elimina un día y todos los turnos que haya en él de un médico en específico
    if request.is_json:
        #chequea que se haya recibido un archivo JSON
        eliminar_dia = request.get_json()
        if 'dia_numero' in eliminar_dia:
            #chequea que se adjunte el número de día
            if dia_valido(eliminar_dia["dia_numero"]):
                agenda_formateada = eliminar_dia_horario(eliminar_dia['dia_numero'], id_medico)
                if agenda_formateada:
                    return jsonify({'Mensaje': 'Los turnos del dia han sido eliminados correctamente'}), 201
                else:
                    return jsonify({'Error': 'No se encontro el dia en la agenda'}), 404
            else:
                return jsonify({'Error': 'El día debe ser un número entre 0 y 6'}), 400
        else:
            return jsonify({'Error': 'Datos incorrectos'}), 400
    else:
        return jsonify({'Error': 'No se recibió información en formato JSON'}), 400
    
