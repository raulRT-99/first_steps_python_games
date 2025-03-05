import pygame
import random
import config as cfg

class Bloque:

    def dibujar(pantalla, cords, cordsKill, good, bad):
        cordsXY = dict()
        bueno = (0,43,255)
        malo = (203,35,35)
        normal = (90,190,190)
        color = normal
        cordsPU = dict()
        for item in cords:
            x,y = item
            xGB = x
            yGB = y
            x = x*115
            y = y*32 + 5
            if cordsKill.get(item):
                cordsXY[(x,y)] = True
                if tuple((xGB,yGB)) in good:
                    color = bueno
                elif tuple((xGB,yGB)) in bad:
                    color = malo
                else:
                    color = normal
                cordsPU[(x,y)] = color
                pygame.draw.rect(pantalla, color, ((x,y), (100,30)), 0,4)
            else:
                cordsXY[(x,y)] = False
        return cordsXY, cordsPU

    
    def bloquePU(cordsXY, cordsPU):
        bueno = (0,43,255)
        malo = (203,35,35)
        normal = (90,190,190)
        powerUps, powerDowns = cfg.Configuraciones.arrPowerUps()
        if cordsPU.get(cordsXY) == bueno:
            return random.choice(powerUps)
        elif cordsPU.get(cordsXY) == malo:
            return random.choice(powerDowns)
        else:
            return 0


class Validaciones:

    def golpeoX(ball_movX, ball_pos, bordeX, ballX):
        if (ball_pos.x >= bordeX - 4) or (ball_pos.x <= 4):
            ballX = ballX*-1
            ball_movX = not ball_movX
        return ballX,ball_movX


    def golpeoY(ball_movY,ball_pos,bordeY,ballX,ballY):
        if ball_movY and ball_pos.y < bordeY:
            ball_pos.y += ballY
            ball_pos.x += ballX 
        elif not ball_movY and ball_pos.y > 0:
            ball_pos.y -= ballY    
            ball_pos.x += ballX
        return ball_pos.x,ball_pos.y

    
    def coordsBloques(nivel):
        lista = list()
        coords = list()
        cordsKill =dict()
        count = 1
        goodPU = list()
        badPU = list()
        totalBolas = nivel*10
        minBolasBuenas = 1
        minBolasMalas = nivel*2 + nivel%3 - (nivel//5)*3
        maxBolasMalas = nivel*3 + nivel//2
        # 550, 630
        # x->63, y->55 
        for i in range(totalBolas):
            while True:
                x = random.randrange(0,100)
                if x not in lista:
                    lista.append(x)
                    break
        
        for item in lista:
            y = item//10
            x = item%10
            coords.append(tuple((x,y)))
            if count >= minBolasBuenas and count <= minBolasMalas:
                goodPU.append(tuple((x,y)))
            elif count >= minBolasMalas and count <= maxBolasMalas:
                badPU.append(tuple((x,y))) 
            count += 1

        for item in coords:
            cordsKill[tuple(item)] = True

        return tuple((coords, cordsKill,goodPU,badPU))


    def golpePU(pu,enumPU,enumPD,tamBarraPU,velPU,inv,Super,barraUp):
        powerUps,powerDowns = cfg.Configuraciones.arrPowerUps()
        tipoBloque = 2
        #0
        if pu in powerUps or pu in powerDowns:
            if pu == enumPU.VELLESS or pu == enumPD.VELPLUS:
                velPU = 0
                velPU += pu.value
            elif pu == enumPU.BARRALPLUS or pu == enumPD.BARRALESS:
                tamBarraPU = 0
                tamBarraPU += pu.value
            elif pu == enumPU.SUPER:
                Super = True
        #1
        if pu in powerDowns:
            if pu == enumPD.INVERSO:
                inv = True
            elif pu == enumPD.BARRAUP:
                barraUp = pu.value

        if pu in powerUps:
            tipoBloque = 1
        elif pu in powerDowns:
            tipoBloque = 0


        return tamBarraPU,velPU,tipoBloque,inv,Super,barraUp

    def resetPU(pu,velPU,tamBarraPU,enumPU,enumPD,inv,Super,barraUp):
        if pu == enumPU.VELLESS or pu == enumPD.VELPLUS:
            velPU = 0
        elif pu == enumPU.BARRALPLUS or pu == enumPD.BARRALESS:
            tamBarraPU = 0
        elif pu == enumPD.INVERSO:
            inv = False
        elif pu == enumPU.SUPER:
            Super = False
        elif pu == enumPD.BARRAUP:
            barraUp = 0
        return velPU,tamBarraPU,inv,Super,barraUp
        





