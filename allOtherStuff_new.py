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
    
def mv_bloc(bl, x, y, gameDisplay):
        gameDisplay.blit(bl, (x,y))

class gameParams():
    def __init__(self):
        self.disp_wdth = 600
        self.disp_hght = 600
    
        self.FPS = 60
        
        # "Bodenhöhe"
        self.y_max = self.disp_hght - 100
    
        # Startkoordinaten
        self.xcoor = 0
        self.ycoor = self.y_max
    
        self.t = 0
    
        self.step_size = 3
        self.xchange = 0
        
        self.jump = False
    
        self.jumpheight = 100
        self.jumpstep = 5
    
        self.onGround = True
        self.mr = False
        self.ml = False
        self.start_jump = False
        
        self.aboveObstacle = False
        
        self.obstacles = []
    
        # Parameter, wenn gameDisplay geschlossen wird
        self.quitGame = False
    
        self.bloc_height = 60
        self.bloc_width = 90
        
        self.onObstacle = False

        self.lasers = []
        self.targets = []
        self.explosions = []
        self.explosion_images = []

        self.lives = 10

        self.car_width = 0

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

