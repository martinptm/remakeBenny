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
    
OS-Pfad-Sachen: https://stackoverflow.com/questions/2632205/how-to-count-the-number-of-files-in-a-directory-using-python
"""

import numpy as np
import pygame as pg
import random as ran

from allOtherStuff_new import *
from calcAccel import calcAandV0

def handleEvent(player, event, pg, gP):
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
        elif event.key == pg.K_SPACE:
            gP.throw_up = False
                    
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
            #laser at left and right side of the player (extra shifts found by testing)
            gP.lasers.append( Laser(player.gX()+15, player.gY(), 'red'))
            gP.lasers.append( Laser(player.gX()+player.gWdth(), player.gY(), 'red'))
            gP.throw_up = True

def choosefig(player, gameDisplay, cou, gP):

    c = 0
    if cou%2 ==0: 
        c = 1

    # Throw up sth
    if gP.throw_up:
        player.sImage(gP.throw_images[c])
    # jumping
    elif gP.ychange < 0:
        player.sImage(gP.jump_images[c])
    # falling
    elif gP.ychange > 0:
        player.sImage(gP.fall_images[c])
    # moving
    elif gP.xchange != 0:
        player.sImage(gP.walk_images[c])
    # standing 
    else:
        player.sImage(gP.stand_images[0])

    draw_image(player.gImage(), player.gX(), player.gY(), gameDisplay)

def main():
    
    """
    Idee: Try/Catch für Entscheidung ob mit JoyStick oder Tastatur?
    Oder Menü-Auswahl?
    """
    
    pg.init()
    
    gP = gameParams()
    colors = Colors()
    
    gameDisplay = pg.display.set_mode((gP.disp_wdth, gP.disp_hght))
    gameDisplay.fill(colors.getColor('blue'))
    pg.display.set_caption('Benny-game')

    clock = pg.time.Clock()
    
    # car = pg.image.load('racecar.png')
    # car_size = car.get_rect().size
    # gP.car_width = car_size[0]
    #car_height = car_size[1]
    #print(car_size)

   
    
    # # Bilder laden und auf Größe 50x50px skalieren
    # for c in range(1,13):
    #     im = pg.transform.scale(pg.image.load('./images/explosion/' + str(c) + '.png'), (50, 50))
    #     gP.explosion_images.append(im)
    load_Images(gP, pg)

    player = Player(gP.stand_images[0], 80,  80, gP.y_max)
    
    (a,v0) = calcAandV0(.5, gP.jumpheight)
    
    xPosBloc = ran.randrange(gP.disp_wdth/5, (4/5)*gP.disp_wdth)
    gP.obstacles.append(Obstacle(xPosBloc, xPosBloc+gP.bloc_width, gP.bloc_height, 'red'))
    #xPosBloc = ran.randrange(gP.disp_wdth/5, (4/5)*gP.disp_wdth)
    #gP.obstacles.append(Obstacle(xPosBloc, xPosBloc+gP.bloc_width, gP.bloc_height, 'red'))
    
    for o in gP.obstacles:
        # '+20'-width found by trial
        draw_bloc(o.gColor(), colors, o.gXStart(), gP.y_max+player.gHght()-o.gHeight(), gP.bloc_width+20, o.gHeight(), pg, gameDisplay)
        #draw_bloc(o.gColor(), colors, o.gXStart(), gP.y_max+o.gHeight(), gP.bloc_width, o.gHeight(), pg, gameDisplay)
    

    # Initialsiation Ausgangsposition 
    draw_image(player.gImage(), player.gX(), player.gY(), gameDisplay) 

    cou = 0

    while not gP.quitGame:

        # maybe add some stochastics in here
        cou += 1
        if cou == 180:
            gP.targets.append(Target(ran.randrange(0, gP.disp_wdth - gP.gTargetWidth()), 0, 'green', gP))
            cou = 0
        
        if player.gY() == gP.y_max:# or (gP.aboveObstacle and gP.ycoor > gP.y_max - gP.bloc_height):
            gP.onGround = True
        else:
            gP.onGround = False
            
        for event in pg.event.get():
            handleEvent(player, event, pg, gP)
                      
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
            if player.gX() + gP.xchange > gP.obstacles[c].gXStart() - player.gWdth() and player.gX() + gP.xchange < gP.obstacles[c].gXStop():
                gP.at_x_of_obst = True
                break
            else:
                gP.at_x_of_obst = False
           
        # Interaktion mit einem Hindernis 
        if gP.at_x_of_obst:

            if gP.onGround:
                gP.xchange = 0  
            elif gP.jump: # 
                if player.gY() < gP.y_max - gP.obstacles[c].gHeight():
                    # Fall wenn höher als Hinderniss und noch im Sprung
                    pass
                elif gP.start_jump and gP.ychange==0:
                    # Fall wenn Absprung auf Hindernis
                    pass
                elif player.gY() - gP.ychange <= gP.y_max - gP.obstacles[c].gHeight() and gP.ychange >= 0:
                    # Fall, dass auf dem Hindernis, nur möglich wenn nicht an Höhe gewinnend
                    player.sY(gP.y_max - gP.obstacles[c].gHeight())
                    gP.t = 0
                    gP.jump = False
                    gP.ychange = 0
                else: 
                    # Fall, dass im Sprung gegen eine Seite des Hindernisses stößt
                    gP.xchange = - gP.xchange

        # sonst durch Spielfeld begrenzt
        if player.gX() + gP.xchange <= gP.disp_wdth - player.gWdth() and player.gX() + gP.xchange >= 0:
            player.sX(player.gX() + gP.xchange)
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
            gP.ychange =  1/gP.FPS * (-v0 + a*gP.t)
            player.sY(player.gY() + gP.ychange)
            # alte Formulierung mit festem Startpunkt
            # gP.ycoor = gP.y_max - v0 * gP.t + 0.5 * a * gP.t**2
            
            # Landen auf Boden 
            if player.gY() > gP.y_max:
                player.sY(gP.y_max)
                gP.jump = False
                gP.t = 0
                gP.ychange = 0

        # Bedingung wenn auf Block war, aber nun nicht mehr ist
        if not gP.jump and not gP.at_x_of_obst  and player.gY() < gP.y_max:
            gP.t += 1/gP.FPS
            #gP.ycoor = gP.y_max - gP.obstacles[c].gHeight() + 0.5 * a * gP.t**2  # veränderte Bewegungsgleichung, da kein Absprung
            gP.ychange =  1/gP.FPS * (a*gP.t)  # veränderte Bewegungsgleichung, da kein Absprung
            player.sY(player.gY() + gP.ychange)

            # Landen auf Boden
            if player.gY() > gP.y_max:
                player.sY(gP.y_max)
                gP.t = 0
                gP.ychange = 0
                
        # Ebenen:
        #   - Hintergrund
        #   - Laser
        #   - Targets
        #   - Player
        #   - Obstacle
        #   - Explosion

        # Hintergrund
        gameDisplay.fill(colors.getColor('blue'))

        # Laser
        for l in gP.lasers:  

            target_hit = False
            for t in gP.targets:
                if ( l.gY() <= t.gY()+t.gHght() ) and  ( l.gX()+l.gWdth() >= t.gX() and l.gX() < t.gX()+t.gWdth() ):
                    target_hit = True
                    gP.explosions.append(Explosion(l.gX(), l.gY()))
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
                if t.gY() >= gP.y_max + (player.gHght() - o.gHeight()) and (t.gX() + t.gWdth() >= o.gXStart() and t.gX() <= o.gXStop()):
                    #print("obstacle hit!")
                    hit_obstacle = True
                    gP.targets.remove(t)
                    gP.explosions.append(Explosion(t.gX(), t.gY()-30))
                    gP.lives -= 1
                    break
                else:
                    hit_obstacle = False

            if not hit_obstacle:
                # check y- and x-coordinates of target and player, ycheck so that you can jump over a target without getting hit
                if (t.gY() >= player.gY() and t.gY() < player.gY() + player.gHght()) and  (t.gX() > player.gX() and t.gX() < player.gX() + player.gWdth()):
                    #print("player hit!")
                    gP.lives = 0
                # falling
                elif t.gY() + 5 < gP.y_max+player.gHght():
                    t.sY(t.gY()+5)
                    draw_bloc(t.gCol(), colors, t.gX(), t.gY()-t.gHght(), t.gWdth(), t.gHght(), pg, gameDisplay)
                # hits ground
                else:
                    gP.lives -= 1
                    #print("ground hit!")
                    gP.explosions.append(Explosion(t.gX(), t.gY()-30))
                    gP.targets.remove(t)

        # Player
        choosefig(player, gameDisplay, cou, gP)    

        # Obstacles
        for o in gP.obstacles:
            # '+20'-width found by trial
            draw_bloc(o.gColor(), colors, o.gXStart(), gP.y_max+player.gHght()-o.gHeight(), gP.bloc_width+20, o.gHeight(), pg, gameDisplay)
            #draw_bloc(o.gColor(), colors, o.gXStart(), gP.y_max+o.gHeight(), gP.bloc_width, o.gHeight(), pg, gameDisplay)
        # Explosions
        for e in gP.explosions:
            if e.gState() == len(gP.explosion_images)+1:
                gP.explosions.remove(e)
            else:
                # '-10' bei Koordinate empirisch gefunden
                draw_image(gP.explosion_images[e.gState()-1] , e.gX()-10, e.gY()-10, gameDisplay)
                e.sState(e.gState()+1)
        
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