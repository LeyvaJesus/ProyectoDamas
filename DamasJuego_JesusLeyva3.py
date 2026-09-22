tablero = [
    [".", "n", ".", "n", ".", "n", ".", "n"],
    ["n", ".", "n", ".", "n", ".", "n", "."],
    [".", "n", ".", "n", ".", "n", ".", "n"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    ["b", ".", "b", ".", "b", ".", "b", "."],
    [".", "b", ".", "b", ".", "b", ".", "b"],
    ["b", ".", "b", ".", "b", ".", "b", "."],
]

turno = "b"

RESET = "\033[0m"
BLANCO = "\033[97m"
NEGRO = "\033[90m"
import json
def guardarPartida():
    datos = {
        "tablero": tablero,
        "turno": turno
    }
    with open("partida.json", "w") as archivo:
        json.dump(datos, archivo)
    print("¡Partida guardada correctamente en 'partida.json'!")

def cargarPartida():
    global tablero, turno
    try:
        with open("partida.json", "r") as archivo:
            datos = json.load(archivo)
            tablero = datos["tablero"]
            turno = datos["turno"]
        print("¡Partida cargada exitosamente!")
        return True
    except FileNotFoundError:
        print("No se encontró ninguna partida guardada.")
        return False

def obtenerFichaColoreada(pieza):
    if pieza == "b" or pieza == "B":
        return BLANCO + pieza + RESET
    elif pieza == "n" or pieza == "N":
        return NEGRO + pieza + RESET
    return "."

def esNumero(texto):
    if len(texto) == 0:
        return False

    inicio = 0
    if texto[0] == "-":
        inicio = 1
        if len(texto) == 1:
            return False

    numeros = "0123456789"
    for caracter in texto[inicio:]:
        if caracter not in numeros:
            return False

    return True


def mostrarTablero():
    print("\n  0 1 2 3 4 5 6 7")
    for i in range(8):
        textoFila = str(i) + " "
        for j in range(8):
            textoFila = textoFila + obtenerFichaColoreada(tablero[i][j]) + " "
        print(textoFila)
    print()


def esMiFicha(pieza, jugador):
    if jugador == "b" and (pieza == "b" or pieza == "B"):
        return True
    if jugador == "n" and (pieza == "n" or pieza == "N"):
        return True
    return False


def buscarCapturas(fila, columna, jugador):
    capturas = []
    pieza = tablero[fila][columna]

    direcciones = []
    if pieza == "b":
        direcciones = [(-1, -1), (-1, 1)]
    elif pieza == "n":
        direcciones = [(1, -1), (1, 1)]
    elif pieza == "B" or pieza == "N":
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for pasoFila, pasoColumna in direcciones:
        filaMitad = fila + pasoFila
        columnaMitad = columna + pasoColumna
        filaDestino = fila + (2 * pasoFila)
        columnaDestino = columna + (2 * pasoColumna)

        if (
            filaDestino >= 0
            and filaDestino < 8
            and columnaDestino >= 0
            and columnaDestino < 8
        ):
            piezaMitad = tablero[filaMitad][columnaMitad]
            piezaDestino = tablero[filaDestino][columnaDestino]

            esEnemigo = False
            if jugador == "b" and (piezaMitad == "n" or piezaMitad == "N"):
                esEnemigo = True
            elif jugador == "n" and (piezaMitad == "b" or piezaMitad == "B"):
                esEnemigo = True

            if esEnemigo and piezaDestino == ".":
                capturas.append((filaDestino, columnaDestino, filaMitad, columnaMitad))

    return capturas


def tieneQueComerAhuevo(jugador):
    for f in range(8):
        for c in range(8):
            if esMiFicha(tablero[f][c], jugador):
                if len(buscarCapturas(f, c, jugador)) > 0:
                    return True
    return False


def contarFichasJugador(jugador):
    total = 0
    for f in range(8):
        for c in range(8):
            if esMiFicha(tablero[f][c], jugador):
                total = total + 1
    return total


jugando = True

print("=== JUEGO DE DAMAS ===")
opcionInicio = input("¿Deseas cargar la última partida guardada? (s/n): ").strip().lower()
if opcionInicio == "s":
    cargarPartida()
    
while jugando:
    mostrarTablero()
    if turno == "b":
        print("Turno del jugador: BLANCAS (b)")
    else:
        print("Turno del jugador: NEGRAS (n)")

    if contarFichasJugador(turno) == 0:
        print("¡Te has quedado sin fichas! ¡Gana el otro jugador!")
        break

    entradaFilaOrigen = input("Fila de la ficha a mover (o -1 para rendirse, -2 para guardar): ")
    if not esNumero(entradaFilaOrigen):
        print("Escribe un número entero válido.")
        continue

    filaOrigen = int(entradaFilaOrigen)
    if filaOrigen == -1:
        print("El juego ha terminado.")
        break
    
    if filaOrigen == -2:
        guardarPartida()
        continue
    
    entradaColumnaOrigen = input("Columna de la ficha a mover: ")
    if not esNumero(entradaColumnaOrigen):
        print("Escribe un número válido.")
        continue
    columnaOrigen = int(entradaColumnaOrigen)

    if (filaOrigen < 0 or filaOrigen >= 8 or columnaOrigen < 0 or columnaOrigen >= 8):
        print("Esa posición está fuera del tablero.")
        continue

    if not esMiFicha(tablero[filaOrigen][columnaOrigen], turno):
        print("Esa casilla no tiene una de tus fichas.")
        continue

    ahuevoComer = tieneQueComerAhuevo(turno)
    capturasDisponibles = buscarCapturas(filaOrigen, columnaOrigen, turno)

    if ahuevoComer and len(capturasDisponibles) == 0:
        print("¡Tienes que comer una ficha! Elige otra ficha.")
        continue
    
    direccion = input("¿Hacia dónde te quieres mover? (izq / der): ").strip().lower()
    if direccion not in ["izq", "der"]:
        print("Dirección no válida. Escribe 'izq' o 'der'")
        continue

    piezaActual = tablero[filaOrigen][columnaOrigen]
    if direccion == "izq":
        pasoCol = -1 
    else:
        pasoCol = 1

    pasoFila = 0
    if piezaActual == "b":
        pasoFila = -1
    elif piezaActual == "n":
        pasoFila = 1
    elif piezaActual == "B" or piezaActual == "N":
        sentido = input("¿Avanzar o retroceder? (arriba / abajo): ").strip().lower()
        if sentido == "arriba":
            pasoFila = -1
        elif sentido == "abajo":
            pasoFila = 1
        else:
            print("Opción no válida.")
            continue

    if ahuevoComer:
        filaDestino = filaOrigen + (2 * pasoFila)
        columnaDestino = columnaOrigen + (2 * pasoCol)
    else:
        filaDestino = filaOrigen + pasoFila
        columnaDestino = columnaOrigen + pasoCol

    if (filaDestino < 0 or filaDestino >= 8 or columnaDestino < 0 or columnaDestino >= 8):
        print("Ese movimiento se sale del tablero.")
        continue

    seRealizoMovimiento = False
    hizoCaptura = False

    for opcion in capturasDisponibles:
        if opcion[0] == filaDestino and opcion[1] == columnaDestino:
            tablero[filaDestino][columnaDestino] = piezaActual
            tablero[filaOrigen][columnaOrigen] = "."
            tablero[opcion[2]][opcion[3]] = "."
            seRealizoMovimiento = True
            hizoCaptura = True
            break

    if not ahuevoComer and not seRealizoMovimiento:
        if tablero[filaDestino][columnaDestino] == ".":
            tablero[filaDestino][columnaDestino] = piezaActual
            tablero[filaOrigen][columnaOrigen] = "."
            seRealizoMovimiento = True
        else:
            print("Esa casilla no está vacía o el movimiento no está permitido.")

    if seRealizoMovimiento:
        if (
            tablero[filaDestino][columnaDestino] == "b"
            and filaDestino == 0
        ):
            tablero[filaDestino][columnaDestino] = "B"
            print("¡Tu ficha blanca se convirtió en Dama 'B'!")
        elif (tablero[filaDestino][columnaDestino] == "n" and filaDestino == 7
        ):
            tablero[filaDestino][columnaDestino] = "N"
            print("¡Tu ficha negra se convirtió en Dama 'N'!")

        if hizoCaptura:
            masCapturas = buscarCapturas(filaDestino, columnaDestino, turno)
            if len(masCapturas) > 0:
                print("¡Puedes seguir comiendo otra ficha!")
                continue

        if turno == "b":
            turno = "n"
        else:
            turno = "b"