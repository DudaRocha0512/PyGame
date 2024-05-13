#----------------------------------------------------- TOCA DA RAPOSA -----------------------------------------------------#

# ----- Importa e inicia pacotes

import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange
import math

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
BRANCO = (255,255,255)

WIDTH = 1400
HEIGHT = 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TOCA DA RAPOSA')

pasta_geral = os.path.dirname(__file__)
imagens = os.path.join(pasta_geral, 'Imagens_Raposa')
#sons = os.path.join(pasta_geral, 'sons')

# ----- Recursos visuais e Funções

sprite_sheet = pygame.image.load(os.path.join(imagens, 'Raposas.png')).convert_alpha()

class Raposa(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        raposa1 = sprite_sheet.subsurface((332,0), (166,166))
        raposa2 = sprite_sheet.subsurface((0,332), (166,166))
        self.andando = [raposa1, raposa1, raposa2,raposa2]        
        self.index_lista = 0
        self.image = self.andando[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (120, 600)
        self.y_inicial = 600 - 166//2
        self.pulo = False
        #self.som.pulo = pygame.mixer.Sound(os.path.join(sons, 'Raposas.png'))
        
    def pular(self):
        self.pulo = True

    def update(self):
        if self.pulo == True:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 20
        else:
            if self.rect.y < self.y_inicial:
                self.rect.y += 20
            else:
                self.rect.y = self.y_inicial

        if self.index_lista > 3:
            self.index_lista = 0
        self.index_lista += 0.2
        self.image = self.andando[int(self.index_lista)]

Cen = pygame.image.load(os.path.join(imagens, 'Cenário Final 2.png')).convert()
t = 24
Cenario = pygame.transform.scale(Cen, (150*t, 30*t))

sprites = pygame.sprite.Group()
rapos = Raposa()
sprites.add(rapos)

movimento = 0
compri_cenario = Cenario.get_width()
repete = math.ceil(WIDTH/ compri_cenario) + 2
