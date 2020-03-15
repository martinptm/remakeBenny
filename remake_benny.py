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

from all_other_stuff import *
from calcAccel import calcAandV0

def handleEvent(player, event, pg, gP):
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
            r = ran.randrange(0, len(gP.things_throw_images))
            if gP.fruits_left > 0:
                gP.fruits_left -= 1
                gP.lasers.append( an_obj(player.gX()+15, player.gY(), 20, 20, gP.things_throw_images[r], 0))
            if gP.fruits_left > 0:
                gP.fruits_left -= 1
                gP.lasers.append( an_obj(player.gX()+player.gW(), player.gY(), 20, 20, gP.things_throw_images[r], 0))
            gP.throw_up = True

def choosefig(player, gameDisplay, cou, gP):
    # Throw up sth
    if gP.throw_up:
        player.sImages(gP.throw_images)
    # jumping
    elif gP.ychange < 0:
        player.sImages(gP.jump_images)
    # falling
    elif gP.ychange > 0:
        player.sImages(gP.fall_images)
    # moving
    elif gP.xchange != 0:
        player.sImages(gP.walk_images)
    # standing 
    else:
        player.sImages(gP.stand_images)

    player.sState(player.gState()+1)

    draw_image(player.gImage(), player.gX(), player.gY(), gameDisplay)

def main(): 
    """
    Idee: Try/Catch für Entscheidung ob mit JoyStick oder Tastatur?
    Oder Menü-Auswahl?
    """ 
    pg.init()

    pg.font.init() # you have to call this at the start, 
                   # if you want to use this module.
    myfont = pg.font.SysFont('Comic Sans MS', 30)
    
    gP = gameParams()
    colors = Colors()
    
    gameDisplay = pg.display.set_mode((gP.disp_wdth, gP.disp_hght))
    gameDisplay.fill(colors.getColor('blue'))
    pg.display.set_caption('Hide the pain EARTH')

    clock = pg.time.Clock()
    
    load_Images(gP, pg)

    player = an_obj(0,  gP.y_max-100, 80,  80, gP.stand_images, 0)
    
    (a,v0) = calcAandV0(.5, gP.jumpheight)
    
    xPosBloc = ran.randrange(gP.disp_wdth/5, (4/5)*gP.disp_wdth)
    gP.obstacles.append(an_obj(xPosBloc, gP.y_max, 90, 60, gP.obstacle_images, 0))
    
    for o in gP.obstacles:
        # '+20'-width found by trial
        draw_image(o.gImage(), o.gX(), gP.y_max+player.gH()-o.gH(), gameDisplay)

    # Initialsiation Ausgangsposition 
    draw_image(player.gImage(), player.gX(), player.gY(), gameDisplay) 

    cou = 0

    while not gP.quitGame:

        # maybe add some stochastics in here
        r = ran.randrange(0, 8)
        cou += 1
        if cou%30 == 0 and gP.fruits_left < 6:
            gP.fruits_left += 1
        if cou+r >= 70 or (gP.species_saved >= 5 and cou+r >= 50):
            target_nr = ran.randrange(0, len(gP.target_images))
            gP.targets.append(an_obj(ran.randrange(0, gP.disp_wdth - gP.gTargetWidth()), 0, 20, 20, gP.target_images[target_nr], 0))
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
            # '-20' wegen Aussehen
            if player.gX() + gP.xchange > gP.obstacles[c].gX() - player.gW() and player.gX() + gP.xchange < gP.obstacles[c].gX() + gP.obstacles[c].gW() -20:
                gP.at_x_of_obst = True
                break
            else:
                gP.at_x_of_obst = False
           
        # Interaktion mit einem Hindernis 
        if gP.at_x_of_obst:

            if gP.onGround:
                gP.xchange = 0  
            elif gP.jump: # 
                if player.gY() < gP.y_max - gP.obstacles[c].gH():
                    # Fall wenn höher als Hinderniss und noch im Sprung
                    pass
                elif gP.start_jump and gP.ychange==0:
                    # Fall wenn Absprung auf Hindernis
                    pass
                elif player.gY() - gP.ychange <= gP.y_max - gP.obstacles[c].gH() and gP.ychange >= 0:
                    # Fall, dass auf dem Hindernis, nur möglich wenn nicht an Höhe gewinnend
                    player.sY(gP.y_max - gP.obstacles[c].gH())
                    gP.t = 0
                    gP.jump = False
                    gP.ychange = 0
                else: 
                    # Fall, dass im Sprung gegen eine Seite des Hindernisses stößt
                    gP.xchange = - gP.xchange

        # sonst durch Spielfeld begrenzt
        # '-10' wegen Aussehen
        if player.gX() + gP.xchange <= gP.disp_wdth - player.gW() and player.gX() + gP.xchange >= 0-15:
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
            
            # Landen auf Boden 
            if player.gY() > gP.y_max:
                player.sY(gP.y_max)
                gP.jump = False
                gP.t = 0
                gP.ychange = 0

        # Bedingung wenn auf Block war, aber nun nicht mehr ist
        if not gP.jump and not gP.at_x_of_obst  and player.gY() < gP.y_max:
            gP.t += 1/gP.FPS
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
                if ( l.gY() <= t.gY()+t.gH() ) and  ( l.gX()+l.gW() >= t.gX() and l.gX() < t.gX()+t.gW() ):
                    target_hit = True
                    gP.species_saved += 1
                    r = ran.randrange(0, len(gP.things_hit_images))
                    gP.explosions.append(an_obj(l.gX(), l.gY(), 50, 50, gP.things_hit_images[r], 0))
                    gP.targets.remove(t)
                    gP.lasers.remove(l)
                    break

            if not target_hit:
                if l.gY() < 0:
                    gP.lasers.remove(l)
                else: 
                    #draw_bloc(l.gCol(), colors, l.gX(), l.gY()-l.gHght(), l.gWdth(), l.gHght(), pg, gameDisplay)
                    draw_image(l.gImage(), l.gX(), l.gY()-l.gH(), gameDisplay)
                    l.sY(l.gY()-20)
                    l.sState(l.gState()+1)

        # Targets
        for t in gP.targets:

            for o in gP.obstacles:  
                # check if target hits an obstacle
                if t.gY() >= gP.y_max + (player.gH() - o.gH()) and (t.gX() + t.gW() >= o.gX() and t.gX() <= o.gX() + o.gW()):
                    #print("obstacle hit!")
                    hit_obstacle = True
                    gP.targets.remove(t)
                    gP.explosions.append(an_obj(t.gX(), t.gY(), 50, 50, gP.co2_images, 0))
                    #gP.explosions.append(Explosion(t.gX(), t.gY()-30))
                    gP.lives -= 1
                    break
                else:
                    hit_obstacle = False

            if not hit_obstacle:
                # check y- and x-coordinates of target and player, ycheck so that you can jump over a target without getting hit
                if (t.gY() >= player.gY() and t.gY() < player.gY() + player.gH()) and  (t.gX() > player.gX() and t.gX() < player.gX() + player.gW()):
                    #print("player hit!")
                    gP.lives = 0
                # falling
                elif t.gY() + 5 < gP.y_max+player.gH()-t.gH():
                    t.sY(t.gY()+5)
                    #draw_bloc(t.gCol(), colors, t.gX(), t.gY()-t.gHght(), t.gWdth(), t.gHght(), pg, gameDisplay)
                    draw_image(t.gImage(), t.gX()-t.gW(), t.gY()-t.gH(), gameDisplay)
                    t.sState(t.gState()+1)
                # hits ground
                else:
                    gP.lives -= 1
                    #gP.explosions.append(Explosion(t.gX(), t.gY()-30))
                    gP.explosions.append(an_obj(t.gX(), t.gY(), 50, 50, gP.co2_images, 0))
                    gP.targets.remove(t)

        # Player
        choosefig(player, gameDisplay, cou, gP)    

        # Obstacles
        for o in gP.obstacles:
            # '+20'-width found by trial
            #draw_bloc(o.gColor(), colors, o.gXStart(), gP.y_max+player.gHght()-o.gHeight(), gP.bloc_width+20, o.gHeight(), pg, gameDisplay)
            draw_image(o.gImage(), o.gX(), o.gY()+20, gameDisplay)
        # Explosions
        for e in gP.explosions:
            if e.gState() == e.gNImages()-1:
                gP.explosions.remove(e)
            else:
                # '-10' bei Koordinate empirisch gefunden
                draw_image(e.gImage(), e.gX()-10, e.gY()-10, gameDisplay)
                e.sState(e.gState()+1)

        draw_image(gP.counter_co2_images[str(gP.lives*60)], 500, 0, gameDisplay)
        draw_image(gP.counter_fruits_images[str(gP.fruits_left)], 500, 100, gameDisplay)
        draw_image(gP.rescued_species_image[0], 500, 200, gameDisplay)
        textsurface = myfont.render(str(gP.species_saved), False, (0, 0, 0))
        gameDisplay.blit(textsurface,(545,275))
        
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