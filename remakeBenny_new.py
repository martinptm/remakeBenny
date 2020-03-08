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

    # detect if gamewindow is closed or esc-key is pressed
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
            #laser at left and right side of the player
            gP.lasers.append( Laser(gP.xcoor, gP.ycoor, 'red'))
            gP.lasers.append( Laser(gP.xcoor+gP.car_width, gP.ycoor, 'red'))
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
    gP.car_width = car_size[0]
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

    cou = 0

    while not gP.quitGame:

        # maybe add some stochastics in here
        cou += 1
        if cou == 60:
            gP.targets.append(Target(ran.randrange(0, gP.disp_wdth - gP.gTargetWidth()), 0, 'green', gP))
            print(gP.targets)
            cou = 0
        
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
            if gP.xcoor + gP.xchange > gP.obstacles[c].gXStart() - gP.car_width and gP.xcoor + gP.xchange < gP.obstacles[c].gXStop():
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
        if gP.xcoor + gP.xchange <= gP.disp_wdth - gP.car_width and gP.xcoor + gP.xchange >= 0:
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
                
        # Ebenen:
        #   - Hintergrund
        #   - Laser
        #   - Targets
        #   - Player
        #   - Obstacle

        # Hintergrund
        gameDisplay.fill(colors.getColor('blue'))

        # Laser
        for l in gP.lasers:  

            target_hit = False
            for t in gP.targets:
                if ( l.gY() <= t.gY()+t.gHght() ) and  ( l.gX()+l.gWdth() >= t.gX() and l.gX() < t.gX()+t.gWdth() ):
                    target_hit = True
                    print("target hit!")
                    gP.targets.remove(t)
                    gP.lasers.remove(l)
                    break

            if not target_hit:
                if l.gY() < 0:
                    gP.lasers.remove(l)
                else: 
                    draw_bloc(l.gCol(), colors, l.gX(), l.gY()-l.gHght(), l.gWdth(), l.gHght(), pg, gameDisplay)
                    l.sY(l.gY()-20)  

        # Targets
        for t in gP.targets:

            for o in gP.obstacles:  
                # check if target hits an obstacle
                if t.gY() >= gP.y_max + (car_height - o.gHeight()) and (t.gX() + t.gWdth() >= o.gXStart() and t.gX() <= o.gXStop()):
                    #print("obstacle hit!")
                    hit_obstacle = True
                    gP.targets.remove(t)
                    gP.lives -= 1
                    break
                else:
                    hit_obstacle = False

            if not hit_obstacle:
                # check y- and x-coordinates of target and player, ycheck so that you can jump over a target without getting hit
                if (t.gY() >= gP.ycoor and t.gY() < gP.ycoor + car_height) and  (t.gX() > gP.xcoor and t.gX() < gP.xcoor + gP.car_width):
                    #print("player hit!")
                    gP.lives = 0
                # falling
                elif t.gY() + 5 < gP.y_max+car_height:
                    t.sY(t.gY()+5)
                    draw_bloc(t.gCol(), colors, t.gX(), t.gY()-t.gHght(), t.gWdth(), t.gHght(), pg, gameDisplay)
                # hits ground
                else:
                    gP.lives -= 1
                    #print("ground hit!")
                    gP.targets.remove(t)

        # Player
        mv_bloc(car, gP.xcoor, gP.ycoor, gameDisplay)

        # Obstacles
        for o in gP.obstacles:
            draw_bloc(o.gColor(), colors, o.gXStart(), gP.y_max+car_height-o.gHeight(), gP.bloc_width, o.gHeight(), pg, gameDisplay)
        
        pg.display.update()
        
        # number of FPS at which the game ist running
        clock.tick(gP.FPS)

        if gP.lives < 1:
            gP.quitGame = True
            print("You lost!")
        
    # Spiel beenden und Programm verlassen 
    pg.quit()
    quit()
    

if __name__ == "__main__":
    main()