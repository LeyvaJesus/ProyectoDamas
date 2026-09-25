import json
import time
import os
import sys
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
tiempos = {Jugador.BLANCAS: 900.0, Jugador.NEGRAS: 900.0}
inicio_turno = time.time()

cursor_fila = 5
cursor_columna = 0

seleccion_fila = None
seleccion_columna = None

mensaje_pantalla = ""

RESET = "\033[0m"
COLOR_BLANCO = "\033[97m"
COLOR_ROJO = "\033[91m"
COLOR_GRIS = "\033[90m"

FONDO_AMARILLO = "\033[43m"  
FONDO_VERDE = "\033[42m"     

def obtenerPartidasGuardadas():
    if os.path.exists("partidas_guardadas.json"):
        try:
            with open("partidas_guardadas.json", "r") as f:
                return json.load(f)
        except:
            return []
    return []

def guardarPartida():
    global tiempos, inicio_turno
    ahora = time.time()
    transcurrido = ahora - inicio_turno
    tiempos[turno] -= transcurrido
    if tiempos[turno] < 0:
        tiempos[turno] = 0.0
    inicio_turno = ahora

    partidas = obtenerPartidasGuardadas()
    tablero_serializado = [[p.value for p in fila] for fila in tablero]
    nombre_partida = time.strftime("%Y-%m-%d %H:%M:%S")
    
    nueva_partida = {
        "fecha": nombre_partida,
        "tablero": tablero_serializado,
        "turno": turno.value,
        "tiempos": {
            Jugador.BLANCAS.value: tiempos[Jugador.BLANCAS],
            Jugador.NEGRAS.value: tiempos[Jugador.NEGRAS]
        }
    }
    
    partidas.append(nueva_partida)
    
    with open("partidas_guardadas.json", "w") as f:
        json.dump(partidas, f, indent=4)

def cargarMenuInicio():
    global tablero, turno, tiempos, inicio_turno
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== JUEGO DE DAMAS ===")
    partidas = obtenerPartidasGuardadas()
    
    if partidas:
        print("\nHISTORIAL DE PARTIDAS GUARDADAS:")
        for idx, p in enumerate(partidas, 1):
            t_info = "BLANCAS" if p["turno"] == "b" else "NEGRAS"
            print(f"  {idx}. Fecha: {p['fecha']} | Turno actual: {t_info}")
        print()
        
        opc = input("¿Deseas cargar una partida guardada? (s/n): ").strip().lower()
        if opc == 's':
            while True:
                try:
                    num = int(input(f"Selecciona el número de partida (1-{len(partidas)}): "))
                    if 1 <= num <= len(partidas):
                        p_sel = partidas[num - 1]
                        tablero = [[Pieza(val) for val in fila] for fila in p_sel["tablero"]]
                        turno = Jugador(p_sel["turno"])
                        tiempos = {
                            Jugador.BLANCAS: p_sel["tiempos"][Jugador.BLANCAS.value],
                            Jugador.NEGRAS: p_sel["tiempos"][Jugador.NEGRAS.value]
                        }
                        inicio_turno = time.time()
                        print("Partida cargada exitosamente.")
                        time.sleep(1)
                        break
                    else:
                        print("Número fuera de rango.")
                except ValueError:
                    print("Ingresa un número válido.")
    else:
        print("\nNo se encontraron partidas guardadas anteriores.")
        input("Presiona ENTER para iniciar una nueva partida...")

def leerTecla():
    if os.name == 'nt':
        import msvcrt
        tecla = msvcrt.getch()
        if tecla in [b'\r', b'\n']:
            return "enter"
        if tecla == b' ':
            return "espacio"
        try:
            return tecla.decode('utf-8').lower()
        except:
            return ""

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
            print("\n¡SE HA AGOTADO EL TIEMPO PARA LAS BLANCAS!")
            print("¡GANA EL JUGADOR DE LAS NEGRAS POR TIEMPO!")
        else:
            print("\n¡SE HA AGOTADO EL TIEMPO PARA LAS NEGRAS!")
            print("¡GANA EL JUGADOR DE LAS BLANCAS POR TIEMPO!")
        return True
    return False

def obtenerSimboloYColor(pieza):
    if pieza == Pieza.BLANCA:
        return "●", COLOR_BLANCO
    elif pieza == Pieza.DAMA_BLANCA:
        return "◉", COLOR_BLANCO
    elif pieza == Pieza.NEGRA:
        return "●", COLOR_GRIS
    elif pieza == Pieza.DAMA_NEGRA:
        return "◉", COLOR_GRIS
    return ".", COLOR_GRIS

def dibujarCasilla(f, c):
    simbolo, color_texto = obtenerSimboloYColor(tablero[f][c])
    
    if f == cursor_fila and c == cursor_columna:
        return FONDO_AMARILLO + color_texto + " " + simbolo + " " + RESET
    
    if seleccion_fila is not None and f == seleccion_fila and c == seleccion_columna:
        return FONDO_VERDE + color_texto + " " + simbolo + " " + RESET
    
    return color_texto + " " + simbolo + " " + RESET

def mostrarTablero():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== JUEGO DE DAMAS ===")
    
    t_blancas = formatearTiempo(obtenerTiempoRestante(Jugador.BLANCAS))
    t_negras = formatearTiempo(obtenerTiempoRestante(Jugador.NEGRAS))
    
    print("RELOJ -> Blancas: " + t_blancas + " | Negras: " + t_negras)
    if turno == Jugador.BLANCAS:
        print("TURNO DE BLANCAS")
    else:
        print("TURNO DE NEGRAS ")
    print("CONTROLES: [W/A/S/D] Mover cursor  [ENTER/ESPACIO] Seleccionar/Mover  [C] Cancelar  [G] Guardar  [E] Salir")

    print("   0  1  2  3  4  5  6  7")
    for f in range(8):
        linea = str(f) + " "
        for c in range(8):
            linea = linea + dibujarCasilla(f, c)
        print(linea)
    print()

    if mensaje_pantalla != "":
        print("AVISO: " + mensaje_pantalla)
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

cargarMenuInicio()

jugando = True
inicio_turno = time.time()

while jugando:
    if verificarTiempoAgotado():
        break

    mostrarTablero()

    if contarFichasJugador(turno) == 0:
        print("¡Te has quedado sin fichas! ¡Gana el otro jugador!")
        break

    tecla = leerTecla()
    mensaje_pantalla = ""

    if verificarTiempoAgotado():
        break

    if tecla == 'w' and cursor_fila > 0:
        cursor_fila = cursor_fila - 1
    elif tecla == 's' and cursor_fila < 7:
        cursor_fila = cursor_fila + 1
    elif tecla == 'a' and cursor_columna > 0:
        cursor_columna = cursor_columna - 1
    elif tecla == 'd' and cursor_columna < 7:
        cursor_columna = cursor_columna + 1
    elif tecla == 'g':
        guardarPartida()
        mensaje_pantalla = "Partida guardada correctamente."
    elif tecla == 'e':
        print("Saliste del juego")
        break
    elif tecla == 'c':
        seleccion_fila = None
        seleccion_columna = None
        mensaje_pantalla = "Selección cancelada."

    elif tecla in ['enter', 'espacio']:
        
        if seleccion_fila is None:
            if esMiFicha(tablero[cursor_fila][cursor_columna], turno):
                ahuevoComer = tieneQueComerAhuevo(turno)
                capturas = buscarCapturas(cursor_fila, cursor_columna, turno)
                
                if ahuevoComer and len(capturas) == 0:
                    mensaje_pantalla = "¡Tienes que comer una ficha obligatoriamente! Elige otra."
                else:
                    seleccion_fila = cursor_fila
                    seleccion_columna = cursor_columna
                    mensaje_pantalla = "Ficha seleccionada. Ahora mueve el cursor a la casilla de destino y presiona ENTER."
            else:
                mensaje_pantalla = "Ahí no hay una ficha tuya."

        else:
            filaOrigen = seleccion_fila
            columnaOrigen = seleccion_columna
            filaDestino = cursor_fila
            columnaDestino = cursor_columna

            piezaActual = tablero[filaOrigen][columnaOrigen]
            ahuevoComer = tieneQueComerAhuevo(turno)
            capturasDisponibles = buscarCapturas(filaOrigen, columnaOrigen, turno)

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
                pasoFila = filaDestino - filaOrigen
                pasoCol = columnaDestino - columnaOrigen

                movimientoValido = False
                if piezaActual == Pieza.BLANCA and pasoFila == -1 and abs(pasoCol) == 1:
                    movimientoValido = True
                elif piezaActual == Pieza.NEGRA and pasoFila == 1 and abs(pasoCol) == 1:
                    movimientoValido = True
                elif piezaActual in (Pieza.DAMA_BLANCA, Pieza.DAMA_NEGRA) and abs(pasoFila) == 1 and abs(pasoCol) == 1:
                    movimientoValido = True

                if movimientoValido and tablero[filaDestino][columnaDestino] == Pieza.VACIA:
                    tablero[filaDestino][columnaDestino] = piezaActual
                    tablero[filaOrigen][columnaOrigen] = Pieza.VACIA
                    seRealizoMovimiento = True

            if seRealizoMovimiento:
                if tablero[filaDestino][columnaDestino] == Pieza.BLANCA and filaDestino == 0:
                    tablero[filaDestino][columnaDestino] = Pieza.DAMA_BLANCA
                elif tablero[filaDestino][columnaDestino] == Pieza.NEGRA and filaDestino == 7:
                    tablero[filaDestino][columnaDestino] = Pieza.DAMA_NEGRA

                duracion_jugada = time.time() - inicio_turno
                tiempos[turno] = tiempos[turno] - duracion_jugada
                if tiempos[turno] < 0:
                    tiempos[turno] = 0.0

                tiempo_usado = formatearTiempo(duracion_jugada)

                if hizoCaptura:
                    masCapturas = buscarCapturas(filaDestino, columnaDestino, turno)
                    if len(masCapturas) > 0:
                        seleccion_fila = filaDestino
                        seleccion_columna = columnaDestino
                        mensaje_pantalla = "¡Puedes seguir comiendo otra ficha!"
                        inicio_turno = time.time()
                        continue

                seleccion_fila = None
                seleccion_columna = None

                if turno == Jugador.BLANCAS:
                    mensaje_pantalla = "Las BLANCAS tardaron " + tiempo_usado + " en mover."
                    turno = Jugador.NEGRAS
                else:
                    mensaje_pantalla = "Las NEGRAS tardaron " + tiempo_usado + " en mover."
                    turno = Jugador.BLANCAS

                inicio_turno = time.time()
            else:
                mensaje_pantalla = "Movimiento no permitido. Intenta de nuevo o presiona C para cancelar."