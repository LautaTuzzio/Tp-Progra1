capital = float(input("Ingrese el capital inicial: "))
tasa_anual = 15
dias = int(input("Ingrese el plazo en días: "))
interes = capital * (tasa_anual / 100) * (dias / 365)
monto_final = capital + interes
print(f"Interés ganado (15% anual): ${interes:.2f}")
print(f"Monto total al vencimiento: ${monto_final:.2f}")