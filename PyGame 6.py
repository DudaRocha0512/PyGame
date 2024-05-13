#----------------------------------------------------- TOCA DA RAPOSA -----------------------------------------------------#

# ----- Importa e inicia pacotes

import pygame
from pygame.locals import *
from sys import exit
import os
import random
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

game_over = pygame.image.load(os.path.join(imagens, 'Raposas.png')).convert()
maior_prontuacao = 0
ponts = 0

def Pontuacao(texto,tamnanho,cor):   # Texto de Score
    fonte = pygame.font.SysFont('comicSanssms', tamnanho, True, False)
    texto_msg = f'{texto}'
    texto_final = fonte.render(texto_msg, True, cor)
    return texto_final

class Raposa(pygame.sprite.Sprite):    # Imagens da Raposa
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        raposa1 = sprite_sheet.subsurface((332,0), (166,166))
        raposa2 = sprite_sheet.subsurface((0,332), (166,166))
        self.andando = [raposa1, raposa1, raposa2,raposa2]        
        self.index_lista = 0
        self.image = self.andando[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (400, 600)
        self.y_inicial = 600 - 166//2
        self.pulo = False
        #self.som.pulo = pygame.mixer.Sound(os.path.join(sons, 'Raposas.png'))
        
    def pular(self):    # Pulo da Raposa
        self.pulo = True

    def update(self):
        if self.pulo == True:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 20   # Altura do Pulo
        else:
            if self.rect.y < self.y_inicial:
                self.rect.y += 20
            else:
                self.rect.y = self.y_inicial

        if self.index_lista > 3:
            self.index_lista = 0
        self.index_lista += 0.2
        self.image = self.andando[int(self.index_lista)]


class Obstaculos(pygame.sprite.Sprite):   # Imagens dos Obstáculos
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        arb1 = pygame.image.load(os.path.join(imagens, 'Arbusto 1.png')).convert_alpha()
        arbusto1 = pygame.transform.scale(arb1, (245//2,215//2))

        arb2 = pygame.image.load(os.path.join(imagens, 'Arbusto 2.png')).convert_alpha()
        arbusto2 = pygame.transform.scale(arb2, (177//1.2,237//1.2))

        arb3 = pygame.image.load(os.path.join(imagens, 'Arbusto 3.png')).convert_alpha()
        arbusto3 = pygame.transform.scale(arb3, (214//1.2,148//1.2))

        arb4 = pygame.image.load(os.path.join(imagens, 'Arbusto 4.png')).convert_alpha()
        arbusto4 = pygame.transform.scale(arb4, (233//1.5,211//1.5))        

        p1 = pygame.image.load(os.path.join(imagens, 'Pedras 1.png')).convert_alpha()
        pedra1 = pygame.transform.scale(p1, (7946//50,5036//50))  

        p2 = pygame.image.load(os.path.join(imagens, 'Pedras 2.png')).convert_alpha()
        pedra2 = pygame.transform.scale(p2, (7378//50,5282//50))  

        self.obstaculos = [arbusto1, arbusto2, arbusto3, arbusto4, pedra1, pedra2]  
        ind_obs = [0,1,2,3,4,5]      
        #sorteio = random.choice(ind_obs)
        #self.index_lista = sorteio
        self.image = self.obstaculos[random.choice(ind_obs)]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (1400, 600)      

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = 1400
        
        self.rect.x -= 10
    

Cen = pygame.image.load(os.path.join(imagens, 'Cenário Final 2.png')).convert()
t = 24
Cenario = pygame.transform.scale(Cen, (150*t, 30*t))

sprites = pygame.sprite.Group()
rapos = Raposa()
sprites.add(rapos)

movimento = 0
compri_cenario = Cenario.get_width()
repete = math.ceil(WIDTH/ compri_cenario) + 2

obs = Obstaculos()
sprites.add(obs)

todos_obstaculos = pygame.sprite.Group()
todos_obstaculos.add(obs)

# ----- Loop Principal
FPS = pygame.time.Clock()
aceleracao = 0
r = True
while r == True:
    FPS.tick(30 + aceleracao)

    for i in range(-1, repete + 1):
        window.blit(Cenario, (i * compri_cenario + movimento % compri_cenario, 0))


    if abs(movimento) > compri_cenario:
        movimento = 0


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if rapos.rect.y != rapos.y_inicial:
                    pass
                else:
                    rapos.pular()
                
    
    colisao = pygame.sprite.spritecollide(rapos,todos_obstaculos, False, pygame.sprite.collide_mask)

    sprites.draw(window)

    if colisao:
        if ponts > maior_prontuacao:
            maior_prontuacao = ponts    # Recorde
            recorde = Pontuacao(f'Recorde: {maior_prontuacao}', 45, (225, 0, 0))
        window.blit(recorde, (1175,80))

    else:
        ponts += 1
        sprites.update()
        pontuacao_txt = Pontuacao(f'Score: {ponts}', 45, (225, 0, 0))   # Pontuação

        #aceleracao += 0.05
        movimento -= 10

    if ponts % 250 == 0:
        aceleracao += 5

    window.blit(pontuacao_txt, (1200,50))

    pygame.display.flip()
