import fnmatch
import os

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
                        t.append(pg.transform.rotate(pg.transform.scale(pg.image.load(path + image_file), sizes[c]), -c2*18))
                    else:
                        t.append(pg.transform.rotate(pg.transform.scale(pg.image.load(path + image_file), sizes[c]), c2*18))
                params[c].append(t)
        elif c == 11 or c == 12:
            for image_file in image_files:
                im = image_file.replace(".png", "")
                params[c][im] = pg.transform.scale(pg.image.load(path + image_file), sizes[c])
        elif c == 15:
            for image_file in image_files:
                if image_file == 'how_to.png':
                    params[c][image_file.replace(".png", "")] = pg.transform.scale(pg.image.load(path + image_file), sizes[c][0])
                else:
                    params[c][image_file.replace(".png", "")] = pg.transform.scale(pg.image.load(path + image_file), sizes[c][1])
        else:
            [params[c].append(pg.transform.scale(pg.image.load(path + image_file), sizes[c])) for image_file in image_files]
            #[print(image_file) for image_file in image_files]

class gameParams():
    def __init__(self):
        self.disp_wdth = 600
        self.disp_hght = 600
        
        # needs to be set to a value that is convenient for you (in my case 20-60
        # depending on the computer I use)
        self._FPS = 15
        
        # ground-level
        self.y_max = self.disp_hght - 100
    
        # time-parameter for jump-simulation
        self.t = 0
    
        # parameters for movement of player
        self.step_size = 6
        self.xchange = 0
        self.ychange = 0
        self.jump = False
        self.jumpheight = 100
        self.jumpstep = 5
        self.onGround = True
        self.mr = False
        self.ml = False
        self.start_jump = False
        
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
    