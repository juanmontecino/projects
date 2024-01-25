import csv
import requests

id_paciente = 0
lista_pacientes = []
ruta = "pacientes.csv"

def iniciar_pacientes():
    importar_datos_desde_csv(ruta)
    if len(lista_pacientes) == 0:
        url = "https://randomuser.me/api/?results=100&inc=name,email,location,phone,id,login&exc=registered,picture,dob,gender&noinfo&nat=es"
        response = requests.get(url)
        datos = response.json()['results']
        if response.status_code == 200:
            tomar_datos_pacientes_json(datos)

def tomar_datos_pacientes_json(data):
    global id_paciente
    global lista_pacientes
    
    for user in data:
        if user['id']['value']:
            paciente_formateado = {
                'id': id_paciente + 1,
                'dni': user['id']['value'],
                'nombre': user['name']['first'],
                'apellido': user['name']['last'],
                'telefono': user['phone'],
                'email': user['email'], 
                'direccion_calle': user['location']['street']['name'],
                'direccion_numero': user['location']['street']['number'],
            }
            lista_pacientes.append(paciente_formateado)
            id_paciente += 1
    guardar_en_csv()

def guardar_en_csv():
    with open("pacientes.csv", "w", newline='', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        
        header = lista_pacientes[0].keys()
        csv_writer.writerow(header)

        for row in lista_pacientes:
            csv_writer.writerow(row.values())

def importar_datos_desde_csv(ruta_archivo):
    global lista_pacientes
    global id_paciente
    lista_pacientes = []

    with open(ruta_archivo, newline='', encoding='utf8') as csvfile:
        # Use DictReader instead of Reader
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Convert id to int and strip other values
            id_paciente = int(row['id'])
            dni = row['dni'].strip()
            nombre = row['nombre'].strip()
            apellido = row['apellido'].strip()
            telefono = row['telefono'].strip()
            email = row['email'].strip()
            direccion_calle = row['direccion_calle'].strip()
            direccion_numero = row['direccion_numero'].strip()

            # Create a dictionary with the processed data
            datos = {'id': id_paciente, 'dni': dni, 'nombre': nombre, 'apellido': apellido,
                     'telefono': telefono, 'email': email, 'direccion_calle': direccion_calle,
                     'direccion_numero': direccion_numero}
            
            lista_pacientes.append(datos)

        if len(lista_pacientes) > 0:
            id_paciente = lista_pacientes[-1]['id'] + 1
        else:
            id_paciente = 0


def crear_paciente(dni, nombre, apellido, telefono, email, direccion_calle, direccion_numero):
    global id_paciente
    # Agrega al paciente a la lista con un ID único
    lista_pacientes.append({
        'id': id_paciente + 1,
        'dni': dni,
        'nombre': nombre,
        'apellido': apellido,
        'telefono': telefono,
        'email': email,
        'direccion_calle': direccion_calle,
        'direccion_numero': direccion_numero,
        'habilitado': "si"
    })
    id_paciente += 1
    guardar_en_csv()
    # Devuelve el paciente recién creado
    return lista_pacientes[-1]

def obtener_paciente_por_id(id):
    # Recorre la lista de pacientes
    for paciente in lista_pacientes:
        # Si el ID del paciente coincide, devuelve el paciente
        if paciente["id"] == id:
            return paciente
    # Devuelve None si no se encuentra el paciente
    return None

def obtener_pacientes():
    return lista_pacientes

def editar_paciente_por_id(id, dni, nombre, apellido, telefono, email, direccion_calle, direccion_numero):
    # Recorre la lista de pacientes
    for paciente in lista_pacientes:
        if paciente["id"] == id:
            paciente['dni'] = dni
            paciente['nombre'] = nombre
            paciente['apellido'] = apellido
            paciente['telefono'] = telefono
            paciente['email'] = email
            paciente['direccion_calle'] = direccion_calle
            paciente['direccion_numero'] = direccion_numero
            guardar_en_csv()
            return paciente
    # Devuelve None si no se encuentra el paciente
    return None

def existe_paciente(id):
    # Recorre la lista de pacientes
    for paciente in lista_pacientes:
        # Si el ID del paciente coincide, devuelve True
        if paciente["id"] == id:
            return True
    # Devuelve False si no se encuentra el paciente
    return False

def eliminar_paciente_por_id(id):
    global lista_pacientes
    # Crea una nueva lista sin el paciente a eliminar
    paciente_a_eliminar = [paciente for paciente in lista_pacientes if paciente["id"] == id]
    if len(paciente_a_eliminar) > 0:
        lista_pacientes.remove(paciente_a_eliminar[0])
        guardar_en_csv() 
        return paciente_a_eliminar[0]
    else:
        return None
