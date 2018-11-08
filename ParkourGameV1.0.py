try:
    from tkinter import *
except:
    from Tkinter import *

from time import *

root = Tk()

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

canvas = Canvas(root,width = screenWidth, height = screenHeight)
canvas.pack()

class Game:
    def __init__(self):
        self.playgame = True
        self.startTime = time()
        self.time = self.startTime

        self.objects = []
    def update(self):
        root.update()
        self.time = time() - self.startTime
        for i in self.objects:
            i.update()
        enviroment.render()
game = Game()
class Enviroment:
    def __init__(self,sizex,sizey,viewSizeX,viewSizeY):
        self.sizex = sizex
        self.sizey = sizey
        self.viewSizeX = viewSizeX
        self.viewSizeY = viewSizeY
        self.viewArea = viewSizeX / 2
        self.rectsizex = screenWidth/self.viewSizeX
        self.rectsizey = screenHeight/self.viewSizeY
        self.enviroment = []

        i = 0
        while i < self.sizex:
            x = []
            q = 0
            while q < self.sizey:
                x.append(0)
                q += 1
            self.enviroment.append(x)
            i += 1
    def set_block(self,x,y,on = 1):
        self.enviroment[x-1][y-1] = on
        self.render()
    def render(self):
        canvas.delete(ALL)
        i = 0
        while i < self.sizex:
            x = []
            q = 0
            while q < self.sizey:
                if self.enviroment[i][q] == 1 and i < self.viewArea + self.viewSizeY/2:
                    canvas.create_rectangle(self.rectsizex*i,self.rectsizey*(( self.viewArea + self.viewSizeY/2) - q),self.rectsizex*(i+1),self.rectsizey*((( self.viewArea + self.viewSizeY/2) - q)+1),fill = 'blue')

                q += 1
            i += 1
        for i in game.objects:
            i.update()

enviroment = Enviroment(10,100,10,10)
enviroment.set_block(1,5)
class Player:
    def __init__(self,jumpKeys,leftKeys,rightKeys):
        self.x = screenWidth/2
        self.y = screenHeight/2
        self.speedx = screenWidth/75
        self.speedy = screenHeight/30
        self.size = screenWidth/100

        self.lastSpotY = 100

        self.gravTime = game.time - game.startTime
        self.gravMod = 1

        self.jump = False
        self.jumpable = True
        self.left = False
        self.right = False

        self.jumpKeys = jumpKeys
        self.leftKeys = leftKeys
        self.rightKeys = rightKeys

        self.collidersy = [[screenHeight - self.size,screenHeight]]
        self.collidersx = []

        self.graphics = canvas.create_rectangle(self.x + self.size,self.y + self.size,self.x - self.size,self.y - self.size, fill = 'red')

        root.bind('<KeyPress>',self.keyPress,add = '+')
        root.bind('<KeyRelease>',self.keyRelease,add = '+')

    def keyPress(self,event):
        if event.keysym in self.leftKeys:
            self.left = True
        if event.keysym in self.rightKeys:
            self.right = True
        if event.keysym in self.jumpKeys:
            self.jump = True

    def keyRelease(self,event):
        if event.keysym in self.leftKeys:
            self.left = False
        if event.keysym in self.rightKeys:
            self.right = False
        if event.keysym in self.jumpKeys:
            self.jump = False

    def move(self):
        spoty = int((self.y + self.size)/enviroment.rectsizey)
        if spoty < self.lastSpotY:
            enviroment.viewArea += 1
        if spoty > self.lastSpotY:
            enviroment.viewArea -= 1

        if self.left and self.x - self.size > 0:
            self.x -= self.speedx
        if self.right and self.x + self.size * 4 < screenWidth:
            self.x += self.speedx
        if self.jump and self.jumpable and self.y - self.size > 0:
            self.y -= self.speedy
        self.lastSpotY = spoty
    def gravity(self):
        gravity = False
        spoty = int((self.y + self.size)/enviroment.rectsizey)
        spotx = int((self.x + self.size)/enviroment.rectsizex)

        if game.time - self.gravTime > 3 and game.time - self.gravTime < 5:
            self.gravMod = 5
            self.jumpable = False

        elif game.time - self.gravTime > 5:
            self.jumpable = True
            self.gravMod = 1
            self.gravTime = game.time
        i = 0
        #while i < len(self.collidersy):
            #if not (int(self.y/self.speedy) < int(self.collidersy[i][0]//self.speedy) and int(self.y//self.speedy) > int(self.collidersy[i][1]//self.speedy)):
        if not self.y + self.size*3 > screenHeight and (not enviroment.enviroment[spotx][spoty] == 1) :
            gravity = True
        elif self.y + self.size*3 > screenHeight:
            self.y = screenHeight - self.size*3 + 1
        #    i += 1

        if gravity:
            self.y += (self.speedy/2)*self.gravMod

    def render(self):
        canvas.delete(self.graphics)
        self.graphics = canvas.create_rectangle(self.x + self.size,self.y + self.size,self.x - self.size,self.y - self.size, fill = 'red')

    def update(self):
        self.gravity()
        self.move()
        self.render()

player = Player(['w','s'],['a'],['d'])
game.objects.append(player)
enviroment.render()

while game.playgame:
    game.update()
