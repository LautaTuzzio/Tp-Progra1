def depositar_saldo(saldo_actual, monto_deposito):
    float(input(monto_deposito))
    if monto_deposito <= 0:
        print("El monto a depositar debe ser mayor a 0") 

    nuevo_saldo = saldo_actual + monto_deposito
    return nuevo_saldo
depositar_saldo