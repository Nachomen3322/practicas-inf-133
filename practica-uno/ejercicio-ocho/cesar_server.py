from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs


class MessageHandler:
    def __init__(self):
        self.messages = [
            {
                "id": 1,
                "contenido": "hola",
                "encriptado": "krod",
            },
            {
                "id": 2,
                "contenido": "pepe",
                "encriptado": "shsh",
            },
        ]

    def crear_mensaje(self, contenido):
        encriptado = self.encriptar_mensaje(contenido)
        mensaje = {
            "id": len(self.messages) + 1,
            "contenido": contenido,
            "encriptado": encriptado,
        }
        self.messages.append(mensaje)
        return mensaje

    def encriptar_mensaje(self, contenido):
        encriptado = ""
        for char in contenido:
            if char.isalpha():
                movido = chr((ord(char) - ord("a") + 3) % 26 + ord("a"))
                encriptado += movido
            else:
                encriptado += char
        return encriptado

    def listar_mensajes(self):
        return self.messages

    def obtener_por_id(self, id):
        for mensaje in self.messages:
            if mensaje["id"] == id:
                return mensaje
        return None

    def actualizar_mensaje(self, id, contenido):
        mensaje = self.obtener_por_id(id)
        if mensaje:
            mensaje["contenido"] = contenido
            mensaje["encriptado"] = self.encriptar_mensaje(contenido)
            return mensaje
        return None

    def eliminar_mensaje(self, id):
        mensaje = self.obtener_por_id(id)
        if mensaje:
            self.messages.remove(mensaje)
            return True
        else:
            return False


class HTTPResponseHandler:
    @staticmethod
    def set_response(
        handler, status_code=200, content_type="application/json", body=None
    ):
        handler.send_response(status_code)
        handler.send_header("Content-type", content_type)
        handler.end_headers()

        if body:
            handler.wfile.write(json.dumps(body).encode())


class RESTRequestHandler(BaseHTTPRequestHandler):
    message_handler = MessageHandler()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        if path == "/mensajes":
            mensajes = self.message_handler.listar_mensajes()
            HTTPResponseHandler.set_response(self, body=mensajes)
        elif path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensaje = self.message_handler.obtener_por_id(id)
            if mensaje:
                HTTPResponseHandler.set_response(self, body=mensaje)
            else:
                HTTPResponseHandler.set_response(
                    self, status_code=404, body={"Error": "Mensaje no encontrado"}
                )
        else:
            HTTPResponseHandler.set_response(
                self, status_code=404, body={"Error": "Ruta no existente"}
            )

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        contenido = data.get("contenido")
        if contenido:
            mensaje = self.message_handler.crear_mensaje(contenido)
            HTTPResponseHandler.set_response(self, status_code=201, body=mensaje)
        else:
            HTTPResponseHandler.set_response(
                self, status_code=400, body={"Error": "No se encontro contenido"}
            )

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        id = int(parsed_path.path.split("/")[-1])
        content_length = int(self.headers["Content-Length"])
        put_data = self.rfile.read(content_length)
        data = json.loads(put_data.decode())
        nuevo_contenido = data.get("contenido")
        if nuevo_contenido:
            mensaje_actualizado = self.message_handler.actualizar_mensaje(
                id, nuevo_contenido
            )
            if mensaje_actualizado:
                HTTPResponseHandler.set_response(self, body=mensaje_actualizado)
            else:
                HTTPResponseHandler.set_response(
                    self, status_code=404, body={"Error": "Mensaje no encontrado"}
                )
        else:
            HTTPResponseHandler.set_response(
                self, status_code=400, body={"Error": "No se encontro contenido"}
            )

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        id = int(parsed_path.path.split("/")[-1])
        if self.message_handler.eliminar_mensaje(id):
            HTTPResponseHandler.set_response(
                self, body={"Mensaje": "Mensaje Eliminado"}
            )
        else:
            HTTPResponseHandler.set_response(
                self, status_code=404, body={"Error": "Mensaje no encontrado"}
            )


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
