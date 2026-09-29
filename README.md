# Sistema de Parqueo Inteligente

Simulacion en Python de un parqueo para un centro comercial. Genera autos que
entran y salen, calcula la ocupacion, cobra una tarifa por minuto y guarda el
historial de eventos de cada placa.

Examen Parcial #1 - Desarrollo de Software 8

## Requisitos

Python 3.10 o superior. No hay que instalar nada, solo la libreria estandar.

## Como ejecutar

```bash
python Parcial.py
```

Sin argumentos, el programa muestra un menu para elegir el modo:

1. Automatico (movimientos aleatorios)
2. Manual (el usuario indica las cantidades)

### Argumentos

| Argumento | Descripcion | Predeterminado |
|---|---|---|
| `--modo` | `automatico` o `manual`, evita el menu inicial | pregunta al usuario |
| `--duracion` | Cuantos segundos dura la simulacion | `120` |
| `--intervalo` | Segundos de espera entre ciclos | `5` |
| `--semilla` | Fija la semilla para repetir los mismos datos | ninguno |

`--duracion` y `--intervalo` deben ser mayores que cero.

### Ejemplos

```bash
python Parcial.py --modo automatico --duracion 30 --intervalo 5
python Parcial.py --modo manual
```

## Integrantes y grupo

- Grupo 1: 
- Integrantes:
  - Abdias Ruedas 8-1011-2210 
  - Jose Sanchez 8-1032-2111
  - Miguel Martinez 8-960-778
  - Whitney Ault 8-984-1977
