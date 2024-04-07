import requests

print("----------LISTAR TODOS LOS ANIMALES---------")
# Consultando a un servidor RESTful
url = "http://localhost:8000/"
# GET obtener a todos los animales por la ruta /animales
ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)


print("----------CREA ANIMAL--------")
# Crea un nuevo animal
ruta_post = url + "animales"
nuevo_animal = {
    "nombre": "Parrot",
    "especie": "Conures",
    "genero": "Femenino",
    "edad": 3,
    "peso": 50,
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print(post_response.text)


print("----------BUSCAR POR ESPECIE---------")
ruta_get = url + "animales/?especie=Conures"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)


print("----------BUSCAR POR GENERO---------")
ruta_get = url + "animales/?genero=Masculino"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("----------ACTUALIZAR ANIMAL---------")
ruta_put = url + "animales/3"
animal_actualizado = {
    "id": 33,
    "nombre": "Python",
    "especie": "Burmese",
    "genero": "Masculino",
    "edad": 5,
    "peso": 7,
}
put_response = requests.request(method="PUT", url=ruta_put, json=animal_actualizado)
print(put_response.text)

print("----------ELIMINAR ANIMAL---------")
ruta_delete = url + "animales/33"
delete_response = requests.request(method="DELETE", url=ruta_delete)
print(delete_response.text)
