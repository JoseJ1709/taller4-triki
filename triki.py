import pygame

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
    #prueba

def verificar_ganador():
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != '':
            return True
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != '':
            return True 
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != '':
            return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != '':
            return True 
    return False


while not game_over:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos

            # Corrección de las condiciones para detección de clics
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
                    tablero[fila][columna] = turno
                    fin_juego = verificar_ganador()
                    if fin_juego:
                        print(f"El jugador {turno} ha ganado!!")
                        game_over = True
                    turno = 'O' if turno == 'X' else 'X'

    graficar_board()

    pygame.display.update()

pygame.quit()