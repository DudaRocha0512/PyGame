# ----- Loop Principal
FPS = pygame.time.Clock()
aceleracao = 0
while True:
    FPS.tick(30 + aceleracao)

    for i in range(-1, repete + 1):
        window.blit(Cenario, (i * compri_cenario + movimento % compri_cenario, 0))

    movimento -= 10

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
    
    aceleracao += 0.01

    sprites.draw(window)
    sprites.update()

    pygame.display.flip()
