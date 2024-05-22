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
