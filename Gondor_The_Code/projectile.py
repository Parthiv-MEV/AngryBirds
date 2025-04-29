import Gondor_The_Code.const as c
import pygame
import numpy as np
class Projectile:
    def __init__(self,num,x,y):
        self.num=int(num)
        self.name=c.refpro[self.num]
        self.x=x
        self.y=y
        self.vx=0
        self.vy=0
        self.pos=(x,y)
        self.oop=False
        self.rect = pygame.Rect(
        self.x - c.BIRD_SIZE_X // 2,
        self.y - c.BIRD_SIZE_Y // 2,    
        c.BIRD_SIZE_X,
        c.BIRD_SIZE_Y   
        )
        self.activated=0
        self.radius=(c.BIRD_SIZE_X+c.BIRD_SIZE_Y)//4 
        self.collides=0
        self.picked=False

    def damage(self,num):
        base=int(c.DMG*1.5) if self.num==num+1 else int(c.DMG*0.75)
        active_factor=self.activated+1 if self.num==1 else 1
        return (min(c.max_hp,(base+np.random.randint(-20,21))*active_factor)//((1+self.collides**2) if self.num!=2 else 1))
    
    def moveTo(self,x, y):
        self.x=x
        self.y=y
        self.pos=(self.x,self.y)

    def move(self,dx,dy):
        self.x+=dx
        self.y+=dy
        self.pos=(self.x,self.y)

    def sideBounce(self):
        self.vx = -1*self.vx * c.BOUNCINESS
        self.vy = self.vy * c.FRICTION
        self.collides+=1
    def upBounce(self):
        self.vy = -1*self.vy * c.BOUNCINESS
        self.vx = self.vx * c.FRICTION
        self.collides+=1
    def cornerBounce(self):
        self.vy = -1*self.vy * c.BOUNCINESS
        self.vx = -1*self.vx * c.BOUNCINESS
        self.collides+=1

    def activate(self, lotr=False):
        if self.num==3 and self.collides==0:
            self.vx=0
            self.vy=0   
        if self.num==1 and not lotr and self.collides==0 and self.activated==0:
            self.vx*=2
            self.vy*=2       
        if self.num==1 and lotr and self.activated<2 and self.collides<2:
            self.vx*=2
            self.vy*=1.5
        if self.num==2 and lotr and self.activated<2:
            if self.collides==0:
                self.vy*=2
                self.vx*=0.6
                if self.vy>0:
                    self.vy=-0.9*(self.vy)
            if self.collides==1 or self.collides==2:
                self.vx*=-0.9
                if self.vy>0:
                    self.vy=-(self.vy)

        self.activated+=1
        
