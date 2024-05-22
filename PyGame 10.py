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
