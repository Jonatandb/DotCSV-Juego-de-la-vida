#
# https://github.com/Jonatandb/DotCSV-Juego-de-la-vida
#
import pygame, os
import numpy as np
import time

# Hago que la ventana aparezca centrada en Windows
os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()

# Establezco el título de la ventana:
pygame.display.set_caption("Juego de la vida - Jonatandb")

# Carga el icono si existe
iconPath = "./icono.ico"

if os.path.exists(iconPath):

    icono = pygame.image.load(iconPath)

    # Establece el icono de la ventana
    pygame.display.set_icon(icono)

# Defino ancho y alto de la ventana
width, height = 700, 700

# Creación de la ventana
screen = pygame.display.set_mode((height, width))

# Color de fondo, casi negro
bg = 25, 25, 25

# Pinto el fondo con el color elegido (bg)
screen.fill(bg)

# Cantidad de celdas en cada eje
nxC, nyC = 50, 50

# Ancho y alto de cada celda
dimCW = width / nxC
dimCH = height / nyC

# Estructura de datos que contiene todos los estados de las diferentes celdas
# Estados de las celdas: Vivas = 1 - Muertas = 0
# Inicializo matriz con ceros
gameState = np.zeros((nxC, nyC))

# Autómata palo:
# 0 1 0
# 0 1 0
# 0 1 0
# gameState[5, 3] = 1
# gameState[5, 4] = 1
# gameState[5, 5] = 1

# Autómata móvil:
# 0 1 0
# 0 0 1
# 1 1 1
# gameState[21, 21] = 1
# gameState[22, 22] = 1
# gameState[22, 23] = 1
# gameState[21, 23] = 1
# gameState[20, 23] = 1

# Autómata Jonatandb :)
# 1 1 1
# 0 0 1
# 1 0 1
# 1 1 1
# gameState[10, 10] = 1
# gameState[11, 10] = 1
# gameState[12, 10] = 1
# gameState[12, 11] = 1
# gameState[10, 12] = 1
# gameState[12, 12] = 1
# gameState[10, 13] = 1
# gameState[11, 13] = 1
# gameState[12, 13] = 1

# Versión de mi autómata que siempre aparece centrada: Autómata Jonatandb :)
posInitX = int((nxC / 2) - 3)
posInitY = int((nyC / 2) - 4)
gameState[posInitX, posInitY] = 1
gameState[posInitX + 1, posInitY] = 1
gameState[posInitX + 2, posInitY] = 1
gameState[posInitX + 2, posInitY + 1] = 1
gameState[posInitX, posInitY + 2] = 1
gameState[posInitX + 2, posInitY + 2] = 1
gameState[posInitX, posInitY + 3] = 1
gameState[posInitX + 1, posInitY + 3] = 1
gameState[posInitX + 2, posInitY + 3] = 1

# Control de la ejecución - En True se inicia pausado (Para poder ver la forma inicial de los aútomatas):
pauseExec = True

# Controla si se debe pausar un segundo por iteración:
pauseOneSec = False

# Controla la finalización del juego:
endGame = False

# Bucle de ejecución principal (Main Loop):
while not endGame:

    newGameState = np.copy(gameState)

    # Vuelvo a colorear la pantalla con el color de fondo
    screen.fill(bg)

    # Agrego pequeña pausa para que el cpu no trabaje al 100%
    time.sleep(0.1)

    # Registro de eventos de teclado y mouse
    ev = pygame.event.get()

    for event in ev:

        # Si cierran la ventana finalizo el juego
        if event.type == pygame.QUIT:
            endGame = True

        # Si tocan una tecla pauso / reanudo el juego
        if event.type == pygame.KEYDOWN:
            pauseExec = not pauseExec

        # Detección de click del mouse:
        mouseClick = pygame.mouse.get_pressed()

        # Obtención de posición del cursor en la pantalla:
        # Si se hace click con cualquier botón del mouse, se obtiene un valor en mouseClick mayor a cero
        if sum(mouseClick) > 0:

            # Click del medio pausa / reanuda el juego
            if mouseClick[1]:

                pauseExec = not pauseExec

            else:

                # Obtengo las coordenadas del cursor del mouse en pixeles
                posX, posY, = pygame.mouse.get_pos()

                # Convierto de coordenadas en pixeles a celda clickeada en la grilla
                celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))

                # Click izquierdo y derecho permutan entre vida y muerte
                newGameState[celX, celY] = not gameState[celX, celY]

    # Recorro cada una de las celdas generadas
    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExec:

                # Cálculo del número de vecinos cercanos
                n_neigh = (
                    gameState[(x - 1) % nxC, (y - 1) % nyC]
                    + gameState[x % nxC, (y - 1) % nyC]
                    + gameState[(x + 1) % nxC, (y - 1) % nyC]
                    + gameState[(x - 1) % nxC, y % nyC]
                    + gameState[(x + 1) % nxC, y % nyC]
                    + gameState[(x - 1) % nxC, (y + 1) % nyC]
                    + gameState[x % nxC, (y + 1) % nyC]
                    + gameState[(x + 1) % nxC, (y + 1) % nyC]
                )

                # Regla 1: Una célula muerta con exactamente 3 vecinas vivas: "revive"
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Regla 2: Una célula viva con menos de 2 o más de 3 vecinas vivas : "muere"
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Creación del polígono de cada celda a dibujar
            poly = [
                (int(x * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int((y + 1) * dimCH)),
                (int(x * dimCW), int((y + 1) * dimCH)),
            ]

            if newGameState[x, y] == 0:
                # Dibujado de la celda para cada par de x e y:
                # screen          -> Pantalla donde dibujar
                # (128, 128, 128) -> Color a utilizar para dibujar, en este caso un gris
                # poly            -> Puntos que definan al poligono que se está dibujando
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                if pauseExec:
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 0)
                else:
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizo gameState
    gameState = np.copy(newGameState)

    # Muestro y actualizo los fotogramas en cada iteración del bucle principal
    pygame.display.flip()

    if pauseOneSec:

        time.sleep(1)
