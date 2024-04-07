from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import (
    ObjectType,
    String,
    Int,
    List,
    Schema,
    Field,
    Mutation,
    Boolean,
    Float,
)


class Planta(ObjectType):
    id = Int()
    nombre_comun = String()
    especie = String()
    edad = Int()
    altura = Float()
    frutos = Boolean()


plantas = [
    Planta(
        id=1,
        nombre_comun="Cactus",
        especie="Cactaceae",
        edad=20,
        altura=120.0,
        frutos=True,
    ),
    Planta(
        id=2,
        nombre_comun="Girasol",
        especie="Helianthus",
        edad=12,
        altura=10.0,
        frutos=False,
    ),
]


class Query(ObjectType):
    plantas = List(Planta)
    planta_por_id = Field(Planta, id=Int())
    planta_por_especie = List(Planta, especie=String())
    plantas_con_frutos = List(Planta)

    def resolve_plantas(root, info):
        return plantas

    def resolve_plantas_por_id(root, info, id):
        for planta in plantas:
            if planta.id() == id:
                return planta
        return None

    def resolve_por_especie(root, info, especie):
        return [planta for planta in plantas if planta.especie == especie]

    def resolve_plantas_con_frutos(root, info):
        return [planta for planta in plantas if planta.frutos]


class CrearPlanta(Mutation):
    class Arguments:
        nombre_comun = String()
        especie = String()
        edad = Int()
        altura = Float()
        frutos = Boolean()

    planta = Field(Planta)

    def mutate(root, info, nombre_comun, especie, edad, altura, frutos):
        nueva_planta = Planta(
            id=len(plantas) + 1,
            nombre_comun=nombre_comun,
            especie=especie,
            edad=edad,
            altura=altura,
            frutos=frutos,
        )
        plantas.append(nueva_planta)

        return CrearPlanta(planta=nueva_planta)


# ELIMINAR PLANTA
class DeletePlanta(Mutation):
    class Arguments:
        id = Int()

    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None


class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    delete_planta = DeletePlanta.Field()


schema = Schema(query=Query, mutation=Mutations)


class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/plantas/"):
            id = int(self.path.split("/")[-1])
            planta = self.find_plant(id)
            data = self.read_data()
            if planta:
                planta.update(data)
                self.response_handler(200, [plantas])
            else:
                self.response_handler(404, {"Error": "Planta no encontrada"})
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
