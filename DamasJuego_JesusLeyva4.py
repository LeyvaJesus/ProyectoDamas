import json
import time
from enum import Enum

class Jugador(Enum):
    BLANCAS = "b"
    NEGRAS = "n"

class Pieza(Enum):
    VACIA = "."
    BLANCA = "b"
    NEGRA = "n"
    DAMA_BLANCA = "B"
    DAMA_NEGRA = "N"

tablero = [
    [Pieza.VACIA, Pieza.NEGRA, Pieza.VACIA, Pieza.NEGRA, Pieza.VACIA, Pieza.NEGRA, Pieza.VACIA, Pieza.NEGRA],
    [Pieza.NEGRA, Pieza.VACIA, Pieza.NEGRA, Pieza.VACIA, Pieza.NEGRA, Pieza.VACIA, Pieza.NEGRA, Pieza.VACIA],
    [Pieza.VACIA, Pieza.NEGRA, Pieza.VACIA, Pieza.NEGRA, Pieza.VACIA, Pieza.NEGRA, Pieza.VACIA, Pieza.NEGRA],
    [Pieza.VACIA, Pieza.VACIA, Pieza.VACIA, Pieza.VACIA, Pieza.VACIA, Pieza.VACIA, Pieza.VACIA, Pieza.VACIA],
    [Pieza.VACIA, Pieza.VACIA, Pieza.VACIA, Pieza.VACIA, Pieza.VACIA, Pieza.VACIA, Pieza.VACIA, Pieza.VACIA],
    [Pieza.BLANCA, Pieza.VACIA, Pieza.BLANCA, Pieza.VACIA, Pieza.BLANCA, Pieza.VACIA, Pieza.BLANCA, Pieza.VACIA],
    [Pieza.VACIA, Pieza.BLANCA, Pieza.VACIA, Pieza.BLANCA, Pieza.VACIA, Pieza.BLANCA, Pieza.VACIA, Pieza.BLANCA],
    [Pieza.BLANCA, Pieza.VACIA, Pieza.BLANCA, Pieza.VACIA, Pieza.BLANCA, Pieza.VACIA, Pieza.BLANCA, Pieza.VACIA],
]

turno = Jugador.BLANCAS
tiempos = {Jugador.BLANCAS: 10.0, Jugador.NEGRAS: 900.0}
inicio_turno = time.time()

RESET = "\033[0m"
BLANCO = "\033[97m"
NEGRO = "\033[90m"

def formatearTiempo(segundos):
    segundos_enteros = int(segundos)
    if segundos_enteros < 0:
        segundos_enteros = 0
    
    minutos = segundos_enteros // 60
    segs = segundos_enteros % 60

    texto_min = str(minutos)
    if minutos < 10:
        texto_min = "0" + str(minutos)

    texto_seg = str(segs)
    if segs < 10:
        texto_seg = "0" + str(segs)

    return texto_min + ":" + texto_seg

def obtenerTiempoRestante(jugador):
    if jugador == turno:
        transcurrido = time.time() - inicio_turno
        restante = tiempos[jugador] - transcurrido
        if restante < 0:
            return 0.0
        return restante
    return tiempos[jugador]

def verificarTiempoAgotado():
    if obtenerTiempoRestante(turno) <= 0:
        tiempos[turno] = 0.0
        if turno == Jugador.BLANCAS:
            print("\nSE ACABO EL TIEMPO PARA LAS BLANCAS")
            print("GANAN LAS NEGRAS")
        else:
            print("\nSE ACABO EL TIEMPO PARA LAS NEGRAS")
            print("GANAN LAS BLANCAS")
        return True
    return False

def guardarPartida():
    global inicio_turno
    ahora = time.time()
    tiempos[turno] = tiempos[turno] - (ahora - inicio_turno)
    inicio_turno = ahora
    
    datos = {
        "tablero": [[p.value for p in fila] for fila in tablero],
        "turno": turno.value,
        "tiempos": {
            Jugador.BLANCAS.value: tiempos[Jugador.BLANCAS],
            Jugador.NEGRAS.value: tiempos[Jugador.NEGRAS]
        }
    }
    with open("partida.json", "w") as archivo:
        json.dump(datos, archivo)
    print("¡Partida guardada correctamnte en 'partida.json'!")

def cargarPartida():
    global tablero, turno, tiempos, inicio_turno
    try:
        with open("partida.json", "r") as archivo:
            datos = json.load(archivo)
            tablero = [[Pieza(valor) for valor in fila] for fila in datos["tablero"]]
            turno = Jugador(datos["turno"])
            if "tiempos" in datos:
                tiempos = {
                    Jugador.BLANCAS: datos["tiempos"]["b"],
                    Jugador.NEGRAS: datos["tiempos"]["n"]
                }
            inicio_turno = time.time()
        print("¡Partida cargada exitosamente!")
        return True
    except FileNotFoundError:
        print("No se encontró ninguna partida guardada")
        return False

def obtenerFichaColoreada(pieza):
    Simbolos = {
        Pieza.VACIA: "·",
        Pieza.BLANCA: BLANCO + "○" + RESET,
        Pieza.NEGRA: NEGRO + "●" + RESET,
        Pieza.DAMA_BLANCA: BLANCO + "◎" + RESET,
        Pieza.DAMA_NEGRA: NEGRO + "◉" + RESET,
    }
    return Simbolos.get(pieza, pieza.value)

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
    if jugador == Jugador.BLANCAS and pieza in (Pieza.BLANCA, Pieza.DAMA_BLANCA):
        return True
    if jugador == Jugador.NEGRAS and pieza in (Pieza.NEGRA, Pieza.DAMA_NEGRA):
        return True
    return False

def buscarCapturas(fila, columna, jugador):
    capturas = []
    pieza = tablero[fila][columna]

    direcciones = []
    if pieza == Pieza.BLANCA:
        direcciones = [(-1, -1), (-1, 1)]
    elif pieza == Pieza.NEGRA:
        direcciones = [(1, -1), (1, 1)]
    elif pieza in (Pieza.DAMA_BLANCA, Pieza.DAMA_NEGRA):
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for pasoFila, pasoColumna in direcciones:
        filaMitad = fila + pasoFila
        columnaMitad = columna + pasoColumna
        filaDestino = fila + (2 * pasoFila)
        columnaDestino = columna + (2 * pasoColumna)

        if (filaDestino >= 0 and filaDestino < 8 and columnaDestino >= 0 and columnaDestino < 8):
            piezaMitad = tablero[filaMitad][columnaMitad]
            piezaDestino = tablero[filaDestino][columnaDestino]

            esEnemigo = False
            if jugador == Jugador.BLANCAS and piezaMitad in (Pieza.NEGRA, Pieza.DAMA_NEGRA):
                esEnemigo = True
            elif jugador == Jugador.NEGRAS and piezaMitad in (Pieza.BLANCA, Pieza.DAMA_BLANCA):
                esEnemigo = True

            if esEnemigo and piezaDestino == Pieza.VACIA:
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

inicio_turno = time.time()

while jugando:
    if verificarTiempoAgotado():
        break

    mostrarTablero()
    
    t_blancas = formatearTiempo(obtenerTiempoRestante(Jugador.BLANCAS))
    t_negras = formatearTiempo(obtenerTiempoRestante(Jugador.NEGRAS))
    
    print("RELOJ: Blancas: " + t_blancas + " | Negras: " + t_negras)
    if turno == Jugador.BLANCAS:
        print("TURNO DE: BLANCAS (b)")
    else:
        print("TURNO DE: NEGRAS (n)")

    if contarFichasJugador(turno) == 0:
        print("¡Te has quedado sin fichas!")
        if turno == Jugador.BLANCAS:
            print("GANAN LAS NEGRAS")
        else:
            print("GANAN LAS BLANCAS")
        break

    entradaFilaOrigen = input("Fila de la ficha a mover (o -1 para rendirse, -2 para guardar): ")
    if verificarTiempoAgotado():
        break

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
    if verificarTiempoAgotado():
        break

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
    if verificarTiempoAgotado():
        break

    if direccion not in ["izq", "der"]:
        print("Dirección no válida. Escribe 'izq' o 'der'")
        continue

    piezaActual = tablero[filaOrigen][columnaOrigen]
    if direccion == "izq":
        pasoCol = -1 
    else:
        pasoCol = 1

    pasoFila = 0
    if piezaActual == Pieza.BLANCA:
        pasoFila = -1
    elif piezaActual == Pieza.NEGRA:
        pasoFila = 1
    elif piezaActual in (Pieza.DAMA_BLANCA, Pieza.DAMA_NEGRA):
        sentido = input("¿Avanzar o retroceder? (arriba / abajo): ").strip().lower()
        if verificarTiempoAgotado():
            break

        if sentido == "arriba":
            pasoFila = -1
        elif sentido == "abajo":
            pasoFila = 1
        else:
            print("Opción no válida")
            continue

    if ahuevoComer:
        filaDestino = filaOrigen + (2 * pasoFila)
        columnaDestino = columnaOrigen + (2 * pasoCol)
    else:
        filaDestino = filaOrigen + pasoFila
        columnaDestino = columnaOrigen + pasoCol

    if (filaDestino < 0 or filaDestino >= 8 or columnaDestino < 0 or columnaDestino >= 8):
        print("Ese movimiento se sale del tablero")
        continue

    seRealizoMovimiento = False
    hizoCaptura = False

    for opcion in capturasDisponibles:
        if opcion[0] == filaDestino and opcion[1] == columnaDestino:
            tablero[filaDestino][columnaDestino] = piezaActual
            tablero[filaOrigen][columnaOrigen] = Pieza.VACIA
            tablero[opcion[2]][opcion[3]] = Pieza.VACIA
            seRealizoMovimiento = True
            hizoCaptura = True
            break

    if not ahuevoComer and not seRealizoMovimiento:
        if tablero[filaDestino][columnaDestino] == Pieza.VACIA:
            tablero[filaDestino][columnaDestino] = piezaActual
            tablero[filaOrigen][columnaOrigen] = Pieza.VACIA
            seRealizoMovimiento = True
        else:
            print("Esa casilla no está vacía o el movimiento no está permitido")

    if seRealizoMovimiento:
        if tablero[filaDestino][columnaDestino] == Pieza.BLANCA and filaDestino == 0:
            tablero[filaDestino][columnaDestino] = Pieza.DAMA_BLANCA
            print("¡Tu ficha blanca se convirtió en Dama 'B'!")
        elif tablero[filaDestino][columnaDestino] == Pieza.NEGRA and filaDestino == 7:
            tablero[filaDestino][columnaDestino] = Pieza.DAMA_NEGRA
            print("¡Tu ficha negra se convirtió en Dama 'N'!")

        duracion_jugada = time.time() - inicio_turno
        tiempos[turno] = tiempos[turno] - duracion_jugada
        if tiempos[turno] < 0:
            tiempos[turno] = 0.0

        if hizoCaptura:
            masCapturas = buscarCapturas(filaDestino, columnaDestino, turno)
            if len(masCapturas) > 0:
                print("Puedes seguir comiendo otra ficha")
                inicio_turno = time.time()
                continue

        tiempo_usado = formatearTiempo(duracion_jugada)
        if turno == Jugador.BLANCAS:
            print("\nFIN DEL TURNO. Las BLANCAS tardaron " + tiempo_usado + " en mover.\n")
        else:
            print("\nFIN DEL TURNO. Las NEGRAS tardaron " + tiempo_usado + " en mover.\n")

        if turno == Jugador.BLANCAS:
            turno = Jugador.NEGRAS
        else:
            turno = Jugador.BLANCAS
        
        inicio_turno = time.time()