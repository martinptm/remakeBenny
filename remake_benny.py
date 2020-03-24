import numpy as np
import pygame as pg
import random as ran
import time
import ptext

from allotherstuff import Colors, GameParams, AnObj
from allotherstuff import draw_image, load_images, handle_event
from methods.calcjumpparams import calc_a_and_v0

def choosefig(player, gameDisplay, cou, gP):
    """
    Choose correct type of player-figure according to its current
    movement/action.
    """
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
    # increase state to choose next frame from the matching sequence of 
    # images according to the current movement
    player.sState(player.gState()+1)
    draw_image(player.gImage(), player.gX(), player.gY(), gameDisplay)

def message_display(gameDisplay, hidden_text):
    """ Show an eastereg-text.
    """
    ptext.draw(hidden_text.gText(), hidden_text.gPos(), 
    		  color=hidden_text.gColor(), fontsize=hidden_text.gSize())


def game_loop(myfont, gP, clock, gameDisplay, player, a, v0, colors):
    """ Iterate for every frame in the game.
    """
    # counter to track iterations of frames in the game loop
    cou = 0
    # game loop
    while not gP.quitGame:
        cou += 1

        if gP.get_lives() > 0:
            # increase fruits in basket regulary
            if cou%30 == 0 and gP.fruits_left < 6:
                gP.fruits_left += 1

            # rate of appearance increases with more succes in the game 
            # (small level of uncertainty comes into play ;D)
            r = ran.randrange(0, 8)
            if cou+r >= 70 or (gP.species_saved >= 5 and cou+r >= 50):
                target_nr = ran.randrange(0, len(gP.target_images))
                gP.targets.append(AnObj(ran.randrange(0, gP.disp_wdth - 20),
                				  0, 20, 20, gP.target_images[target_nr], 0))
                cou = 0
        
        # check if player is at lowes possible point 
        if player.gY() == gP.y_max:
            gP.onGround = True
        else:
            gP.onGround = False
            
        # detect and handle user-input and set movement accordingly
        for event in pg.event.get():
            gP = handle_event(player, event, pg, gP, colors)      
        if gP.onGround or (gP.at_x_of_obst and not gP.jump):
            if gP.start_jump:
                gP.jump = True
            if gP.mr:
                gP.xchange = gP.step_size
            elif gP.ml:
                gP.xchange = -gP.step_size
            else:
                gP.xchange = 0

        # check if player interacts with the obstacle, '-20' to look 
        # better
        for c in range(0, len(gP.obstacles)):
            if (player.gX() + gP.xchange > gP.obstacles[c].gX() - player.gW() 
            		and player.gX() + gP.xchange < gP.obstacles[c].gX()
            			 + gP.obstacles[c].gW() -20):
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
                if player.gY() < gP.y_max - gP.obstacles[c].gH() + 10:
                    pass
                # jump from obstacle
                elif gP.start_jump and gP.ychange==0:
                    pass
                # land and stand on the obstacle, reset t so if the 
                # obstacle is left, the physical fall/jump-simualtion 
                # is correct
                elif (player.gY() - gP.ychange <= 
                      gP.y_max -gP.obstacles[c].gH() + 10
                		and gP.ychange >= 0):
                    player.sY(gP.y_max - gP.obstacles[c].gH() + 10)
                    gP.t = 0
                    gP.jump = False
                    gP.ychange = 0
                # bounce off obstacle-side
                else: 
                    gP.xchange = - gP.xchange

        # limits of playing-field, '-10' to look better
        if (player.gX() + gP.xchange <= gP.disp_wdth - player.gW() 
        		and player.gX() + gP.xchange >= 0-15):
            player.sX(player.gX() + gP.xchange)
        elif not gP.onGround:
            gP.xchange = - gP.xchange

        # jump-simulation (independent of starting point since change 
        # of position and not the absolute position is calculated)
        if gP.jump:  
            gP.t += 1/gP.get_FPS()    
            gP.ychange =  1/gP.get_FPS() * (-v0 + a*gP.t)
            player.sY(player.gY() + gP.ychange)   
            # land on the ground 
            if player.gY() > gP.y_max:
                player.sY(gP.y_max)
                gP.jump = False
                gP.t = 0
                gP.ychange = 0

        # if player stood on obstacle and now leaving it. No initial 
        # jump, only falling down.
        if not gP.jump and not gP.at_x_of_obst  and player.gY() < gP.y_max:
            gP.t += 1/gP.get_FPS()
            gP.ychange =  1/gP.get_FPS() * (a*gP.t) 
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
                if (f.gY() <= t.gY()+t.gH() 
                        and f.gX()+f.gW() >= t.gX()
                		and f.gX() < t.gX()+t.gW()):
                    target_hit = True
                    gP.species_saved += 1
                    r = ran.randrange(0, len(gP.things_hit_images))
                    gP.co2_sources_gone.append(AnObj(f.gX(), f.gY(), 
                    						   50, 50,
                    						   gP.things_hit_images[r], 0))
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
                if (t.gY() >= gP.y_max - o.gH() + 50 
                		and t.gX() + t.gW() >= o.gX() 
                		and t.gX() <= o.gX() + o.gW()):
                    hit_obstacle = True
                    gP.targets.remove(t)
                    gP.co2_sources_gone.append(AnObj(t.gX(), t.gY(), 
                    						   50, 50, gP.co2_images, 0))
                    gP.set_lives(gP.get_lives()-1)
                    break
                else:
                    hit_obstacle = False

            if not hit_obstacle:
                # check y- and x-coordinates of target and player, 
                # ycheck so that you can jump over a target without 
                # getting hit
                if (t.gY() >= player.gY() 
                		and t.gY() < player.gY() + player.gH()
                		and t.gX() > player.gX() 
                		and t.gX() < player.gX() + player.gW()):
                    gP.set_lives(0)
                # falling
                elif t.gY() + gP.obj_fall_step < gP.y_max+player.gH()-t.gH():
                    t.sY(t.gY()+gP.obj_fall_step)
                    draw_image(t.gImage(), t.gX()-t.gW(), t.gY()-t.gH(), 
                    		   gameDisplay)
                    t.sState(t.gState()+1)
                # hits ground
                else:
                    gP.set_lives(gP.get_lives()-1) 
                    gP.co2_sources_gone.append(AnObj(t.gX(), t.gY(), 50, 50, 
                    						   gP.co2_images, 0))
                    gP.targets.remove(t)

        # chose game-character matching the current movement
        choosefig(player, gameDisplay, cou, gP)    

        # draw obstacles, '+20'-width found by trial to look better
        for o in gP.obstacles:
            draw_image(o.gImage(), o.gX(), o.gY(), gameDisplay) 
            o.sState(o.gState()+1)

        # draw saved animals/ continue animation or quit the animation
        # when all sequences done, '+20'-width found to look better
        for s in gP.co2_sources_gone:
            if s.gState() == s.gNImages()-1:
                gP.co2_sources_gone.remove(s)
            else:
                draw_image(s.gImage(), s.gX()-10, s.gY()-10, gameDisplay)
                s.sState(s.gState()+1)

        # show stats
        draw_image(gP.counter_co2_images[str(gP.get_lives()*60)], 500, 0, 
        		   gameDisplay)
        draw_image(gP.counter_fruits_images[str(gP.fruits_left)], 500, 100, 
        		   gameDisplay)
        draw_image(gP.rescued_species_image[0], 500, 200, gameDisplay)
        draw_image(gP.help_images[gP.help_image], 10, 10, gameDisplay)
        textsurface = myfont.render(str(gP.species_saved), False, (0, 0, 0))
        gameDisplay.blit(textsurface,(545,275))

        if gP.draw_text:
            draw_image(gP.earth_overheated_images[r_num], 150, 250, 
            	       gameDisplay)



        if len(gP.hidden_texts) > 0:
            message_display(gameDisplay, gP.hidden_texts[0])

        pg.display.update()
        
        # number of FPS at which the game ist running
        clock.tick(gP.get_FPS())

        # slow down speed an display game-finished-text from now on 
        if gP.get_lives() < 1 and not gP.draw_text:
            gP.draw_text = True
            r_num = ran.randrange(0, len(gP.earth_overheated_images))
            gP.set_FPS(5)
             

def start_game(): 
    """
    Idee: Try/Catch für Entscheidung ob mit JoyStick oder Tastatur?
    Oder Menü-Auswahl?
    """ 
    pg.init()

    pg.font.init()
    myfont = pg.font.SysFont('Comic Sans MS', 30)
    
    gP = GameParams()
    colors = Colors()

    clock = pg.time.Clock()
    
    # import all necessary images/frames for the animations and things 
    # that are displayed
    load_images(gP, pg)

    gameDisplay = pg.display.set_mode((gP.disp_wdth, gP.disp_hght))
    #gameDisplay.fill(colors.getColor('blue'))
    draw_image(gP.background_image[0], 0, 0, gameDisplay)
    pg.display.set_caption('Hide the pain EARTH')

    # initialise player-figure
    player = AnObj(0,  gP.y_max-100, 80,  80, gP.stand_images, 0)
    
    # calculate parameters for pyhsical simulation of a jump with 
    # specified boundary-conditions (max. time and jumping-height)
    (a,v0) = calc_a_and_v0(1, gP.jumpheight)
    
    # place an obstacle at a random position, '+20'-width found by 
    # trial to look better
    xPosBloc = ran.randrange(gP.disp_wdth/3, (2/3)*gP.disp_wdth)
    gP.obstacles.append(AnObj(xPosBloc, gP.y_max-10, 90, 60, 
    					gP.obstacle_images, 0))
    for o in gP.obstacles:
	    draw_image(o.gImage(), o.gX(), 
                  gP.y_max+player.gH()-o.gH(), gameDisplay) 

    # set starting-position of player
    draw_image(player.gImage(), player.gX(), player.gY(), gameDisplay) 

    # actual game and user-interactions in here
    game_loop(myfont, gP, clock, gameDisplay, player, a, v0, colors)

    # quit game and exit program 
    pg.quit()
    quit()


if __name__ == "__main__":
    start_game()