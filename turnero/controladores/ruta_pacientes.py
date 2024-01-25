from flask import Blueprint, jsonify, request
from modelos.pacientes import obtener_pacientes, obtener_paciente_por_id, crear_paciente, editar_paciente_por_id, eliminar_paciente_por_id
from modelos.turnos import obtener_turnos_pendientes_por_id_paciente

# Crear un blueprint
pacientes_bp = Blueprint('pacientes_bp', __name__)

@pacientes_bp.route('/pacientes', methods=['GET'])
def buscar_pacientes():
    paciente = obtener_pacientes()
    if len(paciente) > 0:
        return jsonify(paciente), 200
    else:
        return jsonify({'Error': 'No hay pacientes cargados'}), 404

@pacientes_bp.route('/pacientes/<int:id>', methods=['GET'])
def buscar_paciente_id(id):
    paciente = obtener_paciente_por_id(id)
    if paciente:
        return jsonify(paciente), 200
    else:
        return jsonify({'Error': 'Paciente no encontrado'}), 404
    
@pacientes_bp.route('/pacientes', methods=['POST'])
def nuevo_paciente():
    if request.is_json:
        nuevo = request.get_json()
        if "id" not in nuevo:
            if 'dni' in nuevo and 'nombre' in nuevo and 'apellido' in nuevo and 'telefono' in nuevo and 'email' in nuevo and 'direccion_calle' in nuevo and 'direccion_numero' in nuevo:         
                paciente_creado = crear_paciente(
                    nuevo['dni'], nuevo['nombre'], nuevo['apellido'],
                    nuevo['telefono'], nuevo['email'],
                    nuevo['direccion_calle'], nuevo['direccion_numero']
                )
                return jsonify(paciente_creado,{'Mensaje': 'Paciente creado exitosamente'}), 201
            else:
                return jsonify({'Error': 'Faltan datos para crear el paciente'}), 400
        else:
            return jsonify({'Error': 'No se le puede asignar id a los pacientes'}), 400
    else:
        return jsonify({'Error': 'No se recibió el formato JSON'}), 400
    
@pacientes_bp.route('/pacientes/<int:id>', methods=['PUT'])
def editar_paciente_id(id):
    paciente_existe = obtener_paciente_por_id(id)
    if request.is_json:
        nuevo = request.get_json()
        paciente_existe = obtener_paciente_por_id(id)
        if paciente_existe:
            if "id" not in nuevo:
                if 'dni' in nuevo and 'nombre' in nuevo and 'apellido' in nuevo and 'telefono' in nuevo and 'email' in nuevo and 'direccion_calle' in nuevo and 'direccion_numero' in nuevo:
                    paciente = editar_paciente_por_id(
                        id, nuevo['dni'], nuevo['nombre'], nuevo['apellido'],
                        nuevo['telefono'], nuevo['email'],
                        nuevo['direccion_calle'], nuevo['direccion_numero']
                    )
                    if paciente:
                        return jsonify(paciente,{'Mensaje': 'Paciente modificado exitosamente'}), 200
                    else:
                        return jsonify({'Error': 'Paciente no encontrado'}), 404
                else:
                    return jsonify({'Error': 'Faltan datos para editar el paciente'}), 400
            else:
                return jsonify({'Error': 'No se le puede asignar id a los pacientes'}), 400
        else:
            return jsonify({'Error': 'Paciente no encontrado'}), 404
    else:
        return jsonify({'Error': 'No se recibió el formato JSON'}), 400
    

    
@pacientes_bp.route('/pacientes/<int:id>', methods=['DELETE'])
def eliminar_paciente_id(id):
    paciente_existe = obtener_paciente_por_id(id)
    if paciente_existe:
        deudas = obtener_turnos_pendientes_por_id_paciente(id)
        if not deudas:
            paciente =eliminar_paciente_por_id(id)
            if paciente:
                return jsonify(paciente,{'Mensaje': 'Paciente eliminado exitosamente'}),200
            else:
                return jsonify({'Error': 'Paciente no encontrado'}), 404
        else:   
            return jsonify({'Error': 'El paciente posee un turno pendiente'}), 401
    else:
        return jsonify({'Error': 'Paciente no encontrado'}), 404




 