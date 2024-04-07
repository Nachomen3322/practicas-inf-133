import requests

url = "http://localhost:8000/graphql"

# Definir la consulta GraphQL
query_lista = """
    {
        plantas{
            id
            nombre_comun
            especie
            edad
            altura
            frutos
        }
    }
"""

# Hacer la solicitud POST al servidor GraphQL
response = requests.post(url, json={"query": query_lista})
print(response.text)


query = """
    {
        plantaPorFrutos(fruto: True){
            nombre_comun
        }
    }
"""
response_mutation = requests.post(url, json={"query": query})
print(response_mutation.text)

crearEstudiante1 = """
mutation {
    crearEstudiante(nombre: "Juan", apellido: "Pérez", carrera: "Arquitectura") {
        estudiante {
            id  
            nombre
            apellido
            carrera
        }
    }
}
"""

crearEstudiante2 = """
mutation {
    crearEstudiante(nombre: "María", apellido: "Gonzalez", carrera: "Arquitectura") {
        estudiante {
            id  
            nombre
            apellido
            carrera
        }
    }
}
"""

crearEstudiante3 = """
mutation {
    crearEstudiante(nombre: "Carlos", apellido: "Martínez", carrera: "Arquitectura") {
        estudiante {
            id  
            nombre
            apellido
            carrera
        }
    }
}
"""

crearPlanta = """
mutation {
    crearPlanta(
        nombre_comun: "Rosa",
        especie: "Rosaceae",
        edad: 20,
        altura: 15.0,
        frutos: true 
    ) {
        planta {
            id  
            nombre_comun
            especie
            edad
            altura
            frutos
        }
    }
}
"""
print("RESPUESTA")
response_mutation = requests.post(url, json={"query": crearPlanta})
print(response_mutation.text)


# print("RESPUESTA")
# response_mutation = requests.post(url, json={"query": crearEstudiante1})
# print(response_mutation.text)
# response_mutation = requests.post(url, json={"query": crearEstudiante2})
# print(response_mutation.text)
# response_mutation = requests.post(url, json={"query": crearEstudiante3})
# print(response_mutation.text)

# query_arquitectura = """
# {
#     estudiantesPorCarrera(carrera: "Arquitectura") {
#         id
#         nombre
#         apellido
#         carrera
#     }
# }
# """
# response_arquitectura = requests.post(url, json={"query": query_arquitectura})
# print(response_arquitectura.text)


# query_eliminar = """
# mutation {
#         deleteEstudiante(id: 3) {
#             estudiante{
#                 id
#                 nombre
#                 apellido
#                 carrera
#             }
#         }
#     }
# """
# response_mutation = requests.post(url, json={'query': query_eliminar})
# print(response_mutation.text)
