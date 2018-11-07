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
        self.speedx = screenWidth/30
        self.speedy = screenHeight/30
        self.size = screenWidth/100

        self.jump = False
        self.left = False
        self.right = False

        self.jumpKeys = jumpKeys
        self.leftKeys = leftKeys
        self.rightKeys = rightKeys

        self.collidersy = [screenHeight - self.size]
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

        i = 0
        while i < len(self.collidersy):
            if not (self.y + self.size*2 > self.collidersy[i] and self.y < self.collidersy[i]):
                gravity = True
            i += 1

        if gravity:
            self.y += self.speedy/2

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
