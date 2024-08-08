import pygame
import time

# Inicializamos pygame
pygame.init()
screen = pygame.display.set_mode((450, 450))
pygame.display.set_caption("Triki - Taller 4 IA")

fondo = pygame.image.load("static/fondotriki.png")
circulo = pygame.image.load("static/circulotriki.png")
equis = pygame.image.load("static/equistriki.png")

fondo = pygame.transform.scale(fondo, (450, 450))
circulo = pygame.transform.scale(circulo, (125, 125))
equis = pygame.transform.scale(equis, (125, 125))

coor = [[(10,20),(165,20),(320,20)],
        [(10,165),(165,165),(320,165)],
        [(10,320),(165,320),(320,320)]]

tablero = [['','',''],
           ['','',''],
           ['','','']]

turno = 'X'
game_over = False
clock = pygame.time.Clock()

def graficar_board():
    screen.blit(fondo, (0, 0))
    for fila in range(3):
        for columna in range(3):
            if tablero[fila][columna] == 'X':
                dibujar_x(fila, columna)
            elif tablero[fila][columna] == 'O':
                dibujar_o(fila, columna)
    
def dibujar_x(fila, columna):
    screen.blit(equis, coor[fila][columna])

def dibujar_o(fila, columna):
    screen.blit(circulo, coor[fila][columna])

def verificar_ganador(tablero):
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != '':
            return tablero[i][0]
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != '':
            return tablero[0][i]
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != '':
        return tablero[0][0]
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != '':
        return tablero[0][2]
    return None

def tablero_lleno(tablero):
    for fila in range(3):
        for columna in range(3):
            if tablero[fila][columna] == '':
                return False
    return True

def algoritmo_minimax(tablero, profundidad, esMaximizador):
    ganador = verificar_ganador(tablero)
    if ganador == 'O':
        return 1
    if ganador == 'X':
        return -1
    if tablero_lleno(tablero):
        return 0

    if esMaximizador:
        mejor = -1000
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == '':
                    tablero[i][j] = 'O'
                    valor = algoritmo_minimax(tablero, profundidad + 1, False)
                    mejor = max(mejor, valor)
                    tablero[i][j] = ''
                    if profundidad == 0:  # Mostrar en la raíz del árbol Minimax
                        print(f"Movimiento: ({i}, {j}), Valor: {valor}")
        return mejor
    else:
        mejor = 1000
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == '':
                    tablero[i][j] = 'X'
                    valor = algoritmo_minimax(tablero, profundidad + 1, True)
                    mejor = min(mejor, valor)
                    tablero[i][j] = ''
        return mejor

def mejor_movimiento(tablero, jugador):
    mejor_valor = -1000 if jugador == 'O' else 1000
    mejor_mov = (-1, -1)
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == '':
                tablero[i][j] = jugador
                movimiento_valor = algoritmo_minimax(tablero, 0, jugador == 'X')
                tablero[i][j] = ''
                if jugador == 'O':
                    if movimiento_valor > mejor_valor:
                        mejor_mov = (i, j)
                        mejor_valor = movimiento_valor
                else:
                    if movimiento_valor < mejor_valor:
                        mejor_mov = (i, j)
                        mejor_valor = movimiento_valor
    print(f"Mejor movimiento: {mejor_mov}, Valor: {mejor_valor}")
    return mejor_mov

def realizar_movimiento(jugador):
    if jugador == 'X':
        fila, columna = mejor_movimiento(tablero, 'X')
        if fila != -1 and columna != -1:
            tablero[fila][columna] = 'X'
            return True
    elif jugador == 'O':
        fila, columna = mejor_movimiento(tablero, 'O')
        if fila != -1 and columna != -1:
            tablero[fila][columna] = 'O'
            return True
    return False

primera_jugada = True

while not game_over:
    clock.tick(30)

    if primera_jugada:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos

                fila = -1
                columna = -1

                if 10 <= mouseX < 155:
                    columna = 0
                elif 165 <= mouseX < 310:
                    columna = 1
                elif 320 <= mouseX < 465:
                    columna = 2

                if 20 <= mouseY < 165:
                    fila = 0
                elif 165 <= mouseY < 310:
                    fila = 1
                elif 320 <= mouseY < 465:
                    fila = 2

                if fila != -1 and columna != -1:
                    if tablero[fila][columna] == '':
                        tablero[fila][columna] = 'X'
                        primera_jugada = False
                        turno = 'O'
    else:
        time.sleep(2)
        if turno == 'X' and not game_over:
            if realizar_movimiento('X'):
                ganador = verificar_ganador(tablero)
                if ganador:
                    print(f"El jugador {ganador} ha ganado!!")
                    game_over = True
                elif tablero_lleno(tablero):
                    print("¡Es un empate!")
                    game_over = True
                turno = 'O'
        elif turno == 'O' and not game_over:
            if realizar_movimiento('O'):
                ganador = verificar_ganador(tablero)
                if ganador:
                    print(f"El jugador {ganador} ha ganado!!")
                    game_over = True
                elif tablero_lleno(tablero):
                    print("¡Es un empate!")
                    game_over = True
                turno = 'X'
    
    graficar_board()
    pygame.display.update()

pygame.quit()
