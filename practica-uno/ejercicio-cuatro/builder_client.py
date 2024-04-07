import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"
# GET obtener a todos los estudiantes por la ruta /estudiantes
ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)


print("------------------------CREA PACIENTE----------------------")
# Crea un nuevo paciente
ruta_post = url + "pacientes"
nuevo_paciente = {
    "nombre": "Sonia",
    "apellido": "Margaret",
    "edad": 19,
    "genero": "Femenino",
    "diagnostico": "Diabetes",
    "doctor": "Rosa Vargas",
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_paciente)
print(post_response.text)


print("------------------------FILTRADO POR CI----------------------")
ruta_get = url + "pacientes/2"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("------------------DIAGNOSTICO--------------------")
ruta_get = url + "pacientes/?diagnostico=Diabetes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)


print("------------------DOCTOR PEDRO PEREZ--------------------")
ruta_get = url + "pacientes/?doctor=Pedro Perez"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("------------------actualizar paciente--------------------")

ruta_put = url + "pacientes/1"
paciente_actualizado = {
    "ci": 11,
    "nombre": "Lola",
    "apellido": "Paloza",
    "edad": "10",
    "genero": "Femenino",
    "diagnostico": "Sarampion",
    "doctor": "Soyla Zerda",
}
put_response = requests.request(method="PUT", url=ruta_put, json=paciente_actualizado)
print(put_response.text)



print("------------------ELIMINAR PACIENTE-------------")
ruta_delete = url + "pacientes/2"
delete_response = requests.request(method="DELETE", url=ruta_delete)
print(delete_response.text)
