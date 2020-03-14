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
    
def draw_bloc(color, colors, xcoor, ycoor, wdth, hgth, pg, gameDisplay):
    pg.draw.rect(gameDisplay, colors.getColor(color), [xcoor, ycoor, wdth, hgth])
    
def draw_image(bl, x, y, gameDisplay):
        gameDisplay.blit(bl, (x,y))

def load_Images(gP, pg):
    # for c in range(1,13):
    #     im = pg.transform.scale(pg.image.load('./images/explosion/' + str(c) + '.png'), (50, 50))
    #     gP.explosion_images.append(im)
    paths = ('explosion', 'earth_stand', 'earth_throw', 'earth_walk', 'earth_jump', 'earth_fall')
    params = (gP.explosion_images, gP.stand_images, gP.throw_images, gP.walk_images, gP.jump_images, gP.fall_images)
  
    for c in range(0, len(paths)):
        path = './Images/' + paths[c] +'/'
        image_files = fnmatch.filter(os.listdir(path), '*.png')
        if c == 0:
            size = (50,50)
        else:
            size = (100, 100)
        [params[c].append(pg.transform.scale(pg.image.load(path + image_file), size)) for image_file in image_files]

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
        self.bloc_width = 90
        
        self.onObstacle = False

        self.lasers = []
        self.targets = []
        self.explosions = []
        self.explosion_images = []

        self.stand_images = []
        self.throw_images = []
        self.walk_images = []
        self.jump_images = []
        self.fall_images = []

        self.throw_up = False

        self.lives = 10

        self.targetWidth = 20

    def gTargetWidth(self):
        return self.targetWidth
        
class Obstacle():
    def __init__(self, xstart, xstop, height, color):
        self._xstart = xstart
        self._xstop = xstop
        self._height = height
        self._color = color
    
    # Getter
    def gXStart(self):
        return self._xstart
    def gXStop(self):
        return self._xstop
    def gHeight(self):
        return self._height
    def gColor(self):
        return self._color
    
    # Setter
    def sXStart(self, xstart):
        self._xstart = xstart
    def sXStop(self, xstop):
        self._xstop = xstop
    def sHeight(self, height):
        self._height = height
    def sColor(self, color):
        self._color = color

class Laser():
    def __init__(self, xpos, ypos, color):
        self.xpos = xpos
        self.ypos = ypos
        self.color = color
        self.wdth = 5
        self.hght = 30

    def gX(self):
        return self.xpos
    def gY(self):
        return self.ypos
    def gCol(self):
        return self.color
    def gWdth(self):
        return self.wdth
    def gHght(self):
        return self.hght

    def sY(self, y):
        self.ypos = y

class Target():
    def __init__(self, xpos, ypos, color, gP):
        self.xpos = xpos
        self.ypos = ypos
        self.color = color
        self.wdth = gP.gTargetWidth()
        self.hght = 20

    def gX(self):
        return self.xpos
    def gY(self):
        return self.ypos
    def gCol(self):
        return self.color
    def gWdth(self):
        return self.wdth
    def gHght(self):
        return self.hght

    def sY(self, y):
        self.ypos = y

class Explosion():
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.state = 0
    
    def sState(self, state):
        self.state = state
    
    def gState(self):
        return self.state
    
    def gX(self):
        return self.x
    def gY(self):
        return self.y

class Player():
    def __init__(self, image, wdth, hght, y_max):
        self.image = image
        self.x_coor = 0
        self.y_coor = y_max - hght
        self.hght = hght
        self.wdth = wdth

    def gX(self):
        return self.x_coor
    def gY(self):
        return self.y_coor
    def gImage(self):
        return self.image
    def gWdth(self):
        return self.wdth
    def gHght(self):
        return self.hght

    def sX(self, x):
        self.x_coor = x
    def sY(self, y):
        self.y_coor = y
    def sImage(self, image):
        self.image = image
