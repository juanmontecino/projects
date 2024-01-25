from flask import Blueprint, jsonify, request
from modelos.turnos import obtener_turnos_por_id_medico,fecha_valida, obtener_turnos_pendientes_por_id_medico, buscar_y_eliminar_turno, agendar_turno, turno_en_menos_de_30_dias, turno_disponible, turno_cada_quince
from modelos.medicos import chequear_medico_habilitado, obtener_medico_por_id
from modelos.agenda_medicos import fecha_que_trabaja, hora_que_trabaja
from modelos.pacientes import obtener_paciente_por_id

turnos_bp = Blueprint('turnos_bp', __name__)

@turnos_bp.route('/turnos/<int:id>', methods=['GET'])
def obtener_turnos_por_id(id):
    #devuelve todos los turnos de un médico, ya sean viejos o futuros
    medico_existe = obtener_medico_por_id(id) # chequea que el medico exista
    if medico_existe:
        turnos = obtener_turnos_por_id_medico(id)
        if len(turnos) > 0:
            return jsonify(turnos), 200
        else:
            return jsonify({'Mensaje': 'No hay turnos de este médico'}), 404
    else:
        return jsonify({'Mensaje': 'No existe el médico'}), 404


@turnos_bp.route('/turnos_pendientes/<int:id>', methods=['GET'])
def obtener_turnos_pendientes(id):
    #devuelve los turnos pendientes que tiene un médico en específico
    medico_existe = obtener_medico_por_id(id) # chequea que el medico exista
    if medico_existe:
        turnos_pendientes = obtener_turnos_pendientes_por_id_medico(id)
        if len(turnos_pendientes) > 0:
            return jsonify(turnos_pendientes), 200
        else:
            return jsonify({'Mensaje': 'No hay turnos pendientes de este médico'}), 404
    else:
        return jsonify({'Mensaje': 'No existe el médico'}), 404

@turnos_bp.route('/turnos/<int:id_medico>', methods=['POST'])
def agregar_turno(id_medico):
    #agrega un turno si cumple con todas las condiciones
    if request.is_json:
        #chequeamos que se recibe un json
        turno = request.get_json()
        #chequeamos que esten todos los datos en el json
        if 'id_paciente' in turno and 'hora_turno' in turno and 'fecha_solicitud' in turno:
            #chequeamos que el medico exista
            if obtener_medico_por_id(id_medico):
                #chequeamos que la fecha solicitud sea una fecha valida
                if obtener_paciente_por_id(turno['id_paciente']):
                    #chequeamos que exista el paciente
                    if fecha_valida(turno['fecha_solicitud']):
                    #chequeamos que el turno sea en menos de 30 dias
                        if turno_en_menos_de_30_dias(turno['fecha_solicitud']):
                            #chequeamos que el turno sea cada 15 minutos
                            if turno_cada_quince(turno['hora_turno']):
                                #chequeamos que el medico este habilitado
                                if chequear_medico_habilitado(id_medico):
                                    #chequeamos que el turno sea un dia que ese medico trabaja
                                    if fecha_que_trabaja(id_medico, turno['fecha_solicitud']):
                                        #chequeamos si el turno es dentro del rango horario del medico
                                        if hora_que_trabaja(turno["fecha_solicitud"], turno['hora_turno'], id_medico):
                                            #chequeamos que el turno este disponible
                                            if turno_disponible(id_medico, turno['hora_turno']):
                                                #agregamos el turno a la lista de turnos
                                                turno = agendar_turno(id_medico, turno['id_paciente'], turno['hora_turno'], turno['fecha_solicitud'])
                                                return jsonify(turno,{"Mensaje": 'Turno creado exitosamente!'}), 201
                                            else:
                                                return jsonify({'Mensaje': 'Este turno no se encuentra disponible'}), 400
                                        else:
                                            return jsonify({'Mensaje': 'El medico no trabaja en el horario solicitado'}), 400
                                    else:
                                        return jsonify({'Mensaje': 'El medico no trabaja en el día solicitado'}), 400
                                else:
                                    return jsonify({'Mensaje': 'El medico no esta habilitado'}), 400
                            else:
                                return jsonify({'Mensaje': 'El turno debe ser en los minutos "00"-"15"-"30"-"45"'}), 400
                        else:
                            return jsonify({'Mensaje': 'El turno debe ser en menos de 30 días'}), 400
                    else:
                        return jsonify({'Mensaje': 'La fecha no puede ser anterior al dia actual'}), 400
                else:
                    return jsonify({'Mensaje': 'No existe el paciente'}), 404
            else:
                return jsonify({'Mensaje': 'No existe el médico'}), 404
        else:
            return jsonify({'Error': 'Faltan datos'}), 400
    else:
        return jsonify({'Error': 'No se ha recibido un JSON válido'}), 400
                                        
@turnos_bp.route('/turnos/<int:id_medico>', methods=['DELETE'])
#debe ingresas id_medico
def registrar_anulacion_turno(id_medico):
    #elimina un turno si cumple con todas las condiciones
    if request.is_json:
        #chequeamos que se recibe un json
        turno = request.get_json()
        #chequeamos que esten todos los datos en el json
        if 'id_paciente' in turno and 'hora_turno' in turno and 'fecha_solicitud' in turno:
            turno_a_eliminar = buscar_y_eliminar_turno(id_medico, turno['id_paciente'], turno['hora_turno'], turno['fecha_solicitud'])
            if turno_a_eliminar:    
                return jsonify(turno_a_eliminar,{'Mensaje': 'Turno eliminado correctamente'}), 200
            else:
                return jsonify({'Mensaje': 'No se ha encontrado el turno'}), 404
        else:
            return jsonify({'Error': 'Faltan datos'}), 400
    else:
        return jsonify({'Error': 'No se ha recibido un JSON válido'}), 400