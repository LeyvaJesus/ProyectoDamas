tablero = [
    ['.', 'n', '.', 'n', '.', 'n', '.', 'n'],
    ['n', '.', 'n', '.', 'n', '.', 'n', '.'],
    ['.', 'n', '.', 'n', '.', 'n', '.', 'n'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['b', '.', 'b', '.', 'b', '.', 'b', '.'],
    ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
    ['b', '.', 'b', '.', 'b', '.', 'b', '.']
]

turno = 'b'
def esNumero(texto):
    if len(texto) == 0:
        return False
    
    inicio = 0
    if texto[0] == '-':
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
            textoFila = textoFila + tablero[i][j] + " "
        print(textoFila)
    print()

def esMiFicha(pieza, jugador):
    if jugador == 'b' and (pieza == 'b' or pieza == 'B'):  
        return True
    if jugador == 'n' and (pieza == 'n' or pieza == 'N'):
        return True
    return False

def buscarCapturas(fila, columna, jugador):
    capturas = []
    pieza = tablero[fila][columna]
    
    direcciones = []
    if pieza == 'b':
        direcciones = [(-1, -1), (-1, 1)] 
    elif pieza == 'n':
        direcciones = [(1, -1), (1, 1)]
    elif pieza == 'B' or pieza == 'N':
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)] 

    for pasoFila, pasoColumna in direcciones:
        filaMitad = fila + pasoFila
        columnaMitad = columna + pasoColumna
        filaDestino = fila + (2 * pasoFila)
        columnaDestino = columna + (2 * pasoColumna)

        if filaDestino >= 0 and filaDestino < 8 and columnaDestino >= 0 and columnaDestino < 8:
            piezaMitad = tablero[filaMitad][columnaMitad]
            piezaDestino = tablero[filaDestino][columnaDestino]

            esEnemigo = False
            if jugador == 'b' and (piezaMitad == 'n' or piezaMitad == 'N'):
                esEnemigo = True
            elif jugador == 'n' and (piezaMitad == 'b' or piezaMitad == 'B'):
                esEnemigo = True

            if esEnemigo and piezaDestino == '.':
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

while jugando:
    mostrarTablero()
    if turno == 'b':
        print("Turno del jugador: BLANCAS (b)")
    else:
        print("Turno del jugador: NEGRAS (n)")

    if contarFichasJugador(turno) == 0:
        print("¡Te has quedado sin fichas! ¡Gana el otro jugador!")
        break

    entradaFilaOrigen = input("Fila de la ficha a mover (o -1 para rendirse): ")
    if not esNumero(entradaFilaOrigen):
        print("Escribe un número entero válido.")
        continue
    
    filaOrigen = int(entradaFilaOrigen)
    if filaOrigen == -1:
        print("El juego ha terminado.")
        break

    entradaColumnaOrigen = input("Columna de la ficha a mover: ")
    if not esNumero(entradaColumnaOrigen):
        print("Escribe un número válido.")
        continue
    columnaOrigen = int(entradaColumnaOrigen)

    if filaOrigen < 0 or filaOrigen >= 8 or columnaOrigen < 0 or columnaOrigen >= 8:
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

    entradaFilaDestino = input("Fila a donde la quieres mover: ")
    if not esNumero(entradaFilaDestino):
        print("Escribe un número válido.")
        continue
    filaDestino = int(entradaFilaDestino)

    entradaColumnaDestino = input("Columna a donde la quieres mover: ")
    if not esNumero(entradaColumnaDestino):
        print("Escribe un número válido.")
        continue
    columnaDestino = int(entradaColumnaDestino)

    if filaDestino < 0 or filaDestino >= 8 or columnaDestino < 0 or columnaDestino >= 8:
        print("El destino está fuera del tablero.")
        continue

    piezaActual = tablero[filaOrigen][columnaOrigen]
    seRealizoMovimiento = False
    hizoCaptura = False

    for opcion in capturasDisponibles:
        if opcion[0] == filaDestino and opcion[1] == columnaDestino:
            tablero[filaDestino][columnaDestino] = piezaActual
            tablero[filaOrigen][columnaOrigen] = '.'
            tablero[opcion[2]][opcion[3]] = '.'
            seRealizoMovimiento = True
            hizoCaptura = True
            break

    if not ahuevoComer and not seRealizoMovimiento:
        movimientoValido = False
        diferenciaFila = filaDestino - filaOrigen
        diferenciaColumna = columnaDestino - columnaOrigen

        if (diferenciaColumna == 1 or diferenciaColumna == -1) and tablero[filaDestino][columnaDestino] == '.':
            if piezaActual == 'b' and diferenciaFila == -1:
                movimientoValido = True
            elif piezaActual == 'n' and diferenciaFila == 1:
                movimientoValido = True
            elif (piezaActual == 'B' or piezaActual == 'N') and (diferenciaFila == 1 or diferenciaFila == -1):
                movimientoValido = True

        if movimientoValido:
            tablero[filaDestino][columnaDestino] = piezaActual
            tablero[filaOrigen][columnaOrigen] = '.'
            seRealizoMovimiento = True
        else:
            print("Ese movimiento no está permitido.")

    if seRealizoMovimiento:
        if tablero[filaDestino][columnaDestino] == 'b' and filaDestino == 0:
            tablero[filaDestino][columnaDestino] = 'B'
            print("¡Tu ficha blanca se convirtió en Dama 'B'!")
        elif tablero[filaDestino][columnaDestino] == 'n' and filaDestino == 7:
            tablero[filaDestino][columnaDestino] = 'N'
            print("¡Tu ficha negra se convirtió en Dama 'N'!")

        if hizoCaptura:
            masCapturas = buscarCapturas(filaDestino, columnaDestino, turno)
            if len(masCapturas) > 0:
                print("¡Puedes seguir comiendo otra ficha!")
                continue

        if turno == 'b':
            turno = 'n'
        else:
            turno = 'b'