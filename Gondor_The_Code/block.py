import Gondor_The_Code.const as c
import random
import pygame
from Gondor_The_Code.texturegenerator import *
class Block:
    def __init__(self,num,x,y):
        self.num=num
        self.falling=False
        self.grounded=False
        self.botrow=False
        self.below=None
        self.x=x
        self.y=y
        self.vy=0
        self.g=c.BLK_G
        self.name=c.refblock[num]
        self.hp=c.max_hp
        self.broken=False
        self.color=list(c.COLORS[num])
        self.outline=c.OUTLINES[num]
        for i in range(3): #Adding slight color variation
            self.color[i]=min(255, max(0, self.color[i] + random.randint(-c.COLVAR, c.COLVAR)))
        self.color=tuple(self.color)
        self.rect = pygame.Rect(
            self.x - c.BLOCKSIZE[0] // 2,
            self.y - c.BLOCKSIZE[1] // 2,
            c.BLOCKSIZE[0],
            c.BLOCKSIZE[1]
            )
        self.crack_texture=None
        self.scaled_crack=None
        self.texture=None
        self.scaled_texture=None

    def hit(self,dmg):
        old_intensity=1-(self.hp/c.max_hp)
        self.hp-=dmg
        if self.crack_texture is not None:
            self.crack_texture=TextureGenerator.upgrade_crack_texture(self.crack_texture,old_intensity,1-(self.hp/c.max_hp))
        else:
            self.crack_texture=TextureGenerator.create_crack_texture(1-(self.hp/c.max_hp))
        self.scaled_crack = pygame.transform.scale(self.crack_texture, (c.BLOCKSIZE[0], c.BLOCKSIZE[1]))



        


    