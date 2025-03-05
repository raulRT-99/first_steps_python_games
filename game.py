# Example file showing a basic pygame "game loop"
import pygame
import random
import bloques
import config as cfg
import time

class game():

    def mapPowerUpsTiempo():
        mapa = dict()
        for item in cfg.PowerUpsEnum:
            mapa[item]=0.0
        for item in cfg.PowerDownsEnum:
            mapa[item]=0.0
        return mapa

    def run(hardcore):
        
        # pygame
        pygame.init()
        pygame.display.set_caption("Brick Ball")
        screen = pygame.display.set_mode((1160, 650))
        clock = pygame.time.Clock()
        running = True

        #imagenes
        # cargamos el fondo y una imagen (se crea objetos "Surface")
        fondo = pygame.image.load("images\\fondo.png").convert()        

        #Sonido
        barraSound = pygame.mixer.Sound('sounds\\star.wav')
        barraSound.set_volume(0)
        #barraSound.set_volume(.5)
        bloqueSound = pygame.mixer.Sound('sounds\\block.mp3')
        #bloqueSound.set_volume(.6)
        bloqueSound.set_volume(0)
        PUSound = pygame.mixer.Sound('sounds\\goodBlock.mp3')
        #PUSound.set_volume(.5)
        PUSound.set_volume(0)
        PDSound = pygame.mixer.Sound('sounds\\badBlock.mp3')
        #PDSound.set_volume(.5)
        PDSound.set_volume(0)
        winSound = pygame.mixer.Sound('sounds\\win.mp3')
        #winSound.set_volume(.75)
        winSound.set_volume(0)
        loseSound = pygame.mixer.Sound('sounds\\lose.mp3')
        #loseSound.set_volume(.17)
        loseSound.set_volume(0)
        pygame.mixer.music.load('sounds\\music.mp3')
        #pygame.mixer.music.set_volume(1)
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play(-1, 0.0)
        
        #bola
        ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        ball_movX = True
        ball_movY = True
        ballX = 0
        ballY = 2
        lento = (195,252,252)
        normal = "white"
        rapido = (190,0,0)
        superPU = (247,220,0)

        #barra
        dt=4
        IzqIzqBarradt = -2
        IzqBarradt = -1
        DerBarradt = 1
        DerDerBarradt = 2
        cordsRect = pygame.Vector2((screen.get_width() / 2) - 120, 610)
        barra = 120

        #in-game
        FPS = 120
        win = -1
        WinLose = False
        diffuculty = 0
        config = cfg.Configuraciones
        bordeX = 1160
        bordeY = 650
        golpes= 0
        nivel = 1
        puntuacion = 0
        velocidad=FPS
                
        #bloques
        dibujado = False
        blockValid = bloques.Validaciones
        block = bloques.Bloque
        cordsBlocks, cordsBlocksKill, goodPU, badPU = blockValid.coordsBloques(nivel)
        
        #power-ups
        pu = ""
        powerUps, powerDowns = config.arrPowerUps()
        enumPU = cfg.PowerUpsEnum
        enumPD = cfg.PowerDownsEnum
        tiempoPU = 3
        tiempoPUMap = game.mapPowerUpsTiempo()
        powerUpsList = powerUps
        powerUpsList.extend(powerDowns)

        #lista-powerups
        velPU = 0
        tamBarraPU = 0
        inverso = False
        Super = False
        barraUp = 0
        

        while running:
            
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # fill the screen with a color to wipe away anything from last frame
            screen.blit(fondo, (0, 0))

            colorBola = normal

            if Super:
                colorBola = superPU
            elif velPU >0:
                colorBola = rapido
            elif velPU <0:
                colorBola=lento

            pygame.draw.circle(screen, colorBola, ball_pos, 7)

            
            cordsBlockXY, cordsPU = block.dibujar(screen, cordsBlocks, cordsBlocksKill, goodPU, badPU)

            ball_pos.x, ball_pos.y = blockValid.golpeoY(ball_movY,ball_pos,bordeY,ballX,ballY)

            ballX,ball_movX = blockValid.golpeoX(ball_movX, ball_pos, bordeX, ballX)

            ### GOLPEA BARRA
            if ball_pos.x >= cordsRect.x and ball_pos.x <= cordsRect.x + (barra + tamBarraPU) and ball_pos.y <= bordeY - 30 - barraUp and ball_pos.y >= bordeY - 45 - barraUp:
                intervalo = (barra + tamBarraPU)/5
                if ball_pos.x >= cordsRect.x and ball_pos.x <= cordsRect.x + intervalo:
                    ballX = IzqIzqBarradt
                    ball_movX = False
                elif ball_pos.x >= cordsRect.x + intervalo and ball_pos.x <= cordsRect.x + intervalo*2:
                    ballX = IzqBarradt
                    ball_movX = False
                elif ball_pos.x >= cordsRect.x + intervalo*2 and ball_pos.x <= cordsRect.x + intervalo*3:
                    ballX = random.choice((IzqBarradt,0,DerBarradt))
                    ball_movX = True
                elif ball_pos.x >= cordsRect.x + intervalo*3 and ball_pos.x <= cordsRect.x + intervalo*4:
                    ballX = DerBarradt
                    ball_movX = True
                elif ball_pos.x >= cordsRect.x + intervalo*4 and ball_pos.x <= cordsRect.x + intervalo*5:
                    ballX = DerDerBarradt
                    ball_movX = True
                golpes += 1
                ball_movY = not ball_movY
                diffuculty = config.dificultad(golpes,diffuculty)
                barraSound.play()
            elif ball_pos.y <= 7:
                if ball_pos.y <= 5:
                    ball_pos.y = 5
                ball_movY = not ball_movY
            

            ### GOLPEA BLOQUE 
            for cordBlock in cordsBlockXY:
                XcordB, YcordB = cordBlock
                XB = XcordB/115
                YB = (YcordB - 5)/32
                if cordsBlocksKill.get((XB,YB)):
                   
                    pu = block.bloquePU((XcordB,YcordB), cordsPU)
                    #abajo
                    if ball_pos.x >= XcordB and ball_pos.x <= XcordB + 100 and ball_pos.y <= YcordB +31 and ball_pos.y >= YcordB +29:
                        if not Super:
                            ball_movY = not ball_movY
                        cordsBlocksKill[(XB,YB)] = False
                        tamBarraPU,velPU,tipoBloque,inverso,Super,barraUp = blockValid.golpePU(pu,enumPU,enumPD,tamBarraPU,velPU,inverso,Super,barraUp)
                        if tipoBloque == 0:
                            tiempoPUMap[pu] = time.process_time()
                            PUSound.play()
                        elif tipoBloque == 1:
                            tiempoPUMap[pu] = time.process_time()
                            PDSound.play()
                        else:
                            bloqueSound.play()

                        puntuacion+=1
                        break
                    #arriba
                    elif ball_pos.x >= XcordB and ball_pos.x <= XcordB + 100 and ball_pos.y >= YcordB -1 and ball_pos.y <= YcordB + 1:
                        if not Super:
                            ball_movY = not ball_movY
                        cordsBlocksKill[(XB,YB)] = False
                        tamBarraPU,velPU,tipoBloque,inverso,Super,barraUp = blockValid.golpePU(pu,enumPU,enumPD,tamBarraPU,velPU,inverso,Super,barraUp)
                        if tipoBloque == 0:
                            tiempoPUMap[pu] = time.process_time()
                            PUSound.play()
                        elif tipoBloque == 1:
                            tiempoPUMap[pu] = time.process_time()
                            PDSound.play()
                        else:
                            bloqueSound.play()
                        puntuacion+=1
                        break
                    #izquierda
                    elif ball_pos.x >= XcordB -1 and ball_pos.x <= XcordB + 1 and ball_pos.y <= YcordB +30 and ball_pos.y >= YcordB:
                        if not Super:
                            ballX = ballX*-1
                            ball_movX = not ball_movX
                        cordsBlocksKill[(XB,YB)] = False
                        tamBarraPU,velPU,tipoBloque,inverso,Super,barraUp = blockValid.golpePU(pu,enumPU,enumPD,tamBarraPU,velPU,inverso,Super,barraUp)
                        if tipoBloque == 0:
                            tiempoPUMap[pu] = time.process_time()
                            PUSound.play()
                        elif tipoBloque == 1:
                            tiempoPUMap[pu] = time.process_time()
                            PDSound.play()
                        else:
                            bloqueSound.play()
                        puntuacion+=1
                        break
                    #derecha
                    elif ball_pos.x >= XcordB + 99 and ball_pos.x <= XcordB + 101 and ball_pos.y <= YcordB +31 and ball_pos.y >= YcordB +29:
                        if not Super:
                            ballX = ballX*-1
                            ball_movX = not ball_movX
                        cordsBlocksKill[(XB,YB)] = False
                        tamBarraPU,velPU,tipoBloque,inverso,Super,barraUp = blockValid.golpePU(pu, enumPU,enumPD,tamBarraPU,velPU,inverso,Super,barraUp)
                        if tipoBloque == 0:
                            tiempoPUMap[pu] = time.process_time()
                            PUSound.play()
                        elif tipoBloque == 1:
                            tiempoPUMap[pu] = time.process_time()
                            PDSound.play()
                        else:
                            bloqueSound.play()
                        puntuacion+=1
                        break

            
            for puMap in powerUpsList:
                if (time.process_time() - tiempoPUMap.get(puMap)) >= tiempoPU and tiempoPUMap.get(puMap) >0:
                    tiempoPUMap[puMap] = 0
                    velPU,tamBarraPU,inverso,Super,barraUp = blockValid.resetPU(puMap,velPU,tamBarraPU,enumPU,enumPD,inverso,Super,barraUp)

                    

            pygame.draw.rect(screen, (0,0,0) if not inverso else (174,63,165), ((cordsRect.x,cordsRect.y - barraUp), (barra + tamBarraPU,15)), 0,3)

            keys = pygame.key.get_pressed()

            keyA = keys[pygame.K_a] or keys[pygame.K_LEFT]
            keyD = keys[pygame.K_d] or keys[pygame.K_RIGHT]

            if inverso:
                if keyD and cordsRect.x > 5:
                    cordsRect.x -= dt
                elif keyA and cordsRect.x < bordeX - (barra + tamBarraPU):
                    cordsRect.x += dt
            else:
                if keyA and cordsRect.x > 5:
                    cordsRect.x -= dt
                elif keyD and cordsRect.x < bordeX - (barra + tamBarraPU):
                    cordsRect.x += dt

            for boolCord in cordsBlocksKill:
                if not cordsBlocksKill.get(boolCord):
                    win =1
                else:
                    win = -1
                    break

            if ball_pos.y >= 650:
                win = 0
                    

            if win >= 0:
                ganador = "Felicidades, terminaste el " + (" nivel "+ str(nivel) ) if nivel<10 else "ultimo nivel!!"
                perdedor = "Perdiste, el juego te ah superado"
                texto = pygame.font.SysFont("Arial", 50)
                imagenTextoPresent = texto.render(ganador if win == 1 else perdedor,True, (200,200,200), (0,0,0))
                rectanguloTextoPresent = imagenTextoPresent.get_rect()
                rectanguloTextoPresent.centerx = screen.get_rect().centerx
                rectanguloTextoPresent.centery =  (screen.get_height() / 2) - 50
                screen.blit(imagenTextoPresent, rectanguloTextoPresent)

                if not WinLose:
                    winSound.play() if win == 1 else loseSound.play()
                    WinLose = True

            velocidad = FPS + diffuculty + velPU + hardcore*10 + (0 if hardcore==0 else nivel)

            texto = pygame.font.SysFont("Arial", 30)
            imagenTextoPresent = texto.render(str(puntuacion),True, (200,200,200), (0,0,0))
            rectanguloTextoPresent = imagenTextoPresent.get_rect()
            rectanguloTextoPresent.centerx = 30
            rectanguloTextoPresent.centery =  30
            screen.blit(imagenTextoPresent, rectanguloTextoPresent)

            texto = pygame.font.SysFont("Arial", 30)
            imagenTextoPresent = texto.render("Velocidad: "+str(velocidad),True, (200,200,200), (0,0,0))
            rectanguloTextoPresent = imagenTextoPresent.get_rect()
            rectanguloTextoPresent.centerx = 1060
            rectanguloTextoPresent.centery =  25
            screen.blit(imagenTextoPresent, rectanguloTextoPresent)

            # RENDER YOUR GAME HERE
            # flip() the display to put your work on screen
            pygame.display.flip()
            clock.tick(FPS + diffuculty + velPU) 
            

            if win == 1 and nivel<10:
                ballX = 0
                ballY = 0
                time.sleep(2) 
                cambiarNivel = "Preaparado para el nivel " + str(nivel + 1)
                texto = pygame.font.SysFont("Arial", 50)
                imagenTextoPresent = texto.render(cambiarNivel,True, (200,200,200), (0,0,0))
                rectanguloTextoPresent = imagenTextoPresent.get_rect()
                rectanguloTextoPresent.centerx = screen.get_rect().centerx
                rectanguloTextoPresent.centery =  (screen.get_height() / 2 ) + 100
                screen.blit(imagenTextoPresent, rectanguloTextoPresent)
                nivel+=1
                pygame.display.flip()
                time.sleep(2) 
                ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
                cordsRect = pygame.Vector2((screen.get_width() / 2) - 120, 610)
                ball_movX = ball_movY = True
                ballX = 0
                ballY = 2
                diffuculty = velPU = tamBarraPU = 0
                inverso = Super = dibujado = False
                blockValid = bloques.Validaciones
                block = bloques.Bloque
                cordsBlocks, cordsBlocksKill, goodPU, badPU = blockValid.coordsBloques(nivel)
                win = -1

        
        

        clock.tick(velocidad) 
            


        pygame.quit()


game.run(1)