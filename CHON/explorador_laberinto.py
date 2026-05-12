import os
import random
import time


ANCHO = 31
ALTO = 17
ENERGIA_INICIAL = 70


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def crear_mapa(semilla=None):
    rng = random.Random(semilla)
    mapa = [["#" for _ in range(ANCHO)] for _ in range(ALTO)]

    x, y = 1, 1
    mapa[y][x] = "."
    pasos = ANCHO * ALTO * 3

    for _ in range(pasos):
        dx, dy = rng.choice([(2, 0), (-2, 0), (0, 2), (0, -2)])
        nx, ny = x + dx, y + dy

        if 1 <= nx < ANCHO - 1 and 1 <= ny < ALTO - 1:
            mapa[y + dy // 2][x + dx // 2] = "."
            mapa[ny][nx] = "."
            x, y = nx, ny

    libres = [(x, y) for y in range(ALTO) for x in range(ANCHO) if mapa[y][x] == "."]
    inicio = (1, 1)
    salida = max(libres, key=lambda p: distancia_manhattan(inicio, p))
    mapa[salida[1]][salida[0]] = "S"

    colocar_objetos(mapa, rng, "E", 9)
    colocar_objetos(mapa, rng, "R", 5)
    colocar_objetos(mapa, rng, "?", 8)

    return mapa, inicio, salida, rng


def colocar_objetos(mapa, rng, simbolo, cantidad):
    libres = [
        (x, y)
        for y in range(ALTO)
        for x in range(ANCHO)
        if mapa[y][x] == "." and (x, y) != (1, 1)
    ]
    for x, y in rng.sample(libres, min(cantidad, len(libres))):
        mapa[y][x] = simbolo


def distancia_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def revelar(vistos, posicion, radio=3):
    px, py = posicion
    for y in range(max(0, py - radio), min(ALTO, py + radio + 1)):
        for x in range(max(0, px - radio), min(ANCHO, px + radio + 1)):
            if distancia_manhattan((px, py), (x, y)) <= radio:
                vistos.add((x, y))


def dibujar(mapa, vistos, jugador, energia, reliquias, mensaje):
    limpiar_pantalla()
    print("EXPLORADOR DEL LABERINTO")
    print("Controles: W/A/S/D para moverte, Q para salir\n")

    for y, fila in enumerate(mapa):
        linea = []
        for x, celda in enumerate(fila):
            if (x, y) == jugador:
                linea.append("@")
            elif (x, y) not in vistos:
                linea.append(" ")
            else:
                linea.append(celda)
        print("".join(linea))

    print(f"\nEnergia: {energia:02d} | Reliquias: {reliquias}/5")
    print(mensaje)


def resolver_evento(rng, energia, reliquias):
    eventos = [
        ("Encontraste una fuente subterranea. +10 energia.", 10, 0),
        ("Una trampa antigua se activo. -8 energia.", -8, 0),
        ("Descifraste una marca del muro. +1 reliquia.", 0, 1),
        ("Un pasadizo se derrumba detras tuyo. -5 energia.", -5, 0),
        ("Respiraste, escuchaste, y elegiste bien. +4 energia.", 4, 0),
    ]
    texto, delta_energia, delta_reliquias = rng.choice(eventos)
    return energia + delta_energia, reliquias + delta_reliquias, texto


def intentar_mover(mapa, posicion, direccion):
    movimientos = {
        "w": (0, -1),
        "a": (-1, 0),
        "s": (0, 1),
        "d": (1, 0),
    }
    dx, dy = movimientos[direccion]
    nx, ny = posicion[0] + dx, posicion[1] + dy
    if mapa[ny][nx] == "#":
        return posicion, False
    return (nx, ny), True


def jugar(semilla=None, movimientos_demo=None):
    mapa, jugador, salida, rng = crear_mapa(semilla)
    energia = ENERGIA_INICIAL
    reliquias = 0
    vistos = set()
    mensaje = "Busca la salida S. Las R son reliquias, E energia y ? eventos."
    demo_activa = movimientos_demo is not None
    movimientos_demo = list(movimientos_demo or [])

    while True:
        revelar(vistos, jugador)
        dibujar(mapa, vistos, jugador, energia, reliquias, mensaje)

        if jugador == salida:
            if reliquias >= 3:
                print("\nGanaste: saliste con suficientes reliquias para contar la historia.")
            else:
                print("\nLlegaste a la salida, pero te faltaron reliquias. Final incompleto.")
            break

        if energia <= 0:
            print("\nTe quedaste sin energia en el laberinto.")
            break

        if movimientos_demo:
            accion = movimientos_demo.pop(0)
            time.sleep(0.05)
        elif demo_activa:
            print("\nDemo terminada.")
            break
        else:
            accion = input("\nMovimiento: ").strip().lower()[:1]

        if accion == "q":
            print("\nPartida terminada.")
            break
        if accion not in "wasd":
            mensaje = "Comando invalido. Usa W, A, S, D o Q."
            continue

        nueva_posicion, se_movio = intentar_mover(mapa, jugador, accion)
        if not se_movio:
            energia -= 1
            mensaje = "Hay una pared. Pierdes 1 energia intentando avanzar."
            continue

        jugador = nueva_posicion
        energia -= 1
        x, y = jugador
        celda = mapa[y][x]

        if celda == "E":
            energia += 15
            mapa[y][x] = "."
            mensaje = "Encontraste provisiones. +15 energia."
        elif celda == "R":
            reliquias += 1
            mapa[y][x] = "."
            mensaje = "Guardaste una reliquia antigua."
        elif celda == "?":
            energia, reliquias, mensaje = resolver_evento(rng, energia, reliquias)
            mapa[y][x] = "."
        else:
            mensaje = "Avanzas por el corredor humedo."


def main():
    print("1) Jugar")
    print("2) Demo automatica")
    opcion = input("Elegir modo: ").strip()

    if opcion == "2":
        jugar(semilla=2026, movimientos_demo="ddddssssaaaawwwddddssssddddwwwwaaaassss")
    else:
        texto_semilla = input("Semilla opcional, enter para azar: ").strip()
        semilla = texto_semilla or None
        jugar(semilla=semilla)


if __name__ == "__main__":
    main()
