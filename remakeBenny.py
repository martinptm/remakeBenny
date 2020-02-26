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

from allOtherStuff import Colors, changeMoveDown, draw_bloc, mv_bloc, gameParams
from calcAccel import calcAandV0

    
def main():
    pg.init()
    
    gP = gameParams()
    colors = Colors()
    
    gameDisplay = pg.display.set_mode((gP.disp_wdth, gP.disp_hght))
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
    
        # Alle Nutzeraktionen bezüglich des gameDisplays erfassen
        for event in pg.event.get():
            
            # wenn gameDisplay geschlossen wird die Spielschleife verlassen
            if event.type == pg.QUIT:
                gP.quitGame = True
            #print(event)
            
            # Loslassen einer Taste ausgenommen der Sprungtaste (damit Bewegen
            # und Springen gleichzeitig möglich) 
            if event.type == pg.KEYUP and not event.key == pg.K_UP:
                
                if gP.moveright and event.key == pg.K_RIGHT or gP.moveleft and event.key == pg.K_LEFT:
                    gP.keyup = True
                    gP.xchange = 0
                    gP.moveright = False
                    gP.moveleft = False
            
            # Tastendruck detektieren
            if event.type == pg.KEYDOWN:
                gP.keyup = False
                
                # Sprunganimation einleiten
                if event.key == pg.K_UP:
                    if gP.jump_clickable:
                        gP.jump_clickable = False
                        gP.jump = True
                        gP.movedown = False
                        gP.t = 0
                
                # nach links oder rechts bewegen
                elif event.key == pg.K_RIGHT:
                    gP.moveright = True
                    gP.xchange += 5
                elif event.key == pg.K_LEFT:
                    gP.moveleft = True
                    gP.xchange -= 5
        
        if not gP.keyup and (gP.moveright and gP.xcoor <= gP.disp_wdth - car_width) or(gP.moveleft and gP.xcoor >= 0):
            gP.xcoor += gP.xchange

        if gP.jump:
            #if gP.xcoor > xPosBloc and gP.xcoor < xPosBloc+gP.bloc_width:
             #   if gP.ycoor > gP.y_max+car_height-gP.bloc_height: 
                #gP.ycoor = gP.y_max
                 #   gP.jump = False
                  #  gP.jump_clickable = True
            if gP.ycoor > gP.y_max:
                gP.ycoor = gP.y_max
                gP.jump = False
                gP.jump_clickable = True
            else:
                gP.t += 1/gP.FPS
                gP.ycoor = gP.y_max - v0 * gP.t + 0.5 * a * gP.t**2
            
        gameDisplay.fill(colors.getColor('black'))
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