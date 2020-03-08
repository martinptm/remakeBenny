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

from allOtherStuff_new import *
from calcAccel import calcAandV0

def handleEvent(event, pg, gP):
    #print(event)

    if event.type == pg.QUIT:
        gP.quitGame = True
    elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:  # äquivalent wäre == 27
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
        elif event.key == pg.K_RIGHT:
            gP.stopXMove = False
            gP.mr = True
            gP.ml = False
        elif event.key == pg.K_LEFT:
            gP.stopXMove = False
            gP.ml = True
            gP.mr = False
        elif event.key == pg.K_SPACE:
            gP.lasers.append( Laser(gP.xcoor, gP.ycoor, 'red'))
            print(gP.lasers)

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
    gP.obstacles.append(Obstacle(xPosBloc, xPosBloc+gP.bloc_width, gP.bloc_height, 'red'))
    #xPosBloc = ran.randrange(gP.disp_wdth/5, (4/5)*gP.disp_wdth)
    #gP.obstacles.append(Obstacle(xPosBloc, xPosBloc+gP.bloc_width, gP.bloc_height, 'red'))
    
    for o in gP.obstacles:
        draw_bloc(o.gColor(), colors, o.gXStart(), gP.y_max+car_height-o.gHeight(), gP.bloc_width, o.gHeight(), pg, gameDisplay)
    
    # Initialsiation Ausgangsposition 
    mv_bloc(car, gP.xcoor, gP.ycoor, gameDisplay)

    while not gP.quitGame:
        
        if gP.ycoor == gP.y_max:# or (gP.aboveObstacle and gP.ycoor > gP.y_max - gP.bloc_height):
            gP.onGround = True
        else:
            gP.onGround = False
            
        for event in pg.event.get():
            handleEvent(event, pg, gP)
                      
        if gP.onGround or (gP.at_x_of_obst and not gP.jump):
            if gP.start_jump:
                gP.jump = True
            if gP.mr:
                gP.xchange = gP.step_size
            elif gP.ml:
                gP.xchange = -gP.step_size
            else:
                gP.xchange = 0

        # Zähler indentifiziert das aktuell relevante Hinderniss
        c = 0
        for c in range(0, len(gP.obstacles)):
            if gP.xcoor + gP.xchange > gP.obstacles[c].gXStart() - car_width and gP.xcoor + gP.xchange < gP.obstacles[c].gXStop():
                gP.at_x_of_obst = True
                break
            else:
                gP.at_x_of_obst = False
           
        # Interaktion mit einem Hindernis 
        if gP.at_x_of_obst:

            if gP.onGround:
                gP.xchange = 0  
            elif gP.jump: # 
                if gP.ycoor < gP.y_max - gP.obstacles[c].gHeight():
                    # Fall wenn höher als Hinderniss und noch im Sprung
                    pass
                elif gP.start_jump:
                    # Fall wenn Absprung auf Hindernis
                    pass
                elif gP.ycoor - ychange <= gP.y_max - gP.obstacles[c].gHeight() and ychange >= 0:
                    # Fall, dass auf dem Hindernis, nur möglich wenn nicht an Höhe gewinnend
                    #no y-change
                    gP.ycoor = gP.y_max - gP.obstacles[c].gHeight()
                    gP.t = 0
                    gP.jump = False
                else: 
                    # Fall, dass im Sprung gegen eine Seite des Hindernisses stößt
                    gP.xchange = - gP.xchange

        # sonst durch Spielfeld begrenzt
        if gP.xcoor + gP.xchange <= gP.disp_wdth - car_width and gP.xcoor + gP.xchange >= 0:
            gP.xcoor += gP.xchange
        elif not gP.onGround:
            gP.xchange = - gP.xchange

        # das so eig. schön, da springen von Hinderniss dann höher usw.
        if gP.jump:
            
            gP.t += 1/gP.FPS
                
            # Bewegungsgleichung muss so abgeändert werden, dass unabh. von Starthöhe, also Berechnung von y-Change,
            # sodass ycoor = ycoor + ychange 
            # oder Parameter für Absprunghöhenstart
            # Abl. nach t:
            # -v0 + a*gP.t
            # flexible Formulierung ohne Abhändigkeit von Absprunghöhe
            ychange =  1/gP.FPS * (-v0 + a*gP.t)
            gP.ycoor += ychange
            # alte Formulierung mit festem Startpunkt
            # gP.ycoor = gP.y_max - v0 * gP.t + 0.5 * a * gP.t**2
            
            # Landen auf Boden 
            if gP.ycoor > gP.y_max:
                gP.ycoor = gP.y_max
                gP.jump = False
                gP.t = 0

        # Bedingung wenn auf Block war, aber nun nicht mehr ist
        if not gP.jump and not gP.at_x_of_obst  and gP.ycoor < gP.y_max:
            gP.t += 1/gP.FPS
            #gP.ycoor = gP.y_max - gP.obstacles[c].gHeight() + 0.5 * a * gP.t**2  # veränderte Bewegungsgleichung, da kein Absprung
            ychange =  1/gP.FPS * (a*gP.t)  # veränderte Bewegungsgleichung, da kein Absprung
            gP.ycoor += ychange

            if gP.ycoor > gP.y_max:
                gP.ycoor = gP.y_max
                gP.t = 0
                
        gameDisplay.fill(colors.getColor('blue'))
        mv_bloc(car, gP.xcoor, gP.ycoor, gameDisplay)
        for o in gP.obstacles:
            draw_bloc(o.gColor(), colors, o.gXStart(), gP.y_max+car_height-o.gHeight(), gP.bloc_width, o.gHeight(), pg, gameDisplay)

        for l in gP.lasers:
            draw_bloc(l.gCol(), colors, l.gX(), l.gY()-l.gHght(), l.gWdth(), l.gHght(), pg, gameDisplay)
            l.sY(l.gY()-20)
            if l.gY() < 0:
                gP.lasers.remove(l)
        
        pg.display.update()
        
        # number of FPS at which the game ist running
        clock.tick(gP.FPS)
        
    # Spiel beenden und Programm verlassen 
    pg.quit()
    quit()
    

if __name__ == "__main__":
    main()