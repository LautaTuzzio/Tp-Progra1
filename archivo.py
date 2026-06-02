"""
-----------------------------------------------------------------------------------------------
Título: TP Progra
Fecha: 29/5/2026
Autor: Grupo 3

Descripción: Un sistema de gestion bancaria

Pendientes: ---
-----------------------------------------------------------------------------------------------
"""

#----------------------------------------------------------------------------------------------
# MÓDULOS
#----------------------------------------------------------------------------------------------
...


#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------
def pedirNumero(msj,msE,msE2,minimo,maximo,convertir = 1):
    """Función de pedir numero
    Parámetros obligatorios:
    msj = Mensaje de pedido de dato (recomendamos recordar al usuario mínimos
    y máximos)
    msjE = Mensaje de error para valores no numéricos
    msjE2 = Mensaje de error para valores fuera de rango
    minimo = valor minimo permitido
    maximo = valor máximo permitido
       
    Parámetros optativos:
    convertir = formato de conversión: 1 para entero, 0 para flotante.
    convierte a entero por defecto. Poner 0 si se quiere un flotante
    """
    
    caracteres_validos = "0123456789.-"
    flag = True
    
    while flag:
        valor = input(msj)
        if any(c not in caracteres_validos for c in valor):
            # si el valor presenta elementos no correspondientes a números
            print(msE)
        elif valor.count('.') > 1 or  valor.count('-') > 1:
            # si el valor presenta  más de un menos o un punto
            print(msE)
        elif (valor.startswith('.') or valor.endswith('.')) or(valor.count('-') == 1 and not valor.startswith('-')):
            # si el valor empieza o termina con punto (debe ir entre medio) o
            # si el valor tiene un menos entre medio (debe empezar obligatoriamente con -)
            print(msE)
        elif len(valor) == 0:
            print(msE) #ingresamos enter x accidente
        else:
            # se valida se encuentre entre el rango
            if float(valor) < minimo or float(valor) > maximo:
                print(f"{msE2} minimo: {minimo} máximo {maximo}")
            else:
                flag = False
    
    # se convierte a flotante por defecto
    numero = float(valor)
    # si se parametriza como entero
    if convertir == 1:
        numero = int(numero)
    # retorno de numero convertido
    return numero

def validarCuit():
    """Funcion para pedir cuit utilizando pedirNumero
    No requiere parámetros y retorna el cuit como un str
    """
    parte1 = pedirNumero("""Ingresa primera parte cuit (2 primeros numeros): """,
                         """El valor no es entero""",
                         """Valor fuera de rango""",
                         10,99,convertir = 1)
    parte2 = pedirNumero("""Ingresa primera parte cuit (DNI): """,
                     """El valor no es entero""",
                     """Valor fuera de rango""",
                     1_000_000,100_000_000,convertir = 1)
    
    parte3 = pedirNumero("""Ingresa última cifra: """,
                     """El valor no es entero""",
                     """Valor fuera de rango""",
                     0,9,convertir = 1)
    valor = f"{parte1}-{parte2}-{parte3}"

    return valor

def iniciarSesion(clientes):
    """
    Permite iniciar sesión.
    Retorna la posición del cliente o None.
    """

    cuit = validarCuit()

    for i, cliente in enumerate(clientes):
        if cliente[0] == cuit:

            clave = pedirNumero(
                "Ingresa contraseña: ",
                "La contraseña debe ser numérica",
                "Contraseña fuera de rango",
                1000,
                9999
            )

            if cliente[2] == clave:
                print("Loggeo Exitoso")
                print(f"Bienvenido {cliente[1]} id {i}!")
                return i

            print("Vuelva intentar")
            print("Usuario Inexistente")
            return None

    print("Usuario Inexistente")
    return None

def cerrarSesion():
    """
    Cierra la sesión actual.
    """
    print("Sesión cerrada")
    return None

def verSaldo(posicion, clientes):
    """
    Permite consultar saldos.
    """

    print(f"Hola, {clientes[posicion][1]}, ¿Qué saldo deseas ver?")
    print("[1] Cuenta Sueldo")
    print("[2] Cuenta Corriente")
    print("[3] Dólares")

    opcion = input("Opción: ")

    if opcion == "1":
        print(f"Saldo en Cuenta Sueldo: ${clientes[posicion][4]:.2f}")

    elif opcion == "2":
        print(f"Saldo en Cuenta Corriente: ${clientes[posicion][5]:.2f}")

    elif opcion == "3":
        print(f"Saldo en Cuenta Dólares: USD ${clientes[posicion][6]:.2f}")

    else:
        print("Opción inválida")

def depositar(posicion, clientes):
    """
    Deposita dinero en cuenta sueldo.
    """

    while True:

        monto = pedirNumero(
            "¿Cuánto deposita?: ",
            "Importe inválido",
            "Valor fuera de rango",
            1000,
            1_000_000
        )

        if monto % 1000 != 0:
            print("Importe inválido")
        else:
            break

    clientes[posicion][4] += monto

    print(f"Nuevo saldo: ${clientes[posicion][4]}")

def retirar(posicion, clientes):
    """
    Retira dinero de la cuenta sueldo.
    """

    saldo = clientes[posicion][4]

    if saldo < 1000:
        print(f"No se puede retirar dinero. Saldo en cuenta: {saldo}")
        return

    while True:

        monto = pedirNumero(
            f"¿Cuánto retira? minimo $1000 y máximo {saldo}: ",
            "Importe inválido",
            "Valor fuera de rango",
            1000,
            saldo
        )

        if monto % 1000 != 0:
            print("Importe inválido")
        else:
            break

    clientes[posicion][4] -= monto

    print(f"Nuevo saldo: ${clientes[posicion][4]}")

  
#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    #-------------------------------------------------
    # Inicialización de variables
    #----------------------------------------------------------------------------------------------
    usuario = None
    #cuit,nombre,pwrd,sueldo,cuenta_sueldo,cuenta_corriente, plazo_fijo
    clientes = [
    ["27-11222333-0", "Maria", 1234, 1_500_000, 0, 0, 1_000],
    ["23-22333444-9", "Luis", 2345, 1_800_000, 15_000, -15_000, 1_000],
    ["20-44252999-8", "Jose", 9685, 2_000_000, 10_000, -1_000, 1_000],
    ["29-55667788-2", "Ana", 4521, 1_600_000, 5_000, 500, 500],
    ["21-33445566-3", "Carlos", 8765, 1_700_000, 20_000, -500, 700],
    ["25-99887766-5", "Sofia", 5678, 1_850_000, 12_000, -2_000, 900],
    ["30-11224455-7", "Diego", 9012, 2_100_000, 30_000, -5_000, 1_200],
    ["22-88997766-8", "Valentina", 3141, 1_450_000, 8_000, 1_500, 300],
    ["28-77665544-1", "Facundo", 2222, 1_750_000, 25_000, -10_000, 650],
    ["24-44556677-2", "Camila", 7890, 1_950_000, 18_000, -3_000, 800],
    ["26-11223344-6", "Martín", 5432, 2_250_000, 40_000, -12_000, 1_500],
    ["32-99887766-9", "Agustina", 6789, 1_400_000, 6_000, 2_000, 250],
    ["31-77665544-3", "Fernando", 1357, 2_000_000, 35_000, -8_000, 1_100],
    ["33-88997766-4", "Julieta", 2468, 1_650_000, 14_000, -1_500, 550],
    ["35-55443322-5", "Leandro", 3698, 2_300_000, 50_000, -20_000, 1_800]
    ]
    usuario = validarCuit()
    #-------------------------------------------------
    # Bloque de menú
    #----------------------------------------------------------------------------------------------
    while True:
        while True:
            opciones = 10
            print()
            print("---------------------------")
            print("MENÚ DEL DIGITAL BANK      ")
            print("---------------------------")
            print("[1] Opción 1, Iniciar sesión.")
            print("[2] Opcion 2, Consultar saldo.")
            print("[3] Opción 3, Depositar")
            print("[4] Opción 4, Retirar")
            print("[5] Opción 51")
            print("[6] Opción 6")
            print("[7] Opción 7")
            print("[8] Opción 8")
            print("[9] Opción 9")
            print("[10] Opción 10")
            print("---------------------------")
            print("[0] Salir del programa")
            print("---------------------------")
            print()
            
            opcion = input("Seleccione una opción: ")
            if opcion in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                break
            else:
                input("Opción inválida. Presione ENTER para volver a seleccionar.")
        print()

        if opcion == "0":
            print("Adiós")
            exit()

        elif opcion == "1":   # Iniciar sesión
            if usuario is None:
                usuario = iniciarSesion(clientes)
            else:
                print("Ya hay una sesión iniciada")

        elif opcion == "2":   # Ver saldo
            if usuario is None:
                print("Debe iniciar sesión primero")
            else:
                verSaldo(usuario, clientes)

        elif opcion == "3":   # Depositar
            if usuario is None:
                print("Debe iniciar sesión primero")
            else:
                depositar(usuario, clientes)

        elif opcion == "4":   # Retirar
            if usuario is None:
                print("Debe iniciar sesión primero")
            else:
                retirar(usuario, clientes)

        elif opcion == "5":   # Cerrar sesión
            if usuario is None:
                print("No hay una sesión iniciada")
            else:
                usuario = cerrarSesion()

        elif opcion == "6":
            print("Opción no implementada")

        elif opcion == "7":
            print("Opción no implementada")

        elif opcion == "8":
            print("Opción no implementada")

        elif opcion == "9":
            print("Opción no implementada")

        elif opcion == "10":
            print("Opción no implementada")
        
        input("\nPresione ENTER para volver al menú.")
        print("\n\n")


# Punto de entrada al programa
main()