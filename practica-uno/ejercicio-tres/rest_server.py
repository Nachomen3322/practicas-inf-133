from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

pacientes = [
    {
        "ci": 1,
        "nombre": "Pedro",
        "apellido": "Saraiche",
        "edad": 35,
        "genero": "Masculino",
        "diagnostico": "Diabetes",
        "doctor": "Pedro Perez",
    },
    {
        "ci": 2,
        "nombre": "Tyler",
        "apellido": "Joseph",
        "edad": 33,
        "genero": "Masculino",
        "diagnostico": "Hair loss",
        "doctor": "Josh Dun",
    },
]


class PacienteService:
    @staticmethod
    def buscar_por_ci(ci):
        return next((paciente for paciente in pacientes if paciente["ci"] == ci), None)

    @staticmethod
    def buscar_por_diagnostico(diagnostico):
        return [
            paciente for paciente in pacientes if paciente["diagnostico"] == diagnostico
        ]

    @staticmethod
    def buscar_por_doctor(doctor):
        return [paciente for paciente in pacientes if paciente["doctor"] == doctor]

    @staticmethod
    def add_paciente(data):
        pacientes.append(data)
        return pacientes

    @staticmethod
    def update_paciente(ci, data):
        paciente = PacienteService.buscar_por_ci(ci)
        if paciente:
            paciente.update(data)
            return pacientes
        else:
            return None

    @staticmethod
    def delete_paciente(ci):
        paciente = PacienteService.buscar_por_ci(ci)
        if paciente:
            pacientes.remove(paciente)
        return pacientes


class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))


class PacienteHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/pacientes/":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = PacienteService.buscar_por_diagnostico(
                    diagnostico
                )
                if pacientes_filtrados != []:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filtrados = PacienteService.buscar_por_doctor(doctor)
                if pacientes_filtrados != []:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])

            else:
                HTTPResponseHandler.handle_response(self, 200, pacientes)

        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente = PacienteService.buscar_por_ci(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])

        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/pacientes":
            data = HTTPResponseHandler.handle_reader(self)
            pacientes = PacienteService.add_paciente(data)
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = HTTPResponseHandler.handle_reader(self)
            pacientes = PacienteService.update_paciente(ci, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Paciente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            pacientes = PacienteService.delete_paciente(ci)

            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Paciente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )


def run(server_class=HTTPServer, handler_class=PacienteHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
