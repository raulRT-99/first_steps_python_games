import math
from enum import Enum

class Configuraciones:

    def dificultad(golpes, dificultad):
        xGolpes = 1
        if golpes>0 and golpes % xGolpes == 0:
            dificultad += 1
        return dificultad

    def arrPowerUps():
        listaUp = list()
        listaDown =list()
        for item in PowerUpsEnum:
            listaUp.append(item)
        for item in PowerDownsEnum:
            listaDown.append(item)
        return listaUp,listaDown


class PowerUpsEnum(Enum):
    VELLESS = -30
    BARRALPLUS = 50
    SUPER = True

class PowerDownsEnum(Enum):
    VELPLUS = 27
    BARRALESS = -35
    INVERSO = True
    BARRAUP = 120
