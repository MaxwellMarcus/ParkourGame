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
class Player:
    def __init__(self,jumpKeys,leftKeys,rightKeys):
        self.x = screenWidth/2
        self.y = screenHeight/2
        self.speedx = screenWidth/30000
        self.speedy = screenHeight/3000
        self.size = screenWidth/100

        self.gravTime = time() - game.startTime
        self.gravMod = 1

        self.jump = False
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
        if self.left:
            self.x -= self.speedx
        if self.right:
            self.x += self.speedx
        if self.jump:
            self.y -= self.speedy

    def gravity(self):
        gravity = False
        if self.gravTime % 5 == 0:
            self.gravMod = 4
        elif self.gravTime % 7 == 0:
            self.gravMod = 1
            self.gravTime = 0
        i = 0
        while i < len(self.collidersy):
            if not (int(self.y/self.speedy) < int(self.collidersy[i][0]//self.speedy) and int(self.y//self.speedy) > int(self.collidersy[i][1]//self.speedy)):
                gravity = True
            i += 1

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
while game.playgame:
    game.update()
