import numpy as np
from Gondor_The_Code.block import  *
import Gondor_The_Code.const as c
from Gondor_The_Code.texturegenerator import *

class Fortress:
    def __init__(self,x,y,map, p, lotr_theme):
        self.blocks = np.empty(c.FORTSIZE, dtype=object)
        self.block_map=(map if p==1 else np.flip(map, axis=1)).copy() 

        for i in range(c.FORTSIZE[0]):
            for j in range(c.FORTSIZE[1]):
                self.blocks[i,j]=Block(self.block_map[i,j],x+c.BLOCKSIZE[0]*j,y+c.BLOCKSIZE[1]*i)
                blk=self.blocks[i,j]
                if not lotr_theme:
                    if blk.num==0:
                        blk.texture=TextureGenerator.create_wood_texture()
                    elif blk.num==1:
                        blk.texture=TextureGenerator.create_ice_texture()
                    elif blk.num==2:
                        blk.texture=TextureGenerator.create_stone_texture()
                elif p==1:
                    if blk.num==0:
                        blk.texture=TextureGenerator.create_texture((200, 200, 220), "smooth_stone")
                    elif blk.num==1:
                        blk.texture=TextureGenerator.create_texture((240, 240, 220), "white_stone")
                    elif blk.num==2:
                        blk.texture=TextureGenerator.create_texture((220, 220, 220), "light_stone")
                else:
                    if blk.num==0:
                        blk.texture=TextureGenerator.create_texture((80, 80, 100), "rough_stone")
                    elif blk.num==1:
                        blk.texture=TextureGenerator.create_texture((100, 50, 50), "dark_red")
                    elif blk.num==2:
                        blk.texture=TextureGenerator.create_texture((50, 30, 30), "lava_stone") 
                blk.scaled_texture = pygame.transform.scale(blk.texture, (c.BLOCKSIZE[0], c.BLOCKSIZE[1]))
                


                
        