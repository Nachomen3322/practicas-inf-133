from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler


# Suma de dos numeros
def SumaDosNumeros(a, b):
    return a + b


# Resta de dos numeros
def RestarDosNumeros(a, b):
    return a - b


# Multiplicacion de dos numeros
def MultiplicarDosNumeros(a, b):
    return a * b


# Divicion de dos numeros
def DivideDosNumeros(a, b):
    return a//b

dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

dispatcher.register_function(
    "SumaDosNumeros",
    SumaDosNumeros,
    returns={"Suma": int},
    args={"a": int, "b": int},
)

dispatcher.register_function(
    "RestarDosNumeros",
    RestarDosNumeros,
    returns={"Resta": int},
    args={"a": int, "b": int},
)

dispatcher.register_function(
    "MultiplicarDosNumeros",
    MultiplicarDosNumeros,
    returns={"Multiplicar": int},
    args={"a": int, "b": int},
)

dispatcher.register_function(
    "DivideDosNumeros",
    DivideDosNumeros,
    returns={"Divide": int},
    args={"a": int, "b": int},
)

server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()
