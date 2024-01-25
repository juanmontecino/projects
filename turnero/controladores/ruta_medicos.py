from flask import Blueprint, jsonify, request
from modelos.medicos import obtener_medicos, obtener_medico_por_id, crear_medico, editar_medico_por_id, deshabilitar_medico

# Crear un blueprint
medicos_bp = Blueprint('medicos_bp', __name__)

@medicos_bp.route('/medicos', methods=['GET'])
def buscar_medicos():
    medico = obtener_medicos()
    if len(medico) > 0:
        return jsonify(medico), 200
    else:
        return jsonify({'Error': 'No hay médicos cargados'}), 404

@medicos_bp.route('/medicos/<int:id>', methods=['GET'])
def buscar_medico_id(id):
    medico = obtener_medico_por_id(id)
    if medico:
        return jsonify(medico), 200
    else:
        return jsonify({'Error': 'Médico no encontrado'}), 404
    
@medicos_bp.route('/medicos', methods=['POST'])
def nuevo_medico():
    if request.is_json:
        nuevo = request.get_json()
        if 'dni' in nuevo and 'nombre' in nuevo and 'apellido' in nuevo and 'telefono' in nuevo and 'matricula' in nuevo and 'email' in nuevo:         
            medico_creado = crear_medico(nuevo['dni'], nuevo['nombre'], nuevo['apellido'], nuevo['telefono'], nuevo['matricula'],nuevo['email'])
            return jsonify(medico_creado,{'Mensaje:' : 'Medico creado exitosamente'}), 201
        else:
            return jsonify({'Error': 'Faltan datos para crear el médico'}), 400
    else:
        return jsonify({'Error': 'No se recibió el formato JSON'}), 400
    
@medicos_bp.route('/medicos/<int:id>', methods=['PUT'])
def editar_medico_id(id):
    if request.is_json:
        nuevo = request.get_json()
        medico_existente = obtener_medico_por_id(id)
        if medico_existente:
            if 'habilitado' not in nuevo:
                if 'dni' in nuevo and 'nombre' in nuevo and 'apellido' in nuevo and 'telefono' in nuevo and 'matricula' in nuevo and 'email' in nuevo:
                    medico = editar_medico_por_id(id,nuevo['dni'], nuevo['nombre'], nuevo['apellido'], nuevo['telefono'], nuevo['matricula'],nuevo['email'])
                    if medico:
                        return jsonify(medico,{'Mensaje:' : 'Medico modificado exitosamente'}), 200
                    else:
                        return jsonify({'Error': 'Médico no encontrado'}), 404
                else:
                    return jsonify({'Error': 'Faltan datos para editar el médico'}), 400
            else:
                return jsonify({'Error': 'No esta permitido deshabilitar por esta ruta'}), 400
        else:
            return jsonify({'Error': 'Médico no encontrado'}), 404
    else:
        return jsonify({'Error': 'No se recibió el formato JSON'}), 400

@medicos_bp.route('/medicos/deshabilitar/<int:id>', methods=['PUT'])
def deshabilitar_medico_id(id):
    medico = deshabilitar_medico(id)
    if medico:
        return jsonify(medico, {'Mensaje': 'Medico deshabilitado exitosamente'}),200
    else:
        return jsonify({'Error': 'Médico no encontrado'}), 404



