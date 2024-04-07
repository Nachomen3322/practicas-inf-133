from zeep import Client

client = Client("http://localhost:8000")

opcion = 0
while True:
    opcion = int(input(
        "Ingrese una opcion. 1) Sumar 2) Restar 3) Multiplicar 4) Dividir 5) Salir del programa: "
    ))
    if opcion == 5:
        print("Saliendo del programa")
        break
    a, b = map(
        int, input("Ingrese 2 datos de la siguiente manera, ejemplo: 4 2: ").split(" ")
    )
    if opcion == 1:
        print(client.service.SumaDosNumeros(a, b))
    elif opcion == 2:
        print(client.service.RestarDosNumeros(a, b))
    elif opcion == 3:
        print(client.service.MultiplicarDosNumeros(a, b))
    elif opcion == 4:
        if b!=0:
            print(client.service.DivideDosNumeros(a, b))
        else:
            print("Nose puede dividir entre 0")
    else:
        print("Valor ingresado invalido")
