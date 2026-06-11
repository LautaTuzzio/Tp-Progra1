"""
-----------------------------------------------------------------------------------------------
Título: TP Progra
Fecha: 9/6/2026
Autor: Grupo 3

Descripción: Un sistema de gestion bancaria

Pendientes: No hay mas pendientes vamaa
-----------------------------------------------------------------------------------------------
"""

#----------------------------------------------------------------------------------------------
# MÓDULOS
#----------------------------------------------------------------------------------------------
import random
import requests
import os

#----------------------------------------------------------------------------------------------
# CONSTANTES
#----------------------------------------------------------------------------------------------
CLAVE_OFICIAL = "f06500_15#%$"
COTIZACION_FALLBACK = 1000  # cotización de respaldo si la API no responde


#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------
def pedirNumero(msj, msE, msE2, minimo, maximo, convertir=1):
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
            print(msE)
        elif valor.count('.') > 1 or valor.count('-') > 1:
            print(msE)
        elif (valor.startswith('.') or valor.endswith('.')) or (valor.count('-') == 1 and not valor.startswith('-')):
            print(msE)
        elif len(valor) == 0:
            print(msE)
        else:
            if float(valor) < minimo or float(valor) > maximo:
                print(f"{msE2} minimo: {minimo} máximo {maximo}")
            else:
                flag = False
    
    numero = float(valor)
    if convertir == 1:
        numero = int(numero)
    return numero


def validarCuit():
    """Funcion para pedir cuit utilizando pedirNumero
    No requiere parámetros y retorna el cuit como un str
    """
    parte1 = pedirNumero(
        "Ingresa primera parte cuit (2 primeros numeros): ",
        "El valor no es entero",
        "Valor fuera de rango",
        10, 99, convertir=1
    )
    parte2 = pedirNumero(
        "Ingresa primera parte cuit (DNI): ",
        "El valor no es entero",
        "Valor fuera de rango",
        1_000_000, 100_000_000, convertir=1
    )
    parte3 = pedirNumero(
        "Ingresa última cifra: ",
        "El valor no es entero",
        "Valor fuera de rango",
        0, 9, convertir=1
    )
    valor = f"{parte1}-{parte2}-{parte3}"
    return valor


def obtenerCotizacionDolar():
    """Obtiene la cotización de compra y venta del dólar blue desde dolarapi.com.
    No requiere parámetros.
    Retorna una tupla (compra, venta) con los valores del dólar blue.
    Si la API no responde, retorna el valor de respaldo COTIZACION_FALLBACK para ambos.
    """
    try:
        respuesta = requests.get("https://dolarapi.com/v1/dolares/blue")
        if respuesta.status_code == 200:
            datos = respuesta.json()
            compra = 1500 #datos.get("compra", COTIZACION_FALLBACK)
            venta = 1460 #datos.get("venta", COTIZACION_FALLBACK)
            return compra, venta
        else:
            print(f"(API dolarapi no disponible, usando cotización de respaldo: ${COTIZACION_FALLBACK})")
            return COTIZACION_FALLBACK, COTIZACION_FALLBACK
    except Exception:
        print(f"(API dolarapi no disponible, usando cotización de respaldo: ${COTIZACION_FALLBACK})")
        return COTIZACION_FALLBACK, COTIZACION_FALLBACK


def iniciarSesion(clientes):
    """Permite iniciar sesión.
    Recibe como parámetro: matriz de clientes
    Retorna la posición del cliente o None.
    """
    cuit = validarCuit()

    for i, cliente in enumerate(clientes):
        if cliente[0] == cuit:
            clave = pedirNumero(
                "Ingresa contraseña: ",
                "La contraseña debe ser numérica",
                "Contraseña fuera de rango",
                1000, 9999
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
    """Cierra la sesión actual.
    No requiere parámetros.
    Retorna None.
    """
    print("Sesión cerrada")
    return None


def verSaldo(posicion, clientes):
    """Permite consultar saldos de las tres cuentas del cliente.
    Recibe como parámetro: posición dentro de la matriz, matriz de clientes
    Retorna: None
    """
    print(f"Hola, {clientes[posicion][1]}, ¿Qué saldo deseas ver?")
    print("[1] Cuenta Sueldo")
    print("[2] Cuenta Corriente")
    print("[3] Dólares")

    opcion = input("Opción: ")

    if opcion == "1":
        # CORRECCIÓN: índice 4 es cuenta_sueldo (índice 3 es el salario del empleador)
        print(f"Saldo en Cuenta Sueldo: ${clientes[posicion][4]:.2f}")
    elif opcion == "2":
        # CORRECCIÓN: índice 5 es cuenta_corriente
        print(f"Saldo en Cuenta Corriente: ${clientes[posicion][5]:.2f}")
    elif opcion == "3":
        # CORRECCIÓN: índice 6 es cuenta_dolares
        print(f"Saldo en Cuenta Dólares: USD ${clientes[posicion][6]:.2f}")
    else:
        print("Opción inválida")


def depositar(posicion, clientes):
    """Deposita dinero en la cuenta sueldo del cliente.
    Recibe como parámetro: posición dentro de la matriz, matriz de clientes
    Retorna: None (modifica la matriz en el lugar)
    """
    while True:
        monto = pedirNumero(
            "¿Cuánto deposita? (mínimo 1.000 máximo 1.000.000 y múltiplo de 1000): ",
            "Importe inválido",
            "Valor fuera de rango",
            1000, 1_000_000
        )
        if monto % 1000 != 0:
            print("Importe inválido")
        else:
            break

    # CORRECCIÓN: índice 4 es cuenta_sueldo
    clientes[posicion][4] += monto
    print(f"Nuevo saldo: ${clientes[posicion][4]}")


def retirar(posicion, clientes):
    """Retira dinero de la cuenta sueldo del cliente.
    Recibe como parámetro: posición dentro de la matriz, matriz de clientes
    Retorna: None (modifica la matriz en el lugar)
    """
    # CORRECCIÓN: índice 4 es cuenta_sueldo
    saldo = clientes[posicion][4]

    if saldo < 1000:
        print(f"No se puede retirar dinero. Saldo en cuenta: {saldo}")
        return

    while True:
        monto = pedirNumero(
            f"¿Cuánto retira? minimo $1000 y máximo {saldo}: ",
            "Importe inválido",
            "Valor fuera de rango",
            1000, saldo
        )
        if monto % 1000 != 0:
            print("Importe inválido")
        else:
            break

    clientes[posicion][4] -= monto
    print(f"Nuevo saldo: ${clientes[posicion][4]}")


def comprarConTarjeta(posicion, clientes):
    """Permite al cliente realizar una compra con tarjeta de crédito.
    El límite de crédito es de 2 sueldos menos la deuda actual.
    Recibe como parámetro: posición dentro de la matriz, matriz de clientes
    Retorna: matriz de clientes actualizada
    """
    sueldo = clientes[posicion][3]
    deuda_actual = clientes[posicion][5]  # cuenta corriente (negativo = deuda)
    limite_total = sueldo * 2
    disponible = limite_total + deuda_actual  # deuda_actual es negativo, entonces resta

    if disponible <= 0:
        print(f"No se puede realizar compra. Disponible: ${disponible:.1f}")
        return clientes

    monto = pedirNumero(
        f"Valor de la compra con tarjeta minimo 0 (cancelar) y máximo {disponible}: ",
        "Importe inválido",
        "Valor fuera de rango",
        0, disponible, convertir=0
    )

    if monto == 0:
        print("Compra cancelada")
        return clientes

    clientes[posicion][5] -= monto
    print("Compra exitosa")
    print(f"Nuevo saldo cuenta corriente: ${clientes[posicion][5]:.1f}")
    return clientes


def pagarTarjeta(posicion, clientes):
    """Permite al cliente pagar su deuda de tarjeta desde la cuenta sueldo.
    Recibe como parámetro: posición dentro de la matriz, matriz de clientes
    Retorna: matriz de clientes actualizada
    """
    saldo_sueldo = clientes[posicion][4]
    deuda = clientes[posicion][5]  # negativo si hay deuda

    if saldo_sueldo < 1000:
        print(f"No se puede realizar pago. Disponible: {saldo_sueldo} pago mínimo $1000")
        return clientes

    if deuda >= 0:
        print("No tenés deuda en cuenta corriente.")
        return clientes

    monto = pedirNumero(
        f"Pago mínimo $1000 Disponible: ${saldo_sueldo:.1f} a pagar:${deuda:.1f} Ud. Abona: ",
        "Importe inválido",
        "Valor fuera de rango",
        1000, saldo_sueldo, convertir=0
    )

    clientes[posicion][5] += monto
    clientes[posicion][4] -= monto
    print("Pago exitoso")
    print(f"Nuevo saldo cuenta corriente: ${clientes[posicion][5]:.1f}")
    print(f"Nuevo saldo cuenta sueldo: ${clientes[posicion][4]:.1f}")
    return clientes


def comprarDolares(posicion, clientes):
    """Permite al cliente comprar dólares con el saldo de su cuenta sueldo.
    Cotización obtenida en tiempo real desde dolarapi.com (precio de venta del banco).
    Recibe como parámetro: posición dentro de la matriz, matriz de clientes
    Retorna: matriz de clientes actualizada
    """
    saldo_sueldo = clientes[posicion][4]

    if saldo_sueldo < 1000:
        print(f"No se puede realizar compra. Disponible: {saldo_sueldo} compra mínima $1000")
        return clientes

    _, cotizacion_venta = obtenerCotizacionDolar()
    print(f"Cotización dólar blue (venta): ${cotizacion_venta:.2f}")

    monto_pesos = pedirNumero(
        f"Mínima compra $1000 Disponible: ${saldo_sueldo:.1f} Ingrese valor a comprar (como pesos): ",
        "Importe inválido",
        "Valor fuera de rango",
        1000, saldo_sueldo, convertir=0
    )

    dolares_comprados = monto_pesos / cotizacion_venta
    clientes[posicion][6] += dolares_comprados
    clientes[posicion][4] -= monto_pesos

    print("Compra de dólares exitosa")
    print(f"Nuevo saldo cuenta dólares: ${clientes[posicion][6]:.2f}")
    print(f"Nuevo saldo cuenta sueldo: ${clientes[posicion][4]:.1f}")
    return clientes


def venderDolares(posicion, clientes):
    """Permite al cliente vender dólares y acreditar pesos en su cuenta sueldo.
    Se requiere un mínimo de 100 USD para poder vender.
    Cotización obtenida en tiempo real desde dolarapi.com (precio de compra del banco).
    Recibe como parámetro: posición dentro de la matriz, matriz de clientes
    Retorna: matriz de clientes actualizada
    """
    saldo_dolares = clientes[posicion][6]

    if saldo_dolares < 100:
        print(f"No se puede realizar venta. Disponible: {saldo_dolares:.1f} venta mínima usd $100")
        return clientes

    cotizacion_compra, _ = obtenerCotizacionDolar()
    print(f"Cotización dólar blue (compra): ${cotizacion_compra:.2f}")

    monto_dolares = pedirNumero(
        f"Mínima venta usd $100 Disponible: ${saldo_dolares:.1f} Ingrese valor a vender (como dólares): ",
        "Importe inválido",
        "Valor fuera de rango",
        100, saldo_dolares, convertir=0
    )

    pesos_recibidos = monto_dolares * cotizacion_compra
    clientes[posicion][6] -= monto_dolares
    clientes[posicion][4] += pesos_recibidos

    print("Venta de dólares exitosa")
    print(f"Nuevo saldo cuenta dólares: ${clientes[posicion][6]:.2f}")
    print(f"Nuevo saldo cuenta sueldo: ${clientes[posicion][4]:.1f}")
    return clientes


def cambiarClave(posicion, clientes):
    """Permite al cliente cambiar su contraseña validando la clave anterior.
    Recibe como parámetro: posición dentro de la matriz, matriz de clientes
    Retorna: matriz de clientes actualizada
    """
    clave_ingresada = pedirNumero(
        "Ingresa tu clave anterior: ",
        "Clave no numérica",
        "Valor fuera de rango",
        1000, 9999
    )

    if clave_ingresada != clientes[posicion][2]:
        print("Clave inválida")
        return clientes

    nueva_clave = pedirNumero(
        "Ingresa tu nueva clave: ",
        "Valor no numérico",
        "Valor fuera de rango",
        1000, 9999
    )

    clientes[posicion][2] = nueva_clave
    print("Clave cambiada exitosamente")
    return clientes


def transferir(posicion, clientes):
    """Permite al cliente transferir dinero desde su cuenta sueldo a otro cliente.
    Valida que el CUIT destinatario exista y que haya saldo suficiente.
    Solicita confirmación antes de ejecutar la transferencia.
    Recibe como parámetro: posición dentro de la matriz, matriz de clientes
    Retorna: matriz de clientes actualizada
    """
    saldo = clientes[posicion][4]

    print("Solo puedes transferir de tu cuenta sueldo...")

    if saldo < 1000:
        print(f"Saldo insuficiente para transferencia: ${saldo}")
        return clientes

    # Buscar destinatario por CUIT
    while True:
        cuit_destino = validarCuit()

        if cuit_destino == clientes[posicion][0]:
            print("No puedes transferirte a vos mismo.")
            continue

        posicion_destino = None
        for i, cliente in enumerate(clientes):
            if cliente[0] == cuit_destino:
                posicion_destino = i
                break

        if posicion_destino is None:
            print(f"Cuit {cuit_destino} no encontrado... vuelve a intentar")
        else:
            break

    nombre_destino = clientes[posicion_destino][1]
    print(f"Cliente beneficiario cuit {cuit_destino} nombre: {nombre_destino}")

    monto = pedirNumero(
        f"¿Cuánto transferirás? minimo $1000 y máximo {saldo}: ",
        "Importe inválido",
        "Valor fuera de rango",
        1000, saldo, convertir=0
    )

    confirmacion = input(f"Se transferirá ${monto:.1f} a cuit {cuit_destino} nombre: {nombre_destino} confirmar? [S] [N] ")

    if confirmacion.upper() != "S":
        print("Transferencia cancelada.")
        return clientes

    clientes[posicion][4] -= monto
    clientes[posicion_destino][4] += monto

    print(f"Transferencia realizada, tu nuevo saldo es ${clientes[posicion][4]:.0f}")
    return clientes


def verificarClaveOficial():
    """Solicita y verifica la clave del oficial de cuentas.
    No requiere parámetros.
    Retorna True si la clave es correcta, False en caso contrario.
    """
    clave = input("Ingresa clave de seguridad: ")
    if clave == CLAVE_OFICIAL:
        return True
    print("Clave inválida")
    return False


def informar(clientes):
    """Muestra el estado actual de todas las cuentas de todos los clientes.
    Requiere autenticación de oficial de cuentas.
    Recibe como parámetro: matriz de clientes
    Retorna: None
    """
    if not verificarClaveOficial():
        return

    print("Mostrando clientes…")
    for cliente in clientes:
        print(f"Cuit:{cliente[0]} Nombre:{cliente[1]}")
        print(f"      Cuenta sueldo ${cliente[4]}")
        print(f"      Cuenta corriente ${cliente[5]}")
        print(f"      Cuenta en dólares usd${cliente[6]}")
        print()


def pagarSueldos(clientes):
    """Acredita el sueldo registrado a la cuenta sueldo de cada cliente.
    El valor resultante es la suma del saldo anterior más el sueldo.
    Requiere autenticación de oficial de cuentas.
    Recibe como parámetro: matriz de clientes
    Retorna: matriz de clientes actualizada
    """
    if not verificarClaveOficial():
        return clientes

    for cliente in clientes:
        cliente[4] += cliente[3]

    print("Sueldos pagados")
    for cliente in clientes:
        print(f"Cuit:{cliente[0]} Nombre:{cliente[1]}")
        print(f"      Cuenta sueldo ${cliente[4]}")
        print(f"      Cuenta corriente ${cliente[5]}")
        print(f"      Cuenta en dólares usd${cliente[6]}")

    return clientes


def crearUsuario(clientes):
    """Permite al oficial de cuentas crear un nuevo cliente en el sistema.
    Valida que el CUIT no exista previamente.
    La clave temporal es un número aleatorio entre 1000 y 9999.
    Las cuentas se inicializan en $0.
    Requiere autenticación de oficial de cuentas.
    Recibe como parámetro: matriz de clientes
    Retorna: matriz de clientes actualizada
    """
    if not verificarClaveOficial():
        return clientes

    print("Creando un nuevo cliente")

    # Validar CUIT único
    while True:
        cuit_nuevo = validarCuit()
        existe = False
        for cliente in clientes:
            if cliente[0] == cuit_nuevo:
                print(f"Cuit existente... vuelva a intentar")
                print(f"Cuit:{cliente[0]} Nombre:{cliente[1]}")
                existe = True
                break
        if not existe:
            break

    nombre = input("Ingrese nombre del nuevo cliente: ").capitalize()
    clave_temporal = random.randint(1000, 9999)
    print(f"Clave temporal {clave_temporal}")

    sueldo = pedirNumero(
        "Ingrese sueldo: ",
        "Importe inválido",
        "Valor fuera de rango",
        1, 100_000_000, convertir=0
    )

    nuevo_cliente = [cuit_nuevo, nombre, clave_temporal, sueldo, 0, 0, 0]
    clientes.append(nuevo_cliente)

    print("Cliente creado con éxito")
    print(nuevo_cliente)
    print(f"Cuit:{cuit_nuevo} Nombre:{nombre}")
    print(f"      Cuenta sueldo $0")
    print(f"      Cuenta corriente $0")
    print(f"      Cuenta en dólares usd$0")

    return clientes


#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    #-------------------------------------------------
    # Inicialización de variables
    #-------------------------------------------------
    usuario = None
    # cuit, nombre, pwrd, sueldo, cuenta_sueldo, cuenta_corriente, cuenta_dolares
    clientes = [
        ["27-11222333-0", "Maria",     1234, 1_500_000, 0,      0,       1_000],
        ["23-22333444-9", "Luis",      2345, 1_800_000, 15_000, -15_000, 1_000],
        ["20-44252999-8", "Jose",      9685, 2_000_000, 10_000, -1_000,  1_000],
        ["29-55667788-2", "Ana",       4521, 1_600_000, 5_000,  500,     500],
        ["21-33445566-3", "Carlos",    8765, 1_700_000, 20_000, -500,    700],
        ["25-99887766-5", "Sofia",     5678, 1_850_000, 12_000, -2_000,  900],
        ["30-11224455-7", "Diego",     9012, 2_100_000, 30_000, -5_000,  1_200],
        ["22-88997766-8", "Valentina", 3141, 1_450_000, 8_000,  1_500,   300],
        ["28-77665544-1", "Facundo",   2222, 1_750_000, 25_000, -10_000, 650],
        ["24-44556677-2", "Camila",    7890, 1_950_000, 18_000, -3_000,  800],
        ["26-11223344-6", "Martín",    5432, 2_250_000, 40_000, -12_000, 1_500],
        ["32-99887766-9", "Agustina",  6789, 1_400_000, 6_000,  2_000,   250],
        ["31-77665544-3", "Fernando",  1357, 2_000_000, 35_000, -8_000,  1_100],
        ["33-88997766-4", "Julieta",   2468, 1_650_000, 14_000, -1_500,  550],
        ["35-55443322-5", "Leandro",   3698, 2_300_000, 50_000, -20_000, 1_800],
    ]

    #-------------------------------------------------
    # Bloque de menú
    #-------------------------------------------------
    while True:
        while True:
            opciones = 14
            print()
            print("---------------------------")
            print("MENÚ DEL DIGITAL BANK      ")
            print("---------------------------")
            print("[1]  Iniciar Sesión")
            print("[2]  Ver Saldo")
            print("[3]  Depositar Dinero")
            print("[4]  Retirar Dinero")
            print("[5]  Compra Tarjeta")
            print("[6]  Pagar Tarjeta")
            print("[7]  Comprar Dólares")
            print("[8]  Vender Dólares")
            print("[9]  Cambiar contraseña")
            print("[10] Transferir")
            print("[11] Cerrar Sesión")
            print("---------------------------")
            print("Soy oficial de cuentas")
            print("[12] Informe de clientes")
            print("[13] Pagar sueldos")
            print("[14] Crear usuario nuevo")
            print("---------------------------")
            print("[0]  Salir del programa")
            print("---------------------------")
            opcion = input("Seleccione una opción: ")
            if opcion in [str(i) for i in range(0, opciones + 1)]:
                break
            else:
                input("Opción inválida. Presione ENTER para volver a seleccionar.")
        print()

        if opcion == "0":
            print("Adiós")
            exit()

        elif opcion == "1":      # Iniciar sesión
            if usuario is None:
                usuario = iniciarSesion(clientes)
            else:
                print("Ya hay una sesión iniciada")

        elif opcion == "2":      # Ver saldo
            if usuario is None:
                print("Debe iniciar sesión primero")
            else:
                verSaldo(usuario, clientes)

        elif opcion == "3":      # Depositar
            if usuario is None:
                print("Debe iniciar sesión primero")
            else:
                depositar(usuario, clientes)

        elif opcion == "4":      # Retirar
            if usuario is None:
                print("Debe iniciar sesión primero")
            else:
                retirar(usuario, clientes)

        elif opcion == "5":      # Comprar con tarjeta
            if usuario is None:
                print("Debe iniciar sesión primero")
            else:
                clientes = comprarConTarjeta(usuario, clientes)

        elif opcion == "6":      # Pagar tarjeta
            if usuario is None:
                print("Debe iniciar sesión primero")
            else:
                clientes = pagarTarjeta(usuario, clientes)

        elif opcion == "7":      # Comprar dólares
            if usuario is None:
                print("Debe iniciar sesión primero")
            else:
                clientes = comprarDolares(usuario, clientes)

        elif opcion == "8":      # Vender dólares
            if usuario is None:
                print("Debe iniciar sesión primero")
            else:
                clientes = venderDolares(usuario, clientes)

        elif opcion == "9":      # Cambiar contraseña
            if usuario is None:
                print("Primero debes iniciar sesión")
            else:
                clientes = cambiarClave(usuario, clientes)

        elif opcion == "10":     # Transferir
            if usuario is None:
                print("Primero debes iniciar sesión")
            else:
                clientes = transferir(usuario, clientes)

        elif opcion == "11":     # Cerrar sesión
            if usuario is None:
                print("No hay una sesión iniciada")
            else:
                usuario = cerrarSesion()

        elif opcion == "12":     # Informe de clientes (oficial)
            informar(clientes)

        elif opcion == "13":     # Pagar sueldos (oficial)
            clientes = pagarSueldos(clientes)

        elif opcion == "14":     # Crear usuario nuevo (oficial)
            clientes = crearUsuario(clientes)

        input("\nPresione ENTER para volver al menú.")
        os.system("cls")


# Punto de entrada al programa
main()
