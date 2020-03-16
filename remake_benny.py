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
import time
import ptext

from all_other_stuff import *
from calcAccel import calcAandV0

def handleEvent(player, event, pg, gP, colors):
    # detect if gamewindow is closed or esc-key is pressed
    if event.type == pg.QUIT:
        gP.quitGame = True
    elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:  # äquivalent wäre == 27
        gP.quitGame = True
         
    if gP.lives > 0:       
        # detect if one of the relevant keys is released
        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                gP.mr = False
            elif event.key == pg.K_LEFT:
                gP.ml = False
            elif event.key == pg.K_UP:
                gP.start_jump = False
            elif event.key == pg.K_SPACE:
                gP.throw_up = False
                    
        # detect if one of the relevant keys is pressed
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
                # throw things at left and right side of the player (extra shifts found by testing) 
                # (only possible if the player has 'fruits' to throw in his basket)
                r = ran.randrange(0, len(gP.things_throw_images))
                if gP.fruits_left > 0:
                    gP.fruits_left -= 1
                    gP.things_to_throw.append( an_obj(player.gX()+15, player.gY(), 20, 20, gP.things_throw_images[r], 0))
                if gP.fruits_left > 0:
                    gP.fruits_left -= 1
                    gP.things_to_throw.append( an_obj(player.gX()+player.gW(), player.gY(), 20, 20, gP.things_throw_images[r], 0))
                gP.throw_up = True

    if event.type == pg.MOUSEBUTTONDOWN:
        mouse_pos = event.pos  # gets mouse position
        if mouse_pos[0] > gP.obstacles[0].gX() and mouse_pos[0] < gP.obstacles[0].gX() + gP.obstacles[0].gW() and mouse_pos[1] > 520 and mouse_pos[1] < 580:
            gP.hidden_texts.append(hidden_text("Inequality because of sex or skin color is not a good thing.\nOur society should overcome this.", (150, 400), 20, colors.getColor('blue')))
        elif mouse_pos[0] >  460 and mouse_pos[0] < 520 and mouse_pos[1] > 530 and mouse_pos[1] < 560:
            gP.hidden_texts.append(hidden_text("There is no planet B!", (100, 100), 30, colors.getColor('green')))
        elif mouse_pos[0] > 45 and mouse_pos[0] < 105 and mouse_pos[1] > 530 and mouse_pos[1] < 570:
            gP.hidden_texts.append(hidden_text("What do we want?\nCLIMATE JUSTICE!\nWhen do we want it?\nNOW!", (400, 300), 25, colors.getColor('red')))
    elif event.type == pg.MOUSEBUTTONUP and len(gP.hidden_texts) > 0:
        gP.hidden_texts.pop()

def choosefig(player, gameDisplay, cou, gP):
    # choose correct type of player-figure according to its current movement/action
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
    # increase state to choose next frame from the matching sequence of images according to the current movement
    player.sState(player.gState()+1)
    draw_image(player.gImage(), player.gX(), player.gY(), gameDisplay)


#def text_objects(text, font):
#    textSurface = font.render(text, True, (0, 0,0))
#    return textSurface, textSurface.get_rect()
def message_display(gameDisplay, hidden_text):
    #largeText = pg.font.Font('freesansbold.ttf', hidden_text.gSize())
    #TextSurf, TextRect = text_objects(hidden_text.gText(), largeText)
    #TextRect.center = hidden_text.gPos()
    #gameDisplay.blit(TextSurf, TextRect)
    ptext.draw(hidden_text.gText(), hidden_text.gPos(), color=hidden_text.gColor(), fontsize=hidden_text.gSize())


def game_loop(myfont, gP, clock, gameDisplay, player, a, v0, colors):
    # counter to track iterations of frames in the game loop
    cou = 0
    # game loop
    while not gP.quitGame:
        cou += 1

        if gP.lives > 0:
            # increase fruits in basket regulary
            if cou%30 == 0 and gP.fruits_left < 6:
                gP.fruits_left += 1

            # rate of appearance increases with more succes in the game (small level of uncertainty comes into play ;D)
            r = ran.randrange(0, 8)
            if cou+r >= 70 or (gP.species_saved >= 5 and cou+r >= 50):
                target_nr = ran.randrange(0, len(gP.target_images))
                gP.targets.append(an_obj(ran.randrange(0, gP.disp_wdth - 20), 0, 20, 20, gP.target_images[target_nr], 0))
                cou = 0
        
        # check if player is at lowes possible point 
        if player.gY() == gP.y_max:
            gP.onGround = True
        else:
            gP.onGround = False
            
        # detect and handle user-input and set movement accordingly
        for event in pg.event.get():
            handleEvent(player, event, pg, gP, colors)      
        if gP.onGround or (gP.at_x_of_obst and not gP.jump):
            if gP.start_jump:
                gP.jump = True
            if gP.mr:
                gP.xchange = gP.step_size
            elif gP.ml:
                gP.xchange = -gP.step_size
            else:
                gP.xchange = 0

        # check if player interacts with the obstacle, '-20' to look better
        for c in range(0, len(gP.obstacles)):
            if player.gX() + gP.xchange > gP.obstacles[c].gX() - player.gW() and player.gX() + gP.xchange < gP.obstacles[c].gX() + gP.obstacles[c].gW() -20:
                gP.at_x_of_obst = True
                break
            else:
                gP.at_x_of_obst = False        
        # interact with the obstacle
        if gP.at_x_of_obst:
            # cannot walk through the obsacle
            if gP.onGround:
                gP.xchange = 0  
            elif gP.jump: 
                # keep falling
                if player.gY() < gP.y_max - gP.obstacles[c].gH():
                    pass
                # jump from obstacle
                elif gP.start_jump and gP.ychange==0:
                    pass
                # land and stand on the obstacle, reset t so if the obstacle is left, the physical fall/jump-simualtion is correct
                elif player.gY() - gP.ychange <= gP.y_max - gP.obstacles[c].gH() and gP.ychange >= 0:
                    player.sY(gP.y_max - gP.obstacles[c].gH())
                    gP.t = 0
                    gP.jump = False
                    gP.ychange = 0
                # bounce off obstacle-side
                else: 
                    gP.xchange = - gP.xchange

        # limits of playing-field, '-10' to look better
        if player.gX() + gP.xchange <= gP.disp_wdth - player.gW() and player.gX() + gP.xchange >= 0-15:
            player.sX(player.gX() + gP.xchange)
        elif not gP.onGround:
            gP.xchange = - gP.xchange

        # jump-simulation (independent of starting point since change of position and not the absolute position is calculated)
        if gP.jump:  
            gP.t += 1/gP.FPS    
            gP.ychange =  1/gP.FPS * (-v0 + a*gP.t)
            player.sY(player.gY() + gP.ychange)   
            # land on the ground 
            if player.gY() > gP.y_max:
                player.sY(gP.y_max)
                gP.jump = False
                gP.t = 0
                gP.ychange = 0

        # if player stood on obstacle and now leaving it. No initial jump, only falling down.
        if not gP.jump and not gP.at_x_of_obst  and player.gY() < gP.y_max:
            gP.t += 1/gP.FPS
            gP.ychange =  1/gP.FPS * (a*gP.t) 
            player.sY(player.gY() + gP.ychange)
            # land on the ground 
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

        # draw background
        #gameDisplay.fill(colors.getColor('blue'))
        draw_image(gP.background_image[0], 0, 0, gameDisplay)

        # fruits to throw
        for f in gP.things_to_throw:  
            target_hit = False
            # check if a target (co2-source) is hit
            for t in gP.targets:
                if ( f.gY() <= t.gY()+t.gH() ) and  ( f.gX()+f.gW() >= t.gX() and f.gX() < t.gX()+t.gW() ):
                    target_hit = True
                    gP.species_saved += 1
                    r = ran.randrange(0, len(gP.things_hit_images))
                    gP.co2_sources_gone.append(an_obj(f.gX(), f.gY(), 50, 50, gP.things_hit_images[r], 0))
                    gP.targets.remove(t)
                    gP.things_to_throw.remove(f)
                    break
            # if still on playing-field contionue throwing-animation
            if not target_hit:
                if f.gY() < 0:
                    gP.things_to_throw.remove(f)
                else: 
                    draw_image(f.gImage(), f.gX(), f.gY()-f.gH(), gameDisplay)
                    f.sY(f.gY()-20)
                    f.sState(f.gState()+1)

        # Targets
        for t in gP.targets:
            for o in gP.obstacles:  
                # check if target hits an obstacle
                #if t.gY() >= gP.y_max + (player.gH() - o.gH()) and (t.gX() + t.gW() >= o.gX() and t.gX() <= o.gX() + o.gW()):
                if t.gY() >= gP.y_max - o.gH() + 50 and (t.gX() + t.gW() >= o.gX() and t.gX() <= o.gX() + o.gW()):
                    hit_obstacle = True
                    gP.targets.remove(t)
                    gP.co2_sources_gone.append(an_obj(t.gX(), t.gY(), 50, 50, gP.co2_images, 0))
                    gP.lives -= 1
                    break
                else:
                    hit_obstacle = False

            if not hit_obstacle:
                # check y- and x-coordinates of target and player, ycheck so that you can jump over a target without getting hit
                if (t.gY() >= player.gY() and t.gY() < player.gY() + player.gH()) and  (t.gX() > player.gX() and t.gX() < player.gX() + player.gW()):
                    gP.lives = 0
                # falling
                elif t.gY() + 5 < gP.y_max+player.gH()-t.gH():
                    t.sY(t.gY()+5)
                    draw_image(t.gImage(), t.gX()-t.gW(), t.gY()-t.gH(), gameDisplay)
                    t.sState(t.gState()+1)
                # hits ground
                else:
                    if gP.lives > 0:
                        gP.lives -= 1
                    gP.co2_sources_gone.append(an_obj(t.gX(), t.gY(), 50, 50, gP.co2_images, 0))
                    gP.targets.remove(t)

        # chose game-character matching the current movement
        choosefig(player, gameDisplay, cou, gP)    

        # draw obstacles, '+20'-width found by trial to look better
        [draw_image(o.gImage(), o.gX(), o.gY()+20, gameDisplay) for o in gP.obstacles]

        # draw saved animals/ continue animation or quit the animation when all sequences done, '+20'-width found to look better
        for s in gP.co2_sources_gone:
            if s.gState() == s.gNImages()-1:
                gP.co2_sources_gone.remove(s)
            else:
                draw_image(s.gImage(), s.gX()-10, s.gY()-10, gameDisplay)
                s.sState(s.gState()+1)

        # show stats
        draw_image(gP.counter_co2_images[str(gP.lives*60)], 500, 0, gameDisplay)
        draw_image(gP.counter_fruits_images[str(gP.fruits_left)], 500, 100, gameDisplay)
        draw_image(gP.rescued_species_image[0], 500, 200, gameDisplay)
        textsurface = myfont.render(str(gP.species_saved), False, (0, 0, 0))
        gameDisplay.blit(textsurface,(545,275))

        if gP.draw_text:
            draw_image(gP.earth_overheated_images[r_num], 150, 250, gameDisplay)



        if len(gP.hidden_texts) > 0:
            message_display(gameDisplay, gP.hidden_texts[0])

        pg.display.update()
        
        # number of FPS at which the game ist running
        clock.tick(gP.FPS)

        if gP.lives < 1 and not gP.draw_text:
            gP.draw_text = True
            r_num = ran.randrange(0, len(gP.earth_overheated_images))
            gP.FPS = 5
             

def main(): 
    """
    Idee: Try/Catch für Entscheidung ob mit JoyStick oder Tastatur?
    Oder Menü-Auswahl?
    """ 
    pg.init()

    pg.font.init()
    myfont = pg.font.SysFont('Comic Sans MS', 30)
    
    gP = gameParams()
    colors = Colors()

    clock = pg.time.Clock()
    
    # import all necessary images/frames for the animations and things that are displayed
    load_Images(gP, pg)

    gameDisplay = pg.display.set_mode((gP.disp_wdth, gP.disp_hght))
    #gameDisplay.fill(colors.getColor('blue'))
    draw_image(gP.background_image[0], 0, 0, gameDisplay)
    pg.display.set_caption('Hide the pain EARTH')

    # initialise player-figure
    player = an_obj(0,  gP.y_max-100, 80,  80, gP.stand_images, 0)
    
    # calculate parameters for pyhsical simulation of a jump with specified boundary-conditions (max. time and jumping-height)
    (a,v0) = calcAandV0(.5, gP.jumpheight)
    
    # place an obstacle at a random position, '+20'-width found by trial to look better
    xPosBloc = ran.randrange(gP.disp_wdth/3, (2/3)*gP.disp_wdth)
    gP.obstacles.append(an_obj(xPosBloc, gP.y_max, 90, 60, gP.obstacle_images, 0))
    [draw_image(o.gImage(), o.gX(), gP.y_max+player.gH()-o.gH(), gameDisplay) for o in gP.obstacles]

    # set starting-position of player
    draw_image(player.gImage(), player.gX(), player.gY(), gameDisplay) 

    
    game_loop(myfont, gP, clock, gameDisplay, player, a, v0, colors)

    # Spiel beenden und Programm verlassen 
    pg.quit()
    quit()


if __name__ == "__main__":
    main()