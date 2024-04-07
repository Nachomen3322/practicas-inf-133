import requests

# Define la URL base del servidor
url = "http://localhost:8000/"

print("------------------------LISTAR TODOS LOS MENSAJES----------------")
# GET obtener todos los mensajes
ruta_get = url + "mensajes"
get_response = requests.get(ruta_get)
print(get_response.text)

print("------------------------CREAR UN MENSAJE----------------")
ruta_post = url +"mensajes"

nuevo_mensaje = {"contenido": "Hola pythonista"}
response_post = requests.post(ruta_post, json=nuevo_mensaje)
print(response_post.text)

print("------------------------BUSCAR POR ID----------------")
ruta_get = url + "mensajes"
response = requests.get(f"{ruta_get}/{2}")
print(response.text)

print("------------------------ACTUALIZAR CONTENIDO DE UN MENSAJE----------------")
ruta_put = url + "mensajes"
nuevo_contenido = {"contenido": "Contenido actualizado"}
response_put = requests.put(f"{ruta_put}/{1}", json=nuevo_contenido)
print(response_put.text)

print("------------------------ELIMINAR UN MENSAJE----------------")
ruta_delete = url + "mensajes"
response_delete = requests.delete(f"{ruta_delete}/{2}")
print(response.text)

