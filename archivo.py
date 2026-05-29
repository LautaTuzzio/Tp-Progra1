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

def iniciarSesion(usuario, clientes):
    """Funcion para iniciar sesion
    Recibe el cuit y la lista de clientes
    Retorna el cliente encontrado
    """
    final = ""
    usuario = str(usuario)
    for i, cliente in enumerate(clientes):

        if cliente[0] == usuario:
            print("Usuario encontrado")
            final = cliente[i]
            break
    if final == "":
        return None
    return final

#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    #-------------------------------------------------
    # Inicialización de variables
    #----------------------------------------------------------------------------------------------
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
            print("[1] Opción 1")
            print("[2] Opción 2")
            print("[3] Opción 3")
            print("[4] Opción 4")
            print("[5] Opción 5")
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

        if opcion == "0": # Opción salir del programa
            print("Adiós")
            exit() # También puede ser sys.exit() para lo cual hay que importar el módulo sys

        elif opcion == "1":   # Opción 1
            cliente = iniciarSesion(usuario, clientes)
            print(f"Cliente: {cliente}")
        elif opcion == "2":   # Opción 2
            ...
        elif opcion == "3":   # Opción 3
            ...
        elif opcion == "4":   # Opción 4
            ...
        elif opcion == "5":   # Opción 5
            ...
        elif opcion == "6":   # Opción 6
            ...
        elif opcion == "7":   # Opción 7
            ...
        elif opcion == "8":   # Opción 8
            ...
        elif opcion == "9":   # Opción 9
            ...
        elif opcion == "10":   # Opción 10
            ...

        input("\nPresione ENTER para volver al menú.")
        print("\n\n")


# Punto de entrada al programa
main()