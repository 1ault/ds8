"""Simulacion basica de un sistema de parqueo inteligente."""

import argparse
import math
import random
import time
from datetime import datetime


# Constantes del sistema
CAPACIDAD_MAXIMA = 20
TARIFA_POR_MINUTO = 0.05
DURACION_PREDETERMINADA = 120  # Dos minutos
INTERVALO_PREDETERMINADO = 5


# Estructuras de datos principales
autos_estacionados = []
horas_entrada = {}
historial_autos = {}
eventos_estacionamiento = []


def hora_actual():
    """Devuelve la hora actual en un formato facil de leer."""
    return datetime.now().strftime("%H:%M:%S")


def generar_placa():
    """Genera una placa que no este siendo utilizada."""
    while True:
        letras = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2))
        numeros = random.randint(1000, 9999)
        placa = f"{letras}{numeros}"
        if placa not in autos_estacionados:
            return placa


def guardar_evento(placa, tipo, tarifa):
    """Guarda el evento como tupla y lo agrega al historial de la placa."""
    evento = (placa, f"{tipo}: {hora_actual()}", tarifa)
    eventos_estacionamiento.append(evento)

    if placa not in historial_autos:
        historial_autos[placa] = []
    historial_autos[placa].append(evento)


def registrar_entrada(placa):
    """Registra la entrada de un auto si existe espacio."""
    if len(autos_estacionados) >= CAPACIDAD_MAXIMA:
        print(f"  No puede entrar {placa}: el parqueo esta lleno.")
        return False

    autos_estacionados.append(placa)
    horas_entrada[placa] = time.time()
    guardar_evento(placa, "Entrada", 0.0)
    print(f"  ENTRO  {placa}")
    return True


def registrar_salida(placa):
    """Registra la salida y calcula la tarifa del auto."""
    if placa not in autos_estacionados:
        print(f"  No se encontro la placa {placa} dentro del parqueo.")
        return False

    segundos = time.time() - horas_entrada[placa]
    minutos = max(1, math.ceil(segundos / 60))
    tarifa = round(minutos * TARIFA_POR_MINUTO, 2)

    autos_estacionados.remove(placa)
    del horas_entrada[placa]
    guardar_evento(placa, "Salida", tarifa)
    print(f"  SALIO  {placa} | Tiempo cobrado: {minutos} min | Tarifa: ${tarifa:.2f}")
    return True


def porcentaje_ocupacion():
    return (len(autos_estacionados) / CAPACIDAD_MAXIMA) * 100


def estado_parqueo():
    """Clasifica el parqueo segun su porcentaje de ocupacion."""
    porcentaje = porcentaje_ocupacion()
    if porcentaje >= 100:
        return "LLENO"
    if porcentaje >= 50:
        return "MEDIO OCUPADO"
    return "DISPONIBLE"


def mostrar_estado():
    ocupados = len(autos_estacionados)
    libres = CAPACIDAD_MAXIMA - ocupados
    print("\n  --- Estado del parqueo ---")
    print(f"  Ocupados: {ocupados}/{CAPACIDAD_MAXIMA}")
    print(f"  Espacios libres: {libres}")
    print(f"  Porcentaje de ocupacion: {porcentaje_ocupacion():.1f}%")
    print(f"  Estado: {estado_parqueo()}")


def mostrar_autos():
    print("\n  Autos que se encuentran dentro:")
    if not autos_estacionados:
        print("  Ninguno")
        return
    for numero, placa in enumerate(autos_estacionados, start=1):
        print(f"  {numero}. {placa}")


def pedir_entero(mensaje, limite):
    """Solicita un entero valido dentro del limite indicado."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("El valor no puede ser negativo.")
            elif valor > limite:
                print(f"El valor maximo permitido en este momento es {limite}.")
            else:
                return valor
        except ValueError:
            print("Entrada invalida. Escriba un numero entero.")


def ejecutar_ciclo_automatico():
    espacios_libres = CAPACIDAD_MAXIMA - len(autos_estacionados)
    cantidad_entran = random.randint(0, min(4, espacios_libres))
    cantidad_salen = random.randint(0, min(3, len(autos_estacionados)))

    for _ in range(cantidad_salen):
        registrar_salida(random.choice(autos_estacionados))
    for _ in range(cantidad_entran):
        registrar_entrada(generar_placa())


def ejecutar_ciclo_manual():
    espacios_libres = CAPACIDAD_MAXIMA - len(autos_estacionados)
    cantidad_entran = pedir_entero(
        f"Cuantos autos entran? (0-{espacios_libres}): ", espacios_libres
    )
    for _ in range(cantidad_entran):
        registrar_entrada(generar_placa())

    cantidad_salen = pedir_entero(
        f"Cuantos autos salen? (0-{len(autos_estacionados)}): ",
        len(autos_estacionados),
    )
    salidas_realizadas = 0
    while salidas_realizadas < cantidad_salen:
        mostrar_autos()
        placa = input("Placa que sale (Enter = elegir al azar): ").strip().upper()
        if placa == "":
            placa = random.choice(autos_estacionados)
        if registrar_salida(placa):
            salidas_realizadas += 1


def mostrar_resumen():
    print("\n" + "=" * 50)
    print("SIMULACION FINALIZADA")
    mostrar_estado()
    mostrar_autos()
    print("\n  Historial de eventos por placa:")
    if not historial_autos:
        print("  No se registraron eventos.")
    for placa, eventos in historial_autos.items():
        print(f"\n  {placa}:")
        for evento in eventos:
            print(f"    {evento}")


def seleccionar_modo(modo_argumento):
    if modo_argumento:
        return modo_argumento

    while True:
        print("Seleccione el modo de simulacion:")
        print("1. Automatico (movimientos aleatorios)")
        print("2. Manual (el usuario indica las cantidades)")
        opcion = input("Opcion: ").strip()
        if opcion == "1":
            return "automatico"
        if opcion == "2":
            return "manual"
        print("Opcion invalida. Escriba 1 o 2.\n")


def simular(duracion, intervalo, modo):
    inicio = time.monotonic()
    ciclo = 1

    print("\n" + "=" * 50)
    print("SISTEMA DE PARQUEO INTELIGENTE")
    print(f"Capacidad maxima: {CAPACIDAD_MAXIMA} autos")
    print(f"Tarifa: ${TARIFA_POR_MINUTO:.2f} por minuto")
    print(f"Duracion: {duracion:g} segundos | Modo: {modo}")
    print("=" * 50)

    while time.monotonic() - inicio < duracion:
        restante = max(0, math.ceil(duracion - (time.monotonic() - inicio)))
        print(f"\nCICLO {ciclo} | Tiempo restante: {restante} segundos")

        if modo == "automatico":
            ejecutar_ciclo_automatico()
        else:
            ejecutar_ciclo_manual()

        mostrar_estado()
        mostrar_autos()
        ciclo += 1

        tiempo_restante = duracion - (time.monotonic() - inicio)
        if tiempo_restante > 0:
            time.sleep(min(intervalo, tiempo_restante))

    mostrar_resumen()


def leer_argumentos():
    parser = argparse.ArgumentParser(
        description="Simula durante dos minutos un parqueo inteligente."
    )
    parser.add_argument(
        "--modo", choices=["automatico", "manual"], help="Evita mostrar el menu inicial."
    )
    parser.add_argument(
        "--duracion",
        type=float,
        default=DURACION_PREDETERMINADA,
        help="Duracion en segundos (predeterminado: 120).",
    )
    parser.add_argument(
        "--intervalo",
        type=float,
        default=INTERVALO_PREDETERMINADO,
        help="Segundos entre ciclos (predeterminado: 5).",
    )
    parser.add_argument("--semilla", type=int, help="Semilla para repetir datos aleatorios.")
    argumentos = parser.parse_args()

    if argumentos.duracion <= 0 or argumentos.intervalo <= 0:
        parser.error("La duracion y el intervalo deben ser mayores que cero.")
    return argumentos


def main():
    argumentos = leer_argumentos()
    if argumentos.semilla is not None:
        random.seed(argumentos.semilla)

    modo = seleccionar_modo(argumentos.modo)
    try:
        simular(argumentos.duracion, argumentos.intervalo, modo)
    except KeyboardInterrupt:
        print("\n\nSimulacion detenida por el usuario.")
        mostrar_resumen()


if __name__ == "__main__":
    main()
