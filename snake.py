import pygame
import random

class main:

    def foodCollision(x,y,coords):
        return False

    def run():

        # pygame
        pygame.init()
        pygame.display.set_caption("Snake")
        height = 800
        width = 400
        screen = pygame.display.set_mode((height, width))
        clock = pygame.time.Clock()
        running = True
        cont =0
        start = True
        win = True

        #snake
        coordsAppend = list()
        anterior = "UP"
        color = "white"
        # xMov = 580
        # yMov = 320
        xMov = 400
        yMov = 200
        largo = 1

        #food
        x = 110
        y = 110


        while running:
            ball_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 2)
            
            
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and anterior != "DOWN":
                        anterior = "UP"
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and anterior != "UP":
                        anterior = "DOWN"
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and anterior != "RIGHT":
                        anterior = "LEFT"
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and anterior != "LEFT":
                        anterior = "RIGHT"

            screen.fill("black")

            if cont == 10:
                if anterior == "UP":
                    yMov -= 20
                elif anterior == "DOWN":
                    yMov += 20
                elif anterior == "LEFT":
                    xMov -= 20
                elif anterior == "RIGHT":
                    xMov += 20
                cont = 0
                if xMov >= height:
                    xMov = 0
                elif xMov <= -20:
                    xMov = height
                elif yMov >= width:
                    yMov = 0
                elif yMov <= -20:
                    yMov = width


                for cordsExist in coordsAppend:
                    if cordsExist == (xMov,yMov):
                        win = False

                coordsAppend.insert(0,(xMov,yMov))
                if len(coordsAppend) -1 > largo:
                    for n in range(len(coordsAppend) - largo):
                        coordsAppend.pop()

            if win:
                pygame.draw.rect(screen, color, (xMov, yMov, 20,20))
                if len(coordsAppend) > 1:
                    for c in range(largo):
                        if c < len(coordsAppend):
                            coordsX,coordsY = coordsAppend[c]
                            pygame.draw.rect(screen, color, (coordsX, coordsY, 20,20))
                

                if x > xMov and x < xMov + 20 and y > yMov and y < yMov + 20:
                    repetir = True
                    while repetir:
                        x = random.randrange(0,height - 20,20) + 10
                        y = random.randrange(0,width - 20,20) + 10
                        for cordsSnake in coordsAppend:
                            xSnake, ySnake = cordsSnake
                            if not (x > xSnake and x < xSnake + 20 and y > ySnake and y < ySnake + 20):
                                repetir = False
                    largo += 1

                pygame.draw.circle(screen, "white", (x,y), 7)
            else:
                perdedor = "Perdiste, el juego te ah superado"
                texto = pygame.font.SysFont("Arial", 50)
                imagenTextoPresent = texto.render(perdedor,True, (200,200,200), (0,0,0))
                rectanguloTextoPresent = imagenTextoPresent.get_rect()
                rectanguloTextoPresent.centerx = screen.get_rect().centerx
                rectanguloTextoPresent.centery =  (screen.get_height() / 2) - 50
                screen.blit(imagenTextoPresent, rectanguloTextoPresent)

            
            pygame.display.flip()
            clock.tick(30) 
            cont +=1

        pygame.quit()


main.run()