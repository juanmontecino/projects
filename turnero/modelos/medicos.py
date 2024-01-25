import csv
import requests

id_medico = 0
lista_medicos = []
ruta = "medicos.csv"

def iniciar_medicos():
    importar_datos_desde_csv(ruta)
    if len(lista_medicos) == 0:
        url = "https://randomuser.me/api/?results=15&inc=name,email,phone,id,login&exc=registered,location,picture,dob,gender&noinfo&password=upper,lower,6-6&nat=es"
        response = requests.get(url)
        datos = response.json()['results']
        if response.status_code == 200:
            tomar_datos_medicos_json(datos)

def tomar_datos_medicos_json(data):
    global id_medico
    global lista_medicos
    
    for user in data:
        if user['id']['value']:
            medico_formateado = {
                'id': id_medico + 1,
                'dni': user['id']['value'],
                'nombre': user['name']['first'],
                'apellido': user['name']['last'],
                'telefono': user['phone'],
                'matricula': user['login']['password'],
                'email': user['email'],
                'habilitado': "si"
            }
            lista_medicos.append(medico_formateado)
            id_medico += 1
    guardar_en_csv()

def guardar_en_csv():
    with open("medicos.csv", "w", newline='', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        
        header = lista_medicos[0].keys()
        csv_writer.writerow(header)

        for row in lista_medicos:
            csv_writer.writerow(row.values())

def importar_datos_desde_csv(ruta_archivo):
    global lista_medicos
    global id_medico
    lista_medicos = []
    
    with open(ruta_archivo, newline='', encoding='utf8') as csvfile:
        # Use DictReader instead of Reader
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # Convert id to int and strip other values
            id = int(row['id'])
            dni = row['dni'].strip()
            nombre = row['nombre'].strip()
            apellido = row['apellido'].strip()
            telefono = row['telefono'].strip()
            matricula = row['matricula'].strip()
            email = row['email'].strip()
            habilitado = row['habilitado'].strip()

            # Create a dictionary with the processed data
            datos = {'id': id, 'dni': dni, 'nombre': nombre, 'apellido': apellido,
                     'telefono': telefono, 'matricula': matricula, 'email': email, 'habilitado': habilitado}
            
            lista_medicos.append(datos)
            
        if len(lista_medicos)>0:
            id_medico = lista_medicos[-1]['id']+1
        else:
            id_medico = 0
        


def crear_medico(dni, nombre, apellido, telefono, matricula, email):
    global id_medico
    # Agrega el médico a la lista con un ID único
    lista_medicos.append({
        'id': id_medico+1,
        'dni': dni,
        'nombre': nombre,
        'apellido':apellido,
        'telefono': telefono,
        'matricula':matricula,
        'email': email,
        'habilitado': "si"
    })
    id_medico += 1
    guardar_en_csv()
    # Devuelve el médico recién creado
    return lista_medicos[-1]

def obtener_medico_por_id(id):
    # Utiliza list comprehension para filtrar la lista de médicos por ID
    medicos_filtrados = [medico for medico in lista_medicos if medico['id'] == id]
    
    # Devuelve el primer médico encontrado o None si no hay coincidencias
    return medicos_filtrados[0] if medicos_filtrados else None


def obtener_medicos():
    return lista_medicos

def editar_medico_por_id(id, dni, nombre, apellido, telefono, matricula, email,):
    # Recorre la lista de médicos
    for medico in lista_medicos:
        if medico["id"] == id:
            medico['dni'] = dni
            medico['nombre'] = nombre
            medico['apellido'] = apellido
            medico['telefono'] = telefono
            medico['matricula'] = matricula
            medico['email'] = email
            guardar_en_csv()  # Asumo que esta función guarda la lista actualizada en un archivo CSV
            return medico
    # Devuelve None si no se encuentra el médico
    return None

def deshabilitar_medico (id):
    for medico in lista_medicos:
        # Si el ID del médico coincide, devuelve True
        if medico["id"] == id:
            medico["habilitado"] = "no"
            guardar_en_csv()
            return medico
            
    # Devuelve False si no se encuentra el médico
    return False

def chequear_medico_habilitado(id):
    for medico in lista_medicos:
        # Si el ID del médico coincide, devuelve True
        if medico["id"] == id:
           if medico["habilitado"] == "si":
               return True
           else:
               return False
    # Devuelve False si no se encuentra el médico
    return False