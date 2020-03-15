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
        # Scheinbar kann mit .get() und [] auf Elemente in einem Dictionary
        # zugegriffen werden.
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
    
#def draw_bloc(color, colors, xcoor, ycoor, wdth, hgth, pg, gameDisplay):
#    pg.draw.rect(gameDisplay, colors.getColor(color), [xcoor, ycoor, wdth, hgth])
    
def draw_image(bl, x, y, gameDisplay):
        gameDisplay.blit(bl, (x,y))

def load_Images(gP, pg):
    paths = ('co2',
        'earth_stand', 
        'earth_throw', 
        'earth_walk', 
        'earth_jump', 
        'earth_fall', 
        'obstacles', 
        'things_throw',
        'targets',
        'things_hit')
    params = (gP.co2_images,
        gP.stand_images, 
        gP.throw_images, 
        gP.walk_images, 
        gP.jump_images, 
        gP.fall_images,
        gP.obstacle_images,
        gP.things_throw_images,
        gP.target_images,
        gP.things_hit_images)
    sizes = ((50,50),
            (100,100),
            (100,100),
            (100,100),
            (100,100),
            (100,100),
            (90,60),
            (20,20),
            (50,50),
            (50,50)) 
    for c in range(0, len(paths)):
        path = './Images/' + paths[c] +'/'
        image_files = fnmatch.filter(os.listdir(path), '*.png')
        if c == 7 or c == 8 or c == 9: 
            for image_file in image_files:
                t = []
                for c2 in range(0,20): 
                    #print("image_file: ", image_file)
                    if image_file == ('parrot.png'):
                        print("BBBBBBIIIIIRRRRD")
                        t.append(pg.transform.rotate(pg.transform.scale(pg.image.load(path + image_file), sizes[c]), -c2*18))
                    else:
                        t.append(pg.transform.rotate(pg.transform.scale(pg.image.load(path + image_file), sizes[c]), c2*18))
                params[c].append(t)
        else:
            [params[c].append(pg.transform.scale(pg.image.load(path + image_file), sizes[c])) for image_file in image_files]

class gameParams():
    def __init__(self):
        self.disp_wdth = 600
        self.disp_hght = 600
    
        self.FPS = 60
        
        # "Bodenhöhe"
        self.y_max = self.disp_hght - 100
    
        self.t = 0
    
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
        
        self.aboveObstacle = False
        self.obstacles = []
        self.at_x_of_obst = False
    
        # Parameter, wenn gameDisplay geschlossen wird
        self.quitGame = False
    
        self.bloc_height = 60
        self.bloc_width = 90-20
        
        self.onObstacle = False

        self.lasers = []
        self.targets = []
        self.explosions = []

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

        self.throw_up = False

        self.lives = 10

        self.targetWidth = 20

    def gTargetWidth(self):
        return self.targetWidth

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
        #print("self._images: ", self._images)
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
