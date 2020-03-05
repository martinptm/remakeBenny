"""
Ziel dieses Projektes ist das Erlernen von Grundfunktionen von PyGame.
Meine erse Idee wäre ein Remake von Benny.scratch2, wobei z.B. eine Amination
eines hüpfenden/fallenden Gegenstands mit einer einfachen realitätsnäheren
Implementierung erweitert werden könnte.

can be run from interactive shell using " exec(open('remakeBenny.py').read())", see
https://stackoverflow.com/questions/17247471/how-to-run-a-python-script-from-idle-interactive-shell.
or (at least in Thonny IDE) using:
%Run remakeBenny.py

https://pythonprogramming.net/pygame-python-3-part-1-intro/


Python elegant alternative for switch-case:
https://bytebaker.com/2008/11/03/switch-case-statement-in-python/

In Thonny verfügbare Shortcuts sind bei -> Edit zu finden !!!

Simultion Sprung (Herleitung siehe 'calcAccel.py'):
    v0 = 267
    a = 356
    y(t) = y_max - v0 * t + 0.5 a * t²

"""

import numpy as np
import pygame as pg
import random as ran

from allOtherStuff_new import Colors, changeMoveDown, draw_bloc, mv_bloc, gameParams
from calcAccel import calcAandV0

    
def main():
    pg.init()
    
    gP = gameParams()
    colors = Colors()
    
    gameDisplay = pg.display.set_mode((gP.disp_wdth, gP.disp_hght))
    gameDisplay.fill(colors.getColor('blue'))
    pg.display.set_caption('Benny-game')

    clock = pg.time.Clock()
    
    car = pg.image.load('racecar.png')
    
    car_size = car.get_rect().size
    car_width = car_size[0]
    car_height = car_size[1]
    
    (a,v0) = calcAandV0(.5, gP.jumpheight)
    
    xPosBloc = ran.randrange(gP.disp_wdth/5, (4/5)*gP.disp_wdth)
   
    draw_bloc('red', colors, xPosBloc, gP.y_max+car_height-gP.bloc_height, gP.bloc_width, gP.bloc_height, pg, gameDisplay)
    
    # Initialsiation Ausgangsposition 
    mv_bloc(car, gP.xcoor, gP.ycoor, gameDisplay)

    while not gP.quitGame:
        
        if gP.ycoor == gP.y_max:# or (gP.aboveObstacle and gP.ycoor > gP.y_max - gP.bloc_height):
            gP.onGround = True
        else:
            gP.onGround = False
            
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                gP.quitGame = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE: # äquivalent wäre == 27
                gP.quitGame = True
                
            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    gP.mr = False
                elif event.key == pg.K_LEFT:
                    gP.ml = False
                elif event.key == pg.K_UP:
                    gP.start_jump = False
                    
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    gP.start_jump = True
                if event.key == pg.K_RIGHT:
                    gP.stopXMove = False
                    gP.mr = True
                    gP.ml = False
                elif event.key == pg.K_LEFT:
                    gP.stopXMove = False
                    gP.ml = True
                    gP.mr = False
                      
        if gP.onGround:
            if gP.start_jump:
                gP.jump = True
            if gP.mr:
                gP.xchange = 5
            elif gP.ml:
                gP.xchange = -5
            else:
                gP.xchange = 0
            
        if gP.xcoor + gP.xchange <= gP.disp_wdth - car_width and gP.xcoor + gP.xchange >= 0:
            gP.xcoor += gP.xchange
        elif not gP.onGround:
            gP.xchange = - gP.xchange
           
        #if gP.xcoor > xPosBloc and gP.xcoor < xPosBloc + gP.bloc_width:
        #    gP.aboveObstacle = True
        #else:
         #   gP.aboveObstacle = False

        # das so eig. schön, da springen von Hinderniss dann höher usw.
        if gP.jump:
            # Berechne neue y-Position und beende Sprung wenn auf Untergrund oder Hindernis
            gP.t += 1/gP.FPS
            gP.ycoor = gP.y_max - v0 * gP.t + 0.5 * a * gP.t**2
            
            #if gP.aboveObstacle and gP.ycoor > gP.y_max - gP.bloc_height: #problem wird sein, dass dann nicht witer runter fällt
            #    gP.jump = False
            #    gP.t = 0   
            if gP.ycoor > gP.y_max:
                gP.ycoor = gP.y_max
                gP.jump = False
                gP.t = 0
                
        gameDisplay.fill(colors.getColor('blue'))
        mv_bloc(car, gP.xcoor, gP.ycoor, gameDisplay)
        draw_bloc('red', colors, xPosBloc, gP.y_max+car_height-gP.bloc_height, gP.bloc_width, gP.bloc_height, pg, gameDisplay)
        
        pg.display.update()
        
        # number of FPS at which the game ist running
        clock.tick(gP.FPS)
        
    # Spiel beenden und Programm verlassen 
    pg.quit()
    quit()
    

if __name__ == "__main__":
    main()