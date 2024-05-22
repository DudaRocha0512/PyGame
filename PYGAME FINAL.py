#----------------------------------------------------- TOCA DA RAPOSA -----------------------------------------------------#

# ----- Importa e inicia pacotes

import pygame
from pygame.locals import *
from sys import exit
import os
import random
import math
from menu import *

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
WIDTH = 1400
HEIGHT = 700
WINDOW_SIZE = (WIDTH, HEIGHT)
FPS_menu = 3
RED = (255, 0, 0)
ORANGE = (220,127,4)

lista_pontos = []

# Função principal do jogo
def TOCA_DA_RAPOSA():
    
    # inicialização da Tela
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('TOCA DA RAPOSA')
    pasta_geral = os.path.dirname(__file__)
    imagens = os.path.join(pasta_geral, 'Imagens_Raposa')

    # ----- Recursos visuais e Funções dentro do jogo
    # Carrega as imagens do menu
    img1 = pygame.image.load('imagem1.png').convert()
    imagem1 = pygame.transform.scale(img1, (1400,700))
    img2 = pygame.image.load('imagem2.png').convert()
    imagem2 = pygame.transform.scale(img2, (1400,700))
    current_image = imagem1  # Começa com a primeira imagem
    

    # Função para alternar entre as imagens do menu
    def alternar_imagem_menu():
        nonlocal current_image
        if current_image == imagem1:
            current_image = imagem2
        else:
            current_image = imagem1

    # Função para desenhar o menu na tela
    def desenhar_menu():
        window.blit(current_image, (0, 0))

    sprite_sheet = pygame.image.load(os.path.join(imagens, 'Raposas.png')).convert_alpha()
    go = pygame.image.load('game_over.jpeg').convert()
    game_over = pygame.transform.scale(go, (1400,700))
    maior_prontuacao = 0

    # Pontuação
    def Pontuacao(texto,tamanho,cor):   # Texto de Score (Pontuação)
        fonte = pygame.font.SysFont('arial', tamanho, True, False)
        texto_msg = f'{texto}'
        texto_final = fonte.render(texto_msg, True, cor)
        return texto_final
    
    # Finalização
    def Final(texto,tamanho,cor):   # Texto de Score (Pontuação)
        fonte = pygame.font.SysFont('arial', tamanho, True, False)
        texto_msg = f'{texto}'
        texto_final = fonte.render(texto_msg, True, cor)
        return texto_final                

    # Imagens da Raposa
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
            
        def pular(self):    # Pulo da Raposa
            self.pulo = True

        def update(self):
            if self.pulo == True:
                if self.rect.y <= 200:
                    self.pulo = False
                self.rect.y -= 15   # Altura do Pulo
            else:
                if self.rect.y < self.y_inicial:
                    self.rect.y += 20
                else:
                    self.rect.y = self.y_inicial

            if self.index_lista > 3:
                self.index_lista = 0
            self.index_lista += 0.2
            self.image = self.andando[int(self.index_lista)]

    # Obstáculos da Raposa
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
            #self.index_lista = sorteio
            for _ in ind_obs:
                sorteio = random.choice(ind_obs)
                self.image = self.obstaculos[sorteio]
                self.rect = self.image.get_rect()
                self.mask = pygame.mask.from_surface(self.image)
                self.rect.center = (1400, 600)      

        def update(self):
            if self.rect.topright[0] < 0:
                self.rect.x = 1400
            
            self.rect.x -= 10
        
    # Cenário de Fundo do Jogo
    Cen = pygame.image.load(os.path.join(imagens, 'Cenário Final 2.png')).convert()
    t = 24
    Cenario = pygame.transform.scale(Cen, (150*t, 30*t))

    sprites = pygame.sprite.Group()
    rapos = Raposa()
    sprites.add(rapos)

    # Movimentação do Fundo
    movimento = 0
    compri_cenario = Cenario.get_width()
    repete = math.ceil(WIDTH/ compri_cenario) + 2

    obs_inicial = 0
    obs_novo = obs_inicial + 1

    if obs_novo != obs_inicial:
        # Inserção dos obstáculos
        obs = Obstaculos()
        sprites.add(obs)
        todos_obstaculos = pygame.sprite.Group()
        todos_obstaculos.add(obs)

    # Repetição do Jogo
    reinicia = False
    ponts = 0
    aceleracao = 0

    # ---- LOOP INICIAL
    menu_visible = True
    clock = pygame.time.Clock()

    # Música
    musica = pygame.mixer.music.load('madagascar pygame.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    

    while True:
        clock.tick(FPS_menu)

        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Inicia o jogo quando Enter é pressionado
                    menu_visible = False

        # Desenha o menu
        if menu_visible:
            desenhar_menu()

            # Alterna entre as imagens do menu enquanto o jogo não começa
            alternar_imagem_menu()

            # ---- LOOP PRINCIPAL - INICIA O JOGO PÓS MENU
        else:
            FPS = pygame.time.Clock()
            aceleracao = 0
            r = True  

            while r:
                # Velocidade
                FPS.tick(50 + aceleracao)

                # Repetição do cenário
                for i in range(-1, repete + 1):
                    window.blit(Cenario, (i * compri_cenario + movimento % compri_cenario, 0))

                if abs(movimento) > compri_cenario:
                    movimento = 0

                for event in pygame.event.get():
                    if event.type == QUIT:   # Encerramento do jogo (X)
                        pygame.quit()
                        exit()

                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:   # Pulo
                            if rapos.rect.y != rapos.y_inicial:
                                pass
                            else:
                                rapos.pular()   

                        if event.key == pygame.K_r and reinicia == True:   # Reinicia o Jogo 
                            ponts = 0
                            aceleracao = 0
                            movimento = 0
                            rapos.rect.y = 600
                            rapos.pulo = False
                            obs.rect.center = (1400, 600) 
                            reinicia = False
                            break

                        if event.key == pygame.K_s and reinicia == True:    # Volta ao Menu
                            TOCA_DA_RAPOSA()     
                                        
                # Detector de colisão
                colisao = pygame.sprite.spritecollide(rapos,todos_obstaculos, False, pygame.sprite.collide_mask)

                sprites.draw(window)

                if colisao:
                    reinicia = True
                    lista_pontos.append(ponts)

                    # Game Over e Continuar
                    window.blit(game_over, (0,0))

                    pergunta = Final(f'DESEJA CONTINUAR?', 35, (225, 225, 225))
                    pygame.draw.rect(window, ORANGE, (900, 530, 472, 125))
                    window.blit(pergunta, (950,550))

                    opcao = Final(f'Pressione R para reiniciar ou S para sair', 20, (225, 0, 0))
                    window.blit(opcao, (950,610))

                    maior_prontuacao = max(lista_pontos)  # Recorde
                    recorde = Pontuacao(f'Recorde: {maior_prontuacao:.0f}', 30, (225, 0, 0))
                    window.blit(recorde, (1180,100))

                else:
                    # Pontuação
                    ponts += 0.5
                    sprites.update()
                    pontuacao_txt = Pontuacao(f'SCORE: {ponts:.0f}', 29, (225, 225, 225))   # Pontuação

                    movimento -= 10

                # Aumenta a velocidade a cada 250 pontos
                if ponts % 150 == 0:
                    aceleracao += 5

                # Exibe a pontuação
                pygame.draw.rect(window, ORANGE, (1180, 30, 205, 60))
                window.blit(pontuacao_txt, (1190,45))
                

                pygame.display.flip()

        # Atualiza a tela - mudanças
        pygame.display.flip()

# Chamada da Função (Jogo)
if __name__ == "__main__":
    TOCA_DA_RAPOSA()
