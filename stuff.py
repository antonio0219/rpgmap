# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 13:28:48 2020

@author: anton

En este archivo estará la clase obstacle y la clase npc y enemy.

Necesito que en level[1] en vez de meter una lista con la información de cada
objeto se meta directamente un objeto que tenga una función .get_info que sea
llamada a cada frame y que devuelva la misma información que se requiere.

La ventaja de esto es que será posible cambiar de imágenes para poder animar
el escenario y que será más fácil definir los bloques por los que no se podrá
pasar. Para ello es necesario pasarle a cada objeto las coordenadas donde está
ubicado.

Se debe especificar el tiempo que va a tardar cada objeto en cambiar de disfraz
como norma general.
"""

import pygame
import pygame.time as GAME_TIME

class obstacle:
    def __init__(self, sizeBlocks, kind, pos, time = 500):
        self.pos = pos #Será una lista con las coordenadas [x,y]
        self.sizeBlocks = sizeBlocks
        self.time = time #El tiempo entre cada imagen. Si no se define tendrá un valor por defecto.
        
        #Lista con los datos de cada tipo de objeto [height, images]
        self.data = [
            [self.sizeBlocks*2, pygame.image.load("assets/layer2/tree.png")], #0 Árbol en hierba
            [self.sizeBlocks, pygame.image.load("assets/layer2/shrubbery/bash.png")], #1 Arbusto normal (para poner en hierba)
            [self.sizeBlocks, pygame.image.load("assets/layer2/shrubbery/red.png")], #2 Arbusto rojo (para poner en hierba)
            [self.sizeBlocks, pygame.image.load("assets/layer2/cutTree.png")], #3 Árbol cortado (para poner en hierba)
            [self.sizeBlocks, pygame.image.load("assets/layer2/cutTreeDirt.png")], #4 Árbol cortado 2 (para poner en hierba o tierra)
        ]
        
        self.info = self.data[kind] #Definimos la altura e imágenes de cada objeto.
        
    def move(self, direction, vel): #Función para mover cada objeto con respecto al escenario.
        if direction == 'right':
            self.pos[0] -= vel
        if direction == 'left':
            self.pos[0] += vel
        if direction == 'up':
            self.pos[1] += vel
        if direction == 'down':
            self.pos[1] -= vel
            
    def get_info(self): #Función que devuelve [image, pos[0], pos[1], height]
        #Pinta cada objeto desde la esquina superior izquierda.
        return [self.info[1], self.pos[0], self.pos[1]-self.info[0]+self.sizeBlocks, self.info[0]]
