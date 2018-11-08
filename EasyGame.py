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
        self.objects = []
    def update(self):
        root.update()
        for i in self.objects:
            i.update()

game = Game()

class Enviroment:
    def __init__(self,sizex,sizey):
        self.sizex = sizex
        self.sizey = sizey
        self.rectsizex = screenWidth/sizex
        self.rectsizey = screenHeight/sizey

        self.enviroment = []
        i = 0
        while i < self.sizex:
            q = 0
            x = []
            while q < self.sizey:
                x.append(1)
                q += 1

            self.enviroment.append(x)
            i += 1
    def render(self):
        canvas.delete(ALL)
        i = 0
        while i < self.sizex-1:
            q = 0
            while q < self.sizey-1:
                if self.enviroment[i][q] == 1:
                    canvas.create_rectangle((i-1)*self.rectsizex,(q-1)*self.rectsizey,i*self.rectsizex,q*self.rectsizey,fill = 'gold')
                q += 1
            i += 1

enviroment = Enviroment(100,100)
enviroment.render()
class Player:
    def __init__(self,jumpKeys,jumpDownKeys,leftKeys,rightKeys):
        self.x = screenWidth/2
        self.y = screenHeight/2
        self.speedx = screenWidth/30
        self.speedy = screenHeight/30
        self.size = screenWidth/100

        self.gravTime = time() - game.startTime
        self.gravMod = 1

        self.jumpup = False
        self.jumpdown = False
        self.left = False
        self.right = False

        self.jumpUpKeys = jumpKeys
        self.leftKeys = leftKeys
        self.rightKeys = rightKeys
        self.jumpDownKeys = jumpDownKeys

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
        if event.keysym in self.jumpUpKeys:
            self.jumpup = True
        if event.keysym in self.jumpDownKeys:
            self.jumpdown = True

    def keyRelease(self,event):
        if event.keysym in self.leftKeys:
            self.left = False
        if event.keysym in self.rightKeys:
            self.right = False
        if event.keysym in self.jumpUpKeys:
            self.jumpup = False
        if event.keysym in self.jumpDownKeys:
            self.jumpdown = False

    def move(self):
        if self.left:
            self.x -= self.speedx
        if self.right:
            self.x += self.speedx
        if self.jumpup:
            self.y -= self.speedy
        if self.jumpdown:
            self.y += self.speedy

    def render(self):
        canvas.delete(self.graphics)
        self.graphics = canvas.create_rectangle(self.x + self.size,self.y + self.size,self.x - self.size,self.y - self.size, fill = 'red')

    def collision(self):
        if self.x - self.size < 0:
            self.x += self.speedx

        if self.x + self.size > screenWidth:
            self.x -= self.speedx

        if self.y - self.size < 0:
            self.y += self.speedy

        if self.y + self.size > screenHeight:
            self.y -= self.speedy
    def update(self):
        self.move()
        self.collision()
        self.render()

player = Player(['w'],['s'],['a'],['d'])
game.objects.append(player)
while game.playgame:
    game.update()
