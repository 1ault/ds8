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

SEGUNDOS_POR_MINUTO = 60
PORCENTAJE_TOTAL = 100.0
UMBRAL_PARQUEO_LLENO = 100.0  # Porcentaje a partir del cual se reporta LLENO
UMBRAL_PARQUEO_MEDIO = 50.0  # Porcentaje a partir del cual se reporta MEDIO OCUPADO
MAX_AUTOS_ENTRAN_POR_CICLO = 4  # Tope aleatorio de entradas por ciclo
MAX_AUTOS_SALEN_POR_CICLO = 3  # Tope aleatorio de salidas por ciclo
LONGITUD_LETRAS_PLACA = 2  # Letras de una placa, por ejemplo "AB1234"
PLACA_NUMERO_MINIMO = 1000
PLACA_NUMERO_MAXIMO = 9999
ANCHO_SEPARADOR = 50  # Ancho de las lineas de separacion


# Estructuras de datos principales
# Cada evento de estacionamiento es una tupla (placa, hora de entrada/salida, tarifa)
Evento = tuple[str, str, float]
HistorialPlaca = list[Evento]

autos_estacionados: list[str] = []
horas_entrada: dict[str, float] = {}
historial_autos: dict[str, HistorialPlaca] = {}
eventos_estacionamiento: list[Evento] = []


def obtener_hora_actual() -> str:
    """Devuelve la hora actual en un formato facil de leer."""
    return datetime.now().strftime("%H:%M:%S")


def generar_placa() -> str:
    """Genera una placa que no este siendo utilizada."""
    while True:
        letras = "".join(
            random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=LONGITUD_LETRAS_PLACA)
        )
        numeros = random.randint(PLACA_NUMERO_MINIMO, PLACA_NUMERO_MAXIMO)
        placa = f"{letras}{numeros}"
        if placa not in autos_estacionados:
            return placa


def guardar_evento(placa: str, tipo_evento: str, tarifa: float) -> None:
    """Guarda el evento como tupla y lo agrega al historial de la placa.

    Args:
        placa: Placa del auto, por ejemplo "AB1234".
        tipo_evento: "Entrada" o "Salida".
        tarifa: Monto cobrado. Es 0.0 cuando el evento es una entrada.

    La tupla guardada tiene la forma (placa, "Tipo: hora", tarifa),
    tal como pide el requisito 10 del examen.
    """
    evento = (placa, f"{tipo_evento}: {obtener_hora_actual()}", tarifa)
    eventos_estacionamiento.append(evento)

    if placa not in historial_autos:
        historial_autos[placa] = []
    historial_autos[placa].append(evento)


def registrar_entrada(placa: str) -> bool:
    """Registra la entrada de un auto si existe espacio.

    Args:
        placa: Placa del auto que entra.

    Returns:
        True si se registro la entrada, False si el parqueo esta lleno.
    """
    if len(autos_estacionados) >= CAPACIDAD_MAXIMA:
        print(f"  No puede entrar {placa}: el parqueo esta lleno.")
        return False

    autos_estacionados.append(placa)
    horas_entrada[placa] = time.time()
    guardar_evento(placa, tipo_evento="Entrada", tarifa=0.0)
    print(f"  ENTRO  {placa}")
    return True


def registrar_salida(placa: str) -> bool:
    """Registra la salida y calcula la tarifa del auto.

    Args:
        placa: Placa del auto que sale. Debe estar dentro del parqueo.

    Returns:
        True si se registro la salida, False si la placa no estaba dentro.
    """
    if placa not in autos_estacionados:
        print(f"  No se encontro la placa {placa} dentro del parqueo.")
        return False

    segundos = time.time() - horas_entrada[placa]
    minutos = max(1, math.ceil(segundos / SEGUNDOS_POR_MINUTO))
    tarifa = round(minutos * TARIFA_POR_MINUTO, 2)

    autos_estacionados.remove(placa)
    del horas_entrada[placa]
    guardar_evento(placa, tipo_evento="Salida", tarifa=tarifa)
    print(f"  SALIO  {placa} | Tiempo cobrado: {minutos} min | Tarifa: ${tarifa:.2f}")
    return True


def porcentaje_ocupacion() -> float:
    """Calcula el porcentaje de ocupacion del parqueo."""
    return (len(autos_estacionados) / CAPACIDAD_MAXIMA) * PORCENTAJE_TOTAL


def estado_parqueo() -> str:
    """Clasifica el parqueo segun su porcentaje de ocupacion."""
    porcentaje = porcentaje_ocupacion()
    if porcentaje >= UMBRAL_PARQUEO_LLENO:
        return "LLENO"
    if porcentaje >= UMBRAL_PARQUEO_MEDIO:
        return "MEDIO OCUPADO"
    return "DISPONIBLE"


def mostrar_estado() -> None:
    """Muestra ocupados, espacios libres, porcentaje y estado."""
    ocupados = len(autos_estacionados)
    libres = CAPACIDAD_MAXIMA - ocupados
    print("\n  --- Estado del parqueo ---")
    print(f"  Ocupados: {ocupados}/{CAPACIDAD_MAXIMA}")
    print(f"  Espacios libres: {libres}")
    print(f"  Porcentaje de ocupacion: {porcentaje_ocupacion():.1f}%")
    print(f"  Estado: {estado_parqueo()}")


def mostrar_autos() -> None:
    """Muestra todas las placas que estan dentro del parqueo."""
    print("\n  Autos que se encuentran dentro:")
    if not autos_estacionados:
        print("  Ninguno")
        return
    for numero, placa in enumerate(autos_estacionados, start=1):
        print(f"  {numero}. {placa}")


def pedir_entero(mensaje: str, limite: int) -> int:
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


def ejecutar_ciclo_automatico() -> None:
    """Simula un ciclo con entradas y salidas aleatorias."""
    espacios_libres = CAPACIDAD_MAXIMA - len(autos_estacionados)
    cantidad_entran = random.randint(
        0, min(MAX_AUTOS_ENTRAN_POR_CICLO, espacios_libres)
    )
    cantidad_salen = random.randint(
        0, min(MAX_AUTOS_SALEN_POR_CICLO, len(autos_estacionados))
    )

    for _ in range(cantidad_salen):
        registrar_salida(random.choice(autos_estacionados))
    for _ in range(cantidad_entran):
        registrar_entrada(generar_placa())


def ejecutar_ciclo_manual() -> None:
    """Pide al usuario cuantos autos entran y cuantos salen."""
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


def mostrar_resumen() -> None:
    """Muestra el estado final y el historial de eventos por placa."""
    print("\n" + "=" * ANCHO_SEPARADOR)
    print("SIMULACION FINALIZADA")
    mostrar_estado()
    mostrar_autos()
    print("\n  Historial de eventos por placa:")
    if not historial_autos:
        print("  No se registraron eventos.")
    for placa_historial, eventos_historial in historial_autos.items():
        print(f"\n  {placa_historial}:")
        for evento in eventos_historial:
            print(f"    {evento}")


def seleccionar_modo(modo_argumento: str | None) -> str:
    """Devuelve el modo de simulacion elegido.

    Args:
        modo_argumento: Modo recibido por linea de comandos. Si es None,
            se muestra el menu para que el usuario elija.

    Returns:
        "automatico" o "manual".
    """
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


def simular(duracion: float, intervalo: float, modo: str) -> None:
    """Ejecuta la simulacion completa y muestra el resumen al final.

    Args:
        duracion: Cuantos segundos dura la simulacion.
        intervalo: Segundos de espera entre un ciclo y el siguiente.
        modo: "automatico" o "manual".
    """
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


def leer_argumentos() -> argparse.Namespace:
    """Lee y valida los argumentos de la linea de comandos."""
    parser = argparse.ArgumentParser(
        description="Simula durante dos minutos un parqueo inteligente."
    )
    
    parser.add_argument(
        "--modo", 
        choices=["automatico", "manual"], 
        help="Evita mostrar el menu inicial."
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
    
    parser.add_argument(
        "--semilla", 
        type=int, 
        help="Semilla para repetir datos aleatorios."
    )
    
    argumentos = parser.parse_args()

    if argumentos.duracion <= 0 or argumentos.intervalo <= 0:
        parser.error("La duracion y el intervalo deben ser mayores que cero.")
    return argumentos


def main() -> None:
    """Punto de entrada del programa."""
    argumentos = leer_argumentos()
    if argumentos.semilla is not None:
        random.seed(argumentos.semilla)

    modo = seleccionar_modo(argumentos.modo)
    try:
        simular(duracion=argumentos.duracion, intervalo=argumentos.intervalo, modo=modo)
    except KeyboardInterrupt:
        print("\n\nSimulacion detenida por el usuario.")
        mostrar_resumen()


# __name__ es un atributo dunder (double underscore) que Python crea solo
# en cada modulo y cuyo valor depende de como se use el archivo:
#   vale "__main__"  si ejecutas este archivo directamente
#   vale "Parcial"   si otro archivo hace import Parcial
# Por eso main() solo se llama cuando ejecutas tu el programa.
if __name__ == "__main__":
    main()
