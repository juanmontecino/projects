from flask import Flask

app = Flask(__name__) 

from modelos.pacientes import iniciar_pacientes
from modelos.medicos import iniciar_medicos
from modelos.agenda_medicos import inicializar_agenda
from modelos.turnos import inicializar_turnos

from controladores.ruta_pacientes import pacientes_bp
from controladores.ruta_medicos import medicos_bp
from controladores.ruta_turnos import turnos_bp
from controladores.ruta_agenda_medicos import agenda_bp

iniciar_medicos()
iniciar_pacientes()
inicializar_agenda()
inicializar_turnos()

app.register_blueprint(medicos_bp)
app.register_blueprint(pacientes_bp)
app.register_blueprint(turnos_bp)
app.register_blueprint(agenda_bp)

if __name__ == '__main__':
    app.run(debug=True)