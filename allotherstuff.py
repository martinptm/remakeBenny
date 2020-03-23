import fnmatch
import os
import random as ran

class Colors():
    def __init__(self):
        self.col = {'black': (0,0,0),
              'red':   (255,0,0),
              'green': (0,255,0),
              'blue':  (0,0,255)
              }
        
    def getColor(self, color):
        if color not in self.col:
            print("Farbe nicht verfügbar!, DEFAULT: red")
            returncolor = self.col.get('red')
        else:
            returncolor = self.col[color]
            
        return returncolor

def changeMoveDown(movedown):
    if movedown:
        return False
    else:
        return True
    
def draw_image(bl, x, y, gameDisplay):
        gameDisplay.blit(bl, (x,y))

def load_Images(gP, pg):
    # read in all frames needed in animations
    paths = ('background',
        'co2',
        'earth_stand', 
        'earth_throw', 
        'earth_walk', 
        'earth_jump', 
        'earth_fall', 
        'obstacles', 
        'things_throw',
        'targets',
        'things_hit',
        'counter_co2',
        'counter_fruits',
        'rescued_species',
        'earth_overheated',
        'help')
    params = (gP.background_image,
        gP.co2_images,
        gP.stand_images, 
        gP.throw_images, 
        gP.walk_images, 
        gP.jump_images, 
        gP.fall_images,
        gP.obstacle_images,
        gP.things_throw_images,
        gP.target_images,
        gP.things_hit_images,
        gP.counter_co2_images,
        gP.counter_fruits_images,
        gP.rescued_species_image,
        gP.earth_overheated_images,
        gP.help_images)
    sizes = ((600,600),
            (50,50),
            (100,100),
            (100,100),
            (100,100),
            (100,100),
            (100,100),
            (90,90),
            (20,20),
            (50,50),
            (50,50),
            (100,60),
            (100,60),
            (100,100),
            (300, 200),
            ((120,60), (300,300))) 
    for c in range(0, len(paths)):
        path = './Images/' + paths[c] +'/'
        image_files = fnmatch.filter(os.listdir(path), '*.png')
        if c == 8 or c == 9 or c == 10: 
            for image_file in image_files:
                t = []
                for c2 in range(0,20): 
                    if image_file == ('parrot.png'):
                        t.append(
                          pg.transform.rotate(
                          pg.transform.scale(pg.image.load(path + image_file), 
                          sizes[c]), -c2*18))
                    else:
                        t.append(
                          pg.transform.rotate(
                          pg.transform.scale(pg.image.load(path + image_file), 
                          sizes[c]), c2*18))
                params[c].append(t)
        elif c == 11 or c == 12:
            for image_file in image_files:
                im = image_file.replace(".png", "")
                params[c][im] = pg.transform.scale(
                              pg.image.load(path + image_file), sizes[c])
        elif c == 15:
            for image_file in image_files:
                if image_file == 'how_to.png':
                    params[c][image_file.replace(".png", "")] = (
                     pg.transform.scale(pg.image.load(path + image_file), 
                                        sizes[c][0]))
                else:
                    params[c][image_file.replace(".png", "")] = (
                     pg.transform.scale(pg.image.load(path + image_file), 
                                        sizes[c][1]))
        else:
            for image_file in image_files:
                params[c].append(
                  pg.transform.scale(pg.image.load(path + image_file), 
                                     sizes[c])) 
            #[print(image_file) for image_file in image_files]

class gameParams():
    def __init__(self):
        self.disp_wdth = 600
        self.disp_hght = 600
        
        self._FPS = 20
        
        # ground-level
        self.y_max = self.disp_hght - 100
    
        # time-parameter for jump-simulation
        self.t = 0
    
        # parameters for movement of player
        self.step_size = 3
        self.xchange = 0
        self.ychange = 0
        self.jump = False
        self.jumpheight = 100
        self.jumpstep = 5
        self.onGround = True
        self.mr = False
        self.ml = False
        self.start_jump = False

        self.obj_fall_step = 2
        
        # parameters for interactions with obstacles
        self.aboveObstacle = False
        self.at_x_of_obst = False
    
        # parameter to quit game
        self.quitGame = False
        
        # lists for interacitve stuff except the player itself
        self.obstacles = []
        self.things_to_throw = []
        self.targets = []
        self.co2_sources_gone = []

        # lists and dicts to store all frames for animations
        self.background_image = []
        self.co2_images = []
        self.stand_images = []
        self.throw_images = []
        self.walk_images = []
        self.jump_images = []
        self.fall_images = [] 
        self.obstacle_images = []
        self.things_throw_images = []
        self.target_images = []
        self.things_hit_images = []
        self.counter_co2_images = {}
        self.counter_fruits_images = {}
        self.rescued_species_image = []
        self.earth_overheated_images = []
        self.help_images = {}

        # parameter if player throws a fruit
        self.throw_up = False
        # counter for GT of co2 left until 2° warming will be exceeded
        self._lives = 10
        #counter of fruits in basket
        self.fruits_left = 6
        # counter for saved species/ avoided co2-sources
        self.species_saved = 0

        self.hidden_texts = []

        self.draw_text = False

        self.help_image = 'how_to'

    def get_lives(self):
        return self._lives
    def set_lives(self, lives):
        if lives >=0:
            self._lives = lives
        else: 
            self._lives = 0

    def get_FPS(self):
        return self._FPS
    def set_FPS(self, FPS):
        self._FPS = FPS


class an_obj():
    def __init__(self, x, y, wdth, hght, images, state):
        self._x = x
        self._y = y
        self._wdth = wdth
        self._hght = hght
        self._images = images
        self._state = state
    
    # Getter
    def gX(self):
        return self._x
    def gY(self):
        return self._y
    def gW(self):
        return self._wdth
    def gH(self):
        return self._hght
    def gImage(self):
        return self._images[self._state]
    def gState(self):
        return self._state
    def gNImages(self):
        return len(self._images)
    
    # Setter
    def sX(self, x):
        self._x = x
    def sY(self, y):
        self._y = y
    def sW(self, wdth):
        self._wdth = wdth
    def sH(self, hght):
        self._hght = hght
    def sImages(self, images):
        self._images = images
    def sState(self, state):
        if state > len(self._images)-1:
            state = 0
        self._state = state

class hidden_text():
    def __init__(self, text, pos, size, color):
        self._text = text
        self._pos = pos
        self._size = size
        self._color = color

    def gText(self):
        return self._text
    def gPos(self):
        return self._pos
    def gSize(self):
        return self._size
    def gColor(self):
        return self._color

def handle_event(player, event, pg, gP, colors):
    # detect if gamewindow is closed or esc-key is pressed
    if event.type == pg.QUIT:
        gP.quitGame = True
    elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE: 
        gP.quitGame = True
         
    if gP.get_lives() > 0:       
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
                # throw things at left and right side of the player (extra 
                # shifts found by testing) 
                # (only possible if the player has 'fruits' to throw in his 
                # basket)
                r = ran.randrange(0, len(gP.things_throw_images))
                if gP.fruits_left > 0:
                    gP.fruits_left -= 1
                    gP.things_to_throw.append(an_obj(player.gX()+15, 
                                              player.gY(), 20, 20, 
                                              gP.things_throw_images[r], 0))
                if gP.fruits_left > 0:
                    gP.fruits_left -= 1
                    gP.things_to_throw.append(an_obj(player.gX()+player.gW(), 
                                              player.gY(), 20, 20, 
                                              gP.things_throw_images[r], 0))
                gP.throw_up = True

    if event.type == pg.MOUSEBUTTONDOWN:
        mouse_pos = event.pos  # gets mouse position
        if (mouse_pos[0] > gP.obstacles[0].gX() 
                and mouse_pos[0] < gP.obstacles[0].gX() + gP.obstacles[0].gW() 
                and mouse_pos[1] > 520 and mouse_pos[1] < 580):
            gP.hidden_texts.append(hidden_text(("Oh, someone left the engine "
                                                "running..."
                                                "\nAnyways:\nGo by bike!\n"
                                                "Better for you, better " 
                                                "for the environment."),
                                                (150, 400), 20, 
                                                colors.getColor('blue')))
        elif (mouse_pos[0] >  460 
                and mouse_pos[0] < 520 
                and mouse_pos[1] > 530 
                and mouse_pos[1] < 560):
            gP.hidden_texts.append(
              hidden_text("There is no planet B!", 
              (100, 100), 30, colors.getColor('green')))
        elif (mouse_pos[0] > 45 
                and mouse_pos[0] < 105 
                and mouse_pos[1] > 530 
                and mouse_pos[1] < 570):
            gP.hidden_texts.append(hidden_text(("What do we want?"
                                                "\nCLIMATE JUSTICE!"
                                                "\nWhen do we want it?"
                                                "\nNOW!"),
                                                (400, 300), 25,
                                                colors.getColor('red')))
    elif event.type == pg.MOUSEBUTTONUP and len(gP.hidden_texts) > 0:
        gP.hidden_texts.pop()

    if event.type == pg.MOUSEMOTION:
        mouse_pos = event.pos
        if (mouse_pos[0] > 10 
                and mouse_pos[0] < 130 
                and mouse_pos[1] > 10 
                and mouse_pos[1] < 70):
            gP.help_image = 'manual'
        else:
            gP.help_image = 'how_to'

    return gP
    