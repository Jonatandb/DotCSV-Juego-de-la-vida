import pygame
import numpy as np

pygame.init()

# Ancho y alto de la pantalla
width, height = 1000, 1000

# Creación de la pantalla
screen = pygame.display.set_mode((height, width))

# Color de fondo, casi negro
bg = 25, 25, 25

# Pinto el fondo con el color elegido (bg)
screen.fill(bg)

# Cantidad de celdas en cada eje
nxC, nyC = 25, 25

# Ancho y alto de cada celda
dimCW = width / nxC
dimCH = height / nyC

# Bucle de ejecución principal (Main Loop)
while True:

    # Recorro cada una de las celdas generadas
    for y in range(0, nxC):
        for x in range(0, nyC):

            poly = [
                ((x) * dimCW, y * dimCH),
                ((x + 1) * dimCW, y * dimCH),
                ((x + 1) * dimCW, (y + 1) * dimCH),
                ((x) * dimCW, (y + 1) * dimCH),
            ]

            # screen          -> Pantalla donde dibujar
            # (128, 128, 128) -> Color a utilizar para dibujar, en este caso un gris
            # poly            -> Puntos que definan al poligono que se está dibujando
            pygame.draw.polygon(screen, (128, 128, 128), poly, 1)

    # Muestro y actualizo los fotogramas en cada iteración del bucle principal
    pygame.display.flip()
