# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 17:03:38 2020

@author: anton
"""

import pygame
import pygame.time as GAME_TIME

class player:
    def __init__(self):
        #self.x = xo Más adelante se podrá definir la posición.
        #self.y = yo
        
        self.height = 75
        
        self.vel = 5 #Píxeles que se mueve por segundo
        self.stepMoment = GAME_TIME.get_ticks() # Coge el instante actual para cambiar de postura andando o quieto.
        self.lastDirection = 'right' #La última posición que tenía
        
        self.brake = 2 #Potencia de los frenos, los píxeles/frame que reduce.
        
        self.images = [
                pygame.image.load("assets/player/oldMan/right.png"), #0
                pygame.image.load("assets/player/oldMan/right2.png"), #1
                pygame.image.load("assets/player/oldMan/left.png"), #2
                pygame.image.load("assets/player/oldMan/left2.png"), #3
                pygame.image.load("assets/player/oldMan/walkingRight1.png"), #4
                pygame.image.load("assets/player/oldMan/walkingRight2.png"), #5
                pygame.image.load("assets/player/oldMan/walkingLeft1.png"), #6
                pygame.image.load("assets/player/oldMan/walkingLeft2.png"), #7
            ]
        
        self.imageToDraw = self.images[0] #La imagen a dibujar en cada frame
    
    def state(self, info): #Estado en el que se encuentra (ej. moviéndose a la derecha, atacando...)
        if info == 'movingRight':
            self.lastDirection = 'right'
            if GAME_TIME.get_ticks() - self.stepMoment >= 60:
                if self.imageToDraw == self.images[4]:
                    self.imageToDraw = self.images[5]
                else:
                    self.imageToDraw = self.images[4]
                self.stepMoment = GAME_TIME.get_ticks()
        if info == 'movingLeft':
            self.lastDirection = 'left'
            if GAME_TIME.get_ticks() - self.stepMoment >= 60:
                if self.imageToDraw == self.images[6]:
                    self.imageToDraw = self.images[7]
                else:
                    self.imageToDraw = self.images[6]
                self.stepMoment = GAME_TIME.get_ticks()
        if info == 'still':
            if GAME_TIME.get_ticks() - self.stepMoment >= 200:
                if self.lastDirection == 'right':
                    if self.imageToDraw == self.images[0]:
                        self.imageToDraw = self.images[1]
                    else:
                        self.imageToDraw = self.images[0]
                if self.lastDirection == 'left':
                    if self.imageToDraw == self.images[2]:
                        self.imageToDraw = self.images[3]
                    else:
                        self.imageToDraw = self.images[2]
                self.stepMoment = GAME_TIME.get_ticks()
                
    def get_vel(self):
        return self.vel
    
    def get_info(self, surface): #Función que devuelve [image, pos[0], pos[1], height]
        return [self.imageToDraw, surface.get_width()/2, surface.get_height()/2, self.height]