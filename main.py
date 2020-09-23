# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 17:19:11 2020

@author: Antonio Muñoz Santiago

NOTAS:
- No se puede cambiar de bloque justo al borde del mapa, siempre será hierba.
- El movimiento del jugador al redimensionar la pantalla puede ser un futuro bug.
- Se debe hacer otra lista con los bloques que no se pueden traspasar (obstáculos).
- En la matriz de los objetos inmóviles se define la esquina inferior izquierda,
pero hay que especificar la posición desde la que se pintará la imagen (esquina
superior izquierda) y los bloques a añadir a la lista de obstáculos.
- Los NPCs irán en la lista level[1] como objetos.
"""

import pygame, sys, random
import pygame.event as GAME_EVENTS
import pygame.locals as GAME_GLOBALS
import pygame.time as GAME_TIME

import player #Archivo player.py
import stuff #Obstacles and NPCs

""" VARIABLES """

state = 'inGame'

#Variables de teclado
wPressed = False
sPressed = False
aPressed = False
dPressed = False

""" CONSTANTS """

WINDOW_WIDTH = 950
WINDOW_HEIGHT = 650
FPS = 60

sizeBlocks = 75 #Cada bloque del escenario será de 75x75 px.

#MATRIZ EN LA QUE SE DEFINEN LOS BLOQUES DE LA CAPA INFERIOR.

matrix = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

#MATRIZ EN LA QUE SE DEFINEN LOS BLOQUES DE LA CAPA SUPERIOR

matrix2 = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 2, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 2, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

#Constantes para clock
deltaTime = 0
lastTime = 0
multiplier = 1

""" PYGAME OBJECTS """

pygame.display.init()
pygame.mixer.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption('x')
clock = GAME_TIME.Clock()

player = player.player()

""" LOAD IMAGES """

mapBlocks = [
    pygame.image.load("assets/blocks/grass.png"), #0 Hierba
    pygame.image.load("assets/blocks/dirt/dirtCovered.png"), #1 Tierra rodeada de hierba
    pygame.image.load("assets/blocks/dirt/dirtCoveredUp.png"), #2 Tierra cubierta por arriba
    pygame.image.load("assets/blocks/dirt/dirtCoveredDown.png"), #3 Tierra cubierta por abajo
    pygame.image.load("assets/blocks/dirt/dirtCoveredLeft.png"), #4 Tierra cubierta por la izquierda
    pygame.image.load("assets/blocks/dirt/dirtCoveredRight.png"), #5 Tierra cubierta por la derecha
    pygame.image.load("assets/blocks/dirt/dirtCoveredUpLeft.png"), #6 Tierra cubierta por la esquina arriba-izquierda
    pygame.image.load("assets/blocks/dirt/dirtCoveredUpRight.png"), #7 Tierra cubierta por la esquina arriba-derecha
    pygame.image.load("assets/blocks/dirt/dirtCoveredDownLeft.png"), #8 Tierra cubierta por la esquina abajo-izquierda
    pygame.image.load("assets/blocks/dirt/dirtCoveredDownRight.png"), #9 Tierra cubierta por la esquina abajo-derecha
    pygame.image.load("assets/blocks/dirt/dirt.png"), #10 Tierra normal
    pygame.image.load("assets/blocks/dirt/dirtCornerUpLeft.png"), #11 Esquina de tierra arriba-izquierda
    pygame.image.load("assets/blocks/dirt/dirtCornerUpRight.png"), #12 Esquina de tierra arriba-derecha
    pygame.image.load("assets/blocks/dirt/dirtCornerDownLeft.png"), #13 Esquina de tierra abajo-izquierda
    pygame.image.load("assets/blocks/dirt/dirtCornerDownRight.png"), #14 Esquina de tierra abajo-derecha
    pygame.image.load("assets/blocks/flowers/white.png"), #15 Flores blancas (para poner en hierba)
]

""" GENERAL FUNCTIONS """

def quitGame(): #Se llama a esta función para parar la ejecución del juego.
    pygame.quit()
    sys.exit()

def get_neigbours(fil, col): #La función pide una coordenada de la matriz y devuelve el tipo de los bloques de alrededor
    #Devuelve los datos en formato [arriba, abajo, izquierda, derecha, esquina superior-izquierda, superior-derecha, inferior-izquierda, inferior-derecha]
    return [matrix[fil-1][col], matrix[fil+1][col], matrix[fil][col-1], matrix[fil][col+1],  matrix[fil-1][col-1], matrix[fil-1][col+1], matrix[fil+1][col-1], matrix[fil+1][col+1]]

def createLevel(): #Crea el escenario a partir de la matriz dada.
    pos = [0, 0] #x, y
    
    level = [] #Lista con la información de cada bloque.
    objects = [] #Lista con los objetos que hay en la superficie.
    
    for fil in range(len(matrix)):
        for col in range(len(matrix[fil])):
            toAddLayer2 = False #Seguirá siendo False si no se añade ningún nuevo objeto en la capa dos en esa casilla.
            
            #CAPA INFERIOR
            if matrix[fil][col] == 0: #Hierba
                image = mapBlocks[0]
            if matrix[fil][col] == 1: #Tierra, debemos comprobar la posición de los bloques de alrededor
                neigbours = get_neigbours(fil,col)
                #Tierra rodeada por hierba.
                if neigbours[0] == 0 and neigbours[1] == 0 and neigbours[2] == 0 and neigbours[3] == 0:
                    image = mapBlocks[1]
                #Tierra con hierba por arriba.
                if neigbours[0] == 0 and neigbours[1] == 1 and neigbours[2] == 1 and neigbours[3] == 1:
                    image = mapBlocks[2]
                #Tierra con hierba por abajo.
                if neigbours[0] == 1 and neigbours[1] == 0 and neigbours[2] == 1 and neigbours[3] == 1:
                    image = mapBlocks[3]
                #Tierra con hierba por la izquierda.
                if neigbours[0] == 1 and neigbours[1] == 1 and neigbours[2] == 0 and neigbours[3] == 1:
                    image = mapBlocks[4]
                #Tierra con hierba por la derecha.
                if neigbours[0] == 1 and neigbours[1] == 1 and neigbours[2] == 1 and neigbours[3] == 0:
                    image = mapBlocks[5]
                #Tierra con hierba por la esquina arriba-izquierda.
                if neigbours[0] == 0 and neigbours[1] == 1 and neigbours[2] == 0 and neigbours[3] == 1:
                    image = mapBlocks[6]
                #Tierra con hierba por la esquina arriba-derecha.
                if neigbours[0] == 0 and neigbours[1] == 1 and neigbours[2] == 1 and neigbours[3] == 0:
                    image = mapBlocks[7]
                #Tierra con hierba por la esquina abajo-izquierda.
                if neigbours[0] == 1 and neigbours[1] == 0 and neigbours[2] == 0 and neigbours[3] == 1:
                    image = mapBlocks[8]
                #Tierra con hierba por la esquina abajo-derecha.
                if neigbours[0] == 1 and neigbours[1] == 0 and neigbours[2] == 1 and neigbours[3] == 0:
                    image = mapBlocks[9]
                #Tierra normal (rodeada por más tierra).
                if neigbours[0] == 1 and neigbours[1] == 1 and neigbours[2] == 1 and neigbours[3] == 1 and neigbours[4] == 1 and neigbours[5] == 1 and neigbours[6] == 1 and  neigbours[7] == 1:
                    image = mapBlocks[10]
                #Esquina de tierra arriba-izquierda.
                if neigbours[0] == 1 and neigbours[1] == 1 and neigbours[2] == 1 and neigbours[3] == 1 and neigbours[4] == 0 and neigbours[5] == 1 and neigbours[6] == 1 and  neigbours[7] == 1:
                    image = mapBlocks[11]
                #Esquina de tierra arriba-derecha.
                if neigbours[0] == 1 and neigbours[1] == 1 and neigbours[2] == 1 and neigbours[3] == 1 and neigbours[4] == 1 and neigbours[5] == 0 and neigbours[6] == 1 and  neigbours[7] == 1:
                    image = mapBlocks[12]
                #Esquina de tierra abajo-izquierda.
                if neigbours[0] == 1 and neigbours[1] == 1 and neigbours[2] == 1 and neigbours[3] == 1 and neigbours[4] == 1 and neigbours[5] == 1 and neigbours[6] == 0 and  neigbours[7] == 1:
                    image = mapBlocks[13]
                #Esquina de tierra abajo-derecha.
                if neigbours[0] == 1 and neigbours[1] == 1 and neigbours[2] == 1 and neigbours[3] == 1 and neigbours[4] == 1 and neigbours[5] == 1 and neigbours[6] == 1 and  neigbours[7] == 0:
                    image = mapBlocks[14]
            if matrix[fil][col] == 2: #Flores blancas (para poner en hierba)
                image = mapBlocks[15]
            #CAPA SUPERIOR
            if matrix2[fil][col] == 1: #Árbol
                if matrix[fil][col] == 0: #Está en la hierba
                    toAddLayer2 = stuff.obstacle(sizeBlocks, 0, pos.copy())
            if matrix2[fil][col] == 2: #Arbusto (para poner en hierba)
                if matrix[fil][col] == 0:
                    toAddLayer2 = stuff.obstacle(sizeBlocks, 1, pos.copy())
            if matrix2[fil][col] == 3: #Arbusto rojo (para poner en hierba)
                if matrix[fil][col] == 0:
                    toAddLayer2 = stuff.obstacle(sizeBlocks, 2, pos.copy())
            if matrix2[fil][col] == 4: #Árbol cortado (para poner en hierba)
                if matrix[fil][col] == 0:
                    toAddLayer2 = stuff.obstacle(sizeBlocks, 3, pos.copy())
            if matrix2[fil][col] == 5: #Árbol cortado hueco (para poner en hierba, tierra o nieve)
                toAddLayer2 = stuff.obstacle(sizeBlocks, 4, pos.copy())
    
            level.append([image, pos[0], pos[1]])
            if toAddLayer2:
                objects.append(toAddLayer2) #Cada objeto, del que luego obtendremos la información con la función .get_info()
            pos[0] += sizeBlocks
        pos[0] = 0
        pos[1] += sizeBlocks
    
    return [level, objects]
                    
def moveMap(): #Para mover el mapa.
    global level, dPressed, aPressed, wPressed, sPressed
    if dPressed:
        for each in level[0]: #Objetos de la capa inferior
            each[1] -= player.get_vel()
        for each in level[1]: #Objetos de la capa superior
            each.move('right', player.get_vel())
        player.state('movingRight')
    if aPressed:
        for each in level[0]: #Objetos de la capa inferior
            each[1] += player.get_vel()
        for each in level[1]: #Objetos de la capa superior
            each.move('left', player.get_vel())
        player.state('movingLeft')
    if wPressed:
        for each in level[0]: #Objetos de la capa inferior
            each[2] += player.get_vel()
        for each in level[1]: #Objetos de la capa superior
            each.move('up', player.get_vel())
        player.state('movingUp')
    if sPressed:
        for each in level[0]: #Objetos de la capa inferior
            each[2] -= player.get_vel()
        for each in level[1]: #Objetos de la capa superior
            each.move('down', player.get_vel())
        player.state('movingDown')
    else: #Cuando no está pulsada ninguna tecla de movimiento.
        player.state('still')

def drawStage(): #Para pintar el escenario, será diferente dependiendo del state.
    global surface, level
    surface.fill((0,0,0))
    for each in level[0]:
        surface.blit(each[0], (each[1], each[2]))
        
    objectList = [] #Creamos una lista con la info de los objetos de la segunda capa para posteriormente añadir los objetos animados.
    for each in level[1]:
        objectList.append(each.get_info())
        #print(each.get_info())
    objectList.append(player.get_info(surface)) #Añadimos la info del jugador a la lista de objetos en la capa 2.
    #Esta lista deberá ordenarse constantemente para ver qué se pinta encima y debajo,
    #también se añadirán los demás objetos con movimiento.
    objectList.sort(key=lambda i : i[2] + i[3]) #Ordena la segunda capa dependiendo de la posy de la parte inferior de cada elemento (de mayor a menor).
    for each in objectList:
        surface.blit(each[0], (each[1], each[2]))
        
""" STATE FUNCTIONS """

def inGame():
    pass
    
""" MAIN LOOP """

level = createLevel() #Con esta línea se genera una lista donde level[0] será la capa inferior y level[1] la superior.

while True:
    drawStage()
    # Handle user and system events 
    for event in GAME_EVENTS.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                dPressed = True
            if event.key == pygame.K_a:
                aPressed = True
            if event.key == pygame.K_w:
                wPressed = True
            if event.key == pygame.K_s:
                sPressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                dPressed = False
            if event.key == pygame.K_a:
                aPressed = False
            if event.key == pygame.K_w:
                wPressed = False
            if event.key == pygame.K_s:
                sPressed = False
        if event.type == GAME_GLOBALS.QUIT:
            quitGame()
 
    if state == 'inGame' :
        moveMap() #Moverá la vista del jugador siempre que esté pulsada alguna tecla de movimiento
    
    clock.tick(FPS)
    deltaTime = GAME_TIME.get_ticks() - lastTime
    lastTime = GAME_TIME.get_ticks()
    multiplier = deltaTime * FPS * 1E-3
    pygame.display.update()