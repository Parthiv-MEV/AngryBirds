import pygame
import numpy as np
import random
import time
from math import dist as dist
from Gondor_The_Code.block import *
import Gondor_The_Code.const as c
from Gondor_The_Code.fortress import *
from Gondor_The_Code.projectile import *
from Gondor_The_Code.inputbox import *
from Gondor_The_Code.button import *
from Gondor_The_Code.togglebutton import *
from Gondor_The_Code.slider import *
from Gondor_The_Code.level_manager import *
from Gondor_The_Code.texturegenerator import *
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
pygame.key.set_repeat(400,50)
pygame.mixer.init()
MENU = 0
GAMEPLAY = 1
GAME_OVER = 2
SETTINGS=3
LEVEL_SELECT = 4
screen = pygame.display.set_mode(c.SCREEN) 
pygame.display.set_caption("Angry Birds PvP") 
SCALE=c.SCREEN_X/800
#  Font setup
ag_font_small = pygame.font.Font(r'Rohan_The_Refs\fonts\angrybirds-regular.ttf', int(20*(SCALE)))
ag_font_medium = pygame.font.Font(r'Rohan_The_Refs\fonts\angrybirds-regular.ttf', int(32*(SCALE)))
ag_font_large = pygame.font.Font(r'Rohan_The_Refs\fonts\angrybirds-regular.ttf', int(48*(SCALE)))
font_lotr_small= pygame.font.Font(r'Rohan_The_Refs\fonts\Aniron\Aniron.ttf', int(18*(SCALE)))
font_lotr_medium=pygame.font.Font(r'Rohan_The_Refs\fonts\Ringbearer.ttf',int(30*(SCALE)))
font_lotr_large=pygame.font.Font(r'Rohan_The_Refs\fonts\Aniron\Aniron.ttf',int(26*(SCALE)))

font_small,font_medium,font_large=ag_font_small,ag_font_medium,ag_font_large

# Images loading - Start
redright = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/red_right.png").convert_alpha(), c.BIRD_SIZE)  # 
chuckright = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/chuck_right.png").convert_alpha(), c.BIRD_SIZE)  # 
bluesright = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/blues_right.png").convert_alpha(), c.BIRD_SIZE)  # 
bombright = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/bomb_right.png").convert_alpha(), c.BIRD_SIZE)  # 

catapultright = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/background/catapult.png").convert_alpha(), c.CATSCALE)  # 

frodo = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/Frodo.png").convert_alpha(), c.BIRD_SIZE)  # 
aragorn = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/Aragorn.png").convert_alpha(), c.BIRD_SIZE)  # 
legolas = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/Legolas.png").convert_alpha(), c.BIRD_SIZE)  # 
gimli = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/Gimli.png").convert_alpha(), c.BIRD_SIZE)  # 

lotr_catapult= pygame.transform.scale(pygame.image.load("Rohan_The_Refs/background/lotr_catapult.png").convert_alpha(), c.LOTRCATSCALE)

ag_imgref = [redright, chuckright, bluesright, bombright]
imgref=ag_imgref
lotr_imgref=[frodo, aragorn, legolas, gimli]

ag_bg = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/background/background_one_proportional.jpg").convert() , c.SCREEN)# 
bgfine=ag_bg

lotr_bg_one=pygame.transform.scale(pygame.image.load("Rohan_The_Refs/background/lotr_helmsdeep.png").convert(), c.SCREEN)
lotr_bg_two=pygame.transform.scale(pygame.image.load("Rohan_The_Refs/background/lotr_minastirith.png").convert(), c.SCREEN)
lotr_bg_three=pygame.transform.scale(pygame.image.load("Rohan_The_Refs/background/lotr_mordor_flat.png").convert(), c.SCREEN)

theoden = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/Theoden.png").convert_alpha(), c.FIGSIZE)
gandalf = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/Gandalf.png").convert_alpha(), c.FIGSIZE)
aragorn_good = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/Aragorn.png").convert_alpha(), c.FIGSIZE)

saruman = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/Saruman.png").convert_alpha(), c.FIGSIZE)
witch_king = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/WitchKing.png").convert_alpha(), c.FIGSIZE)
sauron = pygame.transform.scale(pygame.image.load("Rohan_The_Refs/projectiles/Sauron.png").convert_alpha(), c.FIGSIZE)

lotr_good_figures = {
    "Theoden": theoden,
    "Gandalf": gandalf,
    "Aragorn": aragorn_good
}

lotr_evil_figures = {
    "Saruman": saruman,
    "Witch King": witch_king,
    "Sauron": sauron
}

# Images loading - End

class Game:
    def __init__(self):
        self.state=MENU
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.winner = None
        
        # Menu UI elements
        self.p1_input = InputBox(250*(SCALE), 200*(SCALE), 300*(SCALE), 40*(SCALE), "Player 1",font=font_small)
        self.p2_input = InputBox(250*(SCALE), 270*(SCALE), 300*(SCALE), 40*(SCALE), "Player 2",font=font_small)
        self.start_button = Button(300*(SCALE), 350*(SCALE), 200*(SCALE), 50*(SCALE), "Start Game",font=font_medium)
        self.settings_button = Button(300*(SCALE), 420*(SCALE), 200*(SCALE), 50*(SCALE), "Settings",font=font_medium)
        
        # Settings UI elements
        self.lotr_toggle = ToggleButton(420*(SCALE), 180*(SCALE), 200*(SCALE), 50*(SCALE), "LOTR Theme", initial=False, font=font_medium)
        self.air_slider = Slider(250*(SCALE), 320*(SCALE), 300*(SCALE), 40*(SCALE), min_value=0.5, max_value=2.0, initial=1.0, label="Wind Impact: ", font=font_medium)
        self.back_button = Button(300*(SCALE), 450*(SCALE), 200*(SCALE), 50*(SCALE), "Back to Menu",font=font_medium)
        
        # Game over UI elements
        self.play_again_button = Button(250*(SCALE), 300*(SCALE), 300*(SCALE), 50*(SCALE), "Play Again",font=font_medium)
        self.menu_button = Button(250*(SCALE), 370*(SCALE), 300*(SCALE), 50*(SCALE), "Main Menu",font=font_medium)
        
        # Theme and music settings
        self.lotr_theme = False
        self.lotr_music = r"Rohan_The_Refs\music\bgm_wav_lotr.wav"
        self.ag_music = r"Rohan_The_Refs\music\bgm_wav_ag.wav" 
        self.shake_timer = 0
        self.shake_duration = 0.4 # seconds
        self.shake_magnitude = 3  # pixels
        pygame.mixer.music.load(self.ag_music)
        pygame.mixer.music.play(-1)
        
        # Game variables
        self.scores=[0,0]
        self.turn_count1 = 0
        self.turn_count2 = 0
        self.MAX_TURNS = c.MAX_TURNS

        #  Timer variables
        self.turn_start_time = 0
        self.turn_time = 0
        self.timer_running = False
        self.turn_time_limit = c.TURNTIMER  # 30 seconds per turn

        self.lotr_toggle = ToggleButton(300*(SCALE), 200*(SCALE), 200*(SCALE), 50*(SCALE), "LOTR Mode", initial=False, font=font_medium)
        self.air_slider = Slider(250*(SCALE), 320*(SCALE), 300*(SCALE), 40*(SCALE), min_value=0, max_value=5.0, initial=3.0, label="Air Impact: ", font=font_small)
        self.back_button = Button(300*(SCALE), 450*(SCALE), 200*(SCALE), 50*(SCALE), "Back to Menu",font=font_medium)
        self.level_select_button = Button(300*(SCALE), 380*(SCALE), 200*(SCALE), 50*(SCALE), "Select Level",font=font_lotr_medium)
        # Create level selection buttons
        self.level_buttons = []
        for i in range(3):
            level_name = ["Helms Deep", "Minas Tirith", "Mordor"][i]
            self.level_buttons.append(Button(300*(SCALE), (200 + i*70)*(SCALE), 200*(SCALE), 50*(SCALE), level_name, font=font_lotr_medium))
 
        self.init_game()

        self.level_manager = LevelManager(self,(lotr_bg_one,lotr_bg_two,lotr_bg_three))

        self.level_oneliners = {
            0: pygame.mixer.Sound(r"Rohan_The_Refs\dialogue\theoden_the_horn_of_helm_hammerhand_audio.wav"),
            1: pygame.mixer.Sound(r"Rohan_The_Refs\dialogue\witchking_i_will_break_him_audio.wav"),
            2: pygame.mixer.Sound(r"Rohan_The_Refs\dialogue\frodo_i_will_take_the_ring_to_mordor_audio.wav")
        }

    def play_level_oneliner(self, level_index):
        if level_index in self.level_oneliners:
            self.level_oneliners[level_index].set_volume(1)
            self.level_oneliners[level_index].play()

    def rounded_surface(self,surface, radius):
        size = surface.get_size()
        mask = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, *size), border_radius=radius)
        rounded = pygame.Surface(size, pygame.SRCALPHA)
        rounded.blit(surface, (0, 0))
        rounded.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return rounded

    def reinitialize_ui_elements(self):
        #Updates fonts, colors, appearance, and theme-specific settings.
        self.init_game()
        if self.lotr_theme:
            btn_color = (139, 69, 19)  # brown
            btn_hover_color = (160, 82, 45)  # lighter brown
            active_color = (255, 215, 0)  # gold for active elements
            window_title = "Lord of the Rings: Fortress Battle"
            turn_limit = c.TURNTIMER
        else:
            # Angry Birds theme
            btn_color = (0, 200, 0)  # green
            btn_hover_color = (0, 150, 0)  # dark green
            active_color = (255, 0, 0)  # red for active elements
            window_title = "Angry Birds PvP"
            turn_limit = c.TURNTIMER  # Default turn time
        
        pygame.display.set_caption(window_title)
        
        self.turn_time_limit = turn_limit
        
        # Update all buttons
        buttons = [
            self.start_button,
            self.settings_button,
            self.play_again_button,
            self.menu_button,
            self.back_button
        ]
        
        for button in buttons:
            button.font = font_medium
            button.color = btn_color
            button.hover_color = btn_hover_color
        
        # Update toggle button text
        self.lotr_toggle.font = font_medium
        self.lotr_toggle.text = "Angry Birds" if self.lotr_theme else "LOTR"
        
        # Remember input box states
        p1_active = self.p1_input.active
        p2_active = self.p2_input.active
        p1_text = self.p1_input.text
        p2_text = self.p2_input.text
        
        # Update input boxes
        self.p1_input.font = font_small
        self.p2_input.font = font_small
        
        # Restore input box states
        self.p1_input.active = p1_active
        self.p2_input.active = p2_active
        self.p1_input.text = p1_text
        self.p2_input.text = p2_text
        self.p1_input.color = active_color if p1_active else (0, 0, 0)
        self.p2_input.color = active_color if p2_active else (0, 0, 0)
        
        # Update slider
        self.air_slider.font = font_small
        
        # Update background based on theme
        global bgfine
        if self.lotr_theme:
            # Select a LOTR background based on game state
            lotr_backgrounds = [lotr_bg_one, lotr_bg_two, lotr_bg_three]
            bgfine = lotr_backgrounds[self.level_manager.current_level]
        else:
            bgfine = ag_bg  # Original Angry Birds background

        if self.lotr_theme:
            current_level = self.level_manager.get_current_level()
            bgfine = current_level["background"]
        else:
            bgfine = ag_bg  # Original Angry Birds background


    def toggle_theme(self):
        self.lotr_theme = not self.lotr_theme

        if self.lotr_theme:
            self.level_manager.set_level(0,self)
        # Switch fonts based on theme
        global font_small, font_medium, font_large, imgref, lotr_imgref,ag_imgref
        
        if self.lotr_theme:
            font_small = font_lotr_small
            font_medium = font_lotr_medium
            font_large = font_lotr_large
            
            # Switch to LOTR music
            pygame.mixer.music.load(self.lotr_music)
            pygame.mixer.music.play(-1)
            
            # Change projectile images to LOTR characters
            imgref = lotr_imgref
        else:
            font_small = ag_font_small
            font_medium = ag_font_medium
            font_large = ag_font_large
            
            # Switch to Angry Birds music
            pygame.mixer.music.load(self.ag_music)
            pygame.mixer.music.play(-1)
            
            imgref = ag_imgref
        
        self.reinitialize_ui_elements()

    def trigger_shake(self):
        self.shake_timer = time.time() + self.shake_duration

    def is_shaking(self):
        return time.time() < self.shake_timer
    
    def transition_to_state(self, new_state):
        # Create fade effect
        fade_surface = pygame.Surface(c.SCREEN)
        fade_surface.fill((0, 0, 0))
        
        for alpha in range(0, 256, 8):
            fade_surface.set_alpha(alpha)
            
            # Draw current state
            if self.state == MENU:
                self.draw_menu()
            elif self.state == GAMEPLAY:
                self.draw_gameplay()
            elif self.state == GAME_OVER:
                self.draw_gameover()
            elif self.state == SETTINGS:
                self.draw_settings()
            
            # Draw fade
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)
        
        # Change state
        self.state = new_state
        
        # Fade in new state
        for alpha in range(255, -1, -8):
            fade_surface.set_alpha(alpha)
            
            if self.state == MENU:
                self.draw_menu()
            elif self.state == GAMEPLAY:
                self.draw_gameplay()
            elif self.state == GAME_OVER:
                self.draw_gameover()
            elif self.state == SETTINGS:
                self.draw_settings()
            
            # Draw fade
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)

    def init_game(self):
        # Initialize game variables  variables moved into class
        self.player = 1
        self.missile = None
        self.wind=np.random.randint(c.MIN_WIND, c.MAX_WIND+1)
        # Create balanced array for fortress blocks  logic moved into class
        self.map = self.balanced_array(shape=c.FORTSIZE)
        self.f1 = Fortress(50*(SCALE), 515*(SCALE)-((2*c.FORTSIZE[0]-1)*c.BLOCKSIZE[1]//2), self.map, 1, self.lotr_theme)
        self.f2 = Fortress(750*(SCALE)-(c.FORTSIZE[1]-1)*c.BLOCKSIZE[0], 515*(SCALE)-((2*c.FORTSIZE[0]-1)*c.BLOCKSIZE[1])//2, self.map, 2, self.lotr_theme)
        self.fortresses = [self.f1, self.f2]
        self.frndfort=self.f1
        self.oppofort=self.f2
        self.arsenal1 = []
        self.arsenal2 = []
        self.arsenals = (self.arsenal1, self.arsenal2)
        self.win = -1
        self.blockground=self.frndfort.blocks[4,0].y
        self.scores=[0,0]
        self.turn_count1 = 0
        self.turn_count2 = 0
        self.selected = False
        self.airborne = False
        self.dragging = False
        self.gravity_modifier = 1.0
        self.wind_modifier = 1.0
        self.gen_arsenal(0)
        self.gen_arsenal(1)
        
        #  Start the timer for the first player's turn
        self.start_turn_timer()

    #  function moved into class
    def balanced_array(self, shape):
        total = shape[0]*shape[1]
        done = False
        while not done:
            num_zeros = max(0, min(np.random.randint(total//3 - 1, total//3 + 2, shape[0]*shape[1])))
            num_ones = max(0, min(np.random.randint(total//3 - 1, total//3 + 2, shape[0]*shape[1])))
            num_twos = total - (num_zeros + num_ones)
            if num_twos > 0 and num_ones > 0 and num_zeros > 0 and num_zeros+num_ones+num_twos == shape[0]*shape[1] and max(num_zeros, num_ones, num_twos)-min(num_zeros, num_ones, num_twos) <= 2:
                done = True
                nums = [num_zeros, num_ones, num_twos]
                random.shuffle(nums)

        elements = [0]*num_zeros + [1]*num_ones + [2]*num_twos
        np.random.shuffle(elements)

        elements = np.array(elements).reshape(shape)
        return elements

    def gen_arsenal(self, num):
        self.arsenals[num].clear()
        for i in range(3):
            if num == 0:
                self.arsenals[num].append(Projectile((time.time()+i)%4, (200+20*i)*(SCALE), c.GRND))
            else:
                self.arsenals[num].append(Projectile((time.time()+i)%4, (800-(200+20*i))*(SCALE), c.GRND))

    def update_arsenal(self, num):
        for i in range(3):
            if num == 0:
                if self.arsenal1[i].picked:
                    self.arsenals[num][i] = (Projectile(time.time()%4, (200+20*i)*(SCALE), c.GRND))
            else:
                if self.arsenal2[i].picked:
                    self.arsenals[num][i] = (Projectile(time.time()%4, (800-(200+20*i))*(SCALE), c.GRND))

    def close(self, x, y, tol):
        return x-y <= abs(tol) and x-y >= -abs(tol)

    def draw_block(self, blk, buffer):
        # Get block position and size
        block_rect = pygame.Rect(
            blk.x - c.BLOCKSIZE[0] // 2,
            blk.y - c.BLOCKSIZE[1] // 2,
            c.BLOCKSIZE[0],
            c.BLOCKSIZE[1]
        )
        
        # Create a surface for this block
        block_surface = pygame.Surface((c.BLOCKSIZE[0], c.BLOCKSIZE[1]), pygame.SRCALPHA)
        block_surface.blit(blk.scaled_texture, (0, 0))
        
        if blk.scaled_crack:
                block_surface.blit(blk.scaled_crack, (0, 0))
        
        # create a mask for rounded corners
        mask = pygame.Surface((c.BLOCKSIZE[0], c.BLOCKSIZE[1]), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255), (0, 0, c.BLOCKSIZE[0], c.BLOCKSIZE[1]), border_radius=int(5*(SCALE)))
        
        # Apply the mask
        final_surface = pygame.Surface((c.BLOCKSIZE[0], c.BLOCKSIZE[1]), pygame.SRCALPHA)
        final_surface.blit(mask, (0, 0))
        final_surface.blit(block_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        # Draw the final block
        buffer.blit(final_surface, (blk.x - c.BLOCKSIZE[0] // 2, blk.y - c.BLOCKSIZE[1] // 2))
        
        # Draw outline
        pygame.draw.rect(buffer, blk.outline, block_rect, width=2*c.SCREEN_X//800, border_radius=((5*c.SCREEN_X)//800))

    def activate_explode_missile(self):
        for i in range(c.FORTSIZE[0]):
            for j in range(c.FORTSIZE[1]):
                blk=self.oppofort.blocks[i,j]
                if not blk.broken:
                    hurt_dist=c.BLOCKSIZE[0]+c.BLOCKSIZE[1]
                    bird_dist=dist(self.missile.pos,(blk.x,blk.y))
                    if bird_dist<hurt_dist*2:
                        dmg=self.missile.damage(blk.num)*(hurt_dist**2)//((hurt_dist**2+bird_dist**2)*1.5)
                        if self.lotr_theme:
                            dmg*=1.6
                        blk.hit(dmg)
                        self.scores[self.player-1]+=dmg
        self.missile.oop=True
        self.a_block_was_hit()
        self.trigger_shake()
      

    def split_blues(self):
        if not self.missile or self.missile.num != 2 or getattr(self.missile, 'split', False):
            return  # Only split blue birds, and only once

        # Calculate base velocity and position
        vx, vy = self.missile.vx, self.missile.vy
        x, y = self.missile.x, self.missile.y

        spread = 0.26  # ~15 degrees
        angles = [-spread, 0, spread]

        new_birds = []

        for angle in angles:
            # Rotate velocity vector by angle
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            new_vx = vx * cos_a - vy * sin_a
            new_vy = vx * sin_a + vy * cos_a

            # Create a new projectile (blue bird)
            bird = Projectile(2, x, y)
            bird.vx = new_vx
            bird.vy = new_vy
            bird.activated = 1  # Mark as already activated
            bird.split = True   # Prevent further splits
            new_birds.append(bird)

        self.missile = new_birds

    def closestBlock(self):
        mindist=c.SCREEN_X*10
        minblk=[-1,-1]
        for i in range(c.FORTSIZE[0]):
            for j in range(c.FORTSIZE[1]):
                nblk=self.fortresses[2-self.player].blocks[i,j]
                if dist((nblk.x,nblk.y),self.missile.pos)<mindist and not nblk.broken:
                    minblk=[i,j]
        return self.fortresses[2-self.player].blocks[minblk[0],minblk[1]]
    
    def resolve_overlap_only(self, bird, block_rect):
        dx = bird.x - block_rect.centerx
        dy = bird.y - block_rect.centery

        overlap_x = (block_rect.width // 2 + bird.radius) - abs(dx)
        overlap_y = (block_rect.height // 2 + bird.radius) - abs(dy)

        if overlap_x < overlap_y:
            # Push out horizontally
            if dx > 0:
                bird.x += overlap_x + c.COLBUF
            else:
                bird.x -= overlap_x + c.COLBUF
        else:
            # Push out vertically
            if dy > 0:
                bird.y += overlap_y + c.COLBUF
            else:
                bird.y -= overlap_y + c.COLBUF

    def resolve_collision(self, blk, bird):

        self.resolve_overlap_only(bird, blk.rect)
        dx = abs(bird.x - blk.x)
        dy = abs(bird.y - blk.y)
        fx = dx/((c.BLOCKSIZE[0]//2) + bird.radius)  # fraction of dx
        fy = dy/((c.BLOCKSIZE[1]//2) + bird.radius)  # of dy
        if self.close(fx, fy, 0.01):
            bird.cornerBounce()
        elif (fx) < (fy):
            bird.upBounce()
        elif fx > fy:
            bird.sideBounce()

    def circle_square_collision(self, cx, cy, radius, rect):
        # Find the closest point on the rect to the circle
        closest_x = max(rect.left, min(cx, rect.right))
        closest_y = max(rect.top, min(cy, rect.bottom))

        # Distance between circle center and closest point
        dx = cx - closest_x
        dy = cy - closest_y
        return (dx*dx + dy*dy) <= (radius * radius)

    def checkWin(self):
        frtrs = self.oppofort
        self.win = self.player-1
        for i in range(c.FORTSIZE[0]):
                for blk in frtrs.blocks[i]:
                    if not blk.broken:
                        self.win = -1
        if self.win == -1:
                return False
        else:
                #  Set winner name based on player number
                if self.win == 0:
                    self.winner = f"{self.player1_name} wins by Annihalation!"
                else:
                    self.winner = f"{self.player2_name} wins by Annihalation!"
                return True
        
    def a_block_was_hit(self):
        for fort in self.fortresses:
                for i in range(c.FORTSIZE[0]):
                    for j in range(c.FORTSIZE[1]):
                        blk = fort.blocks[i, j]
                        if blk.hp <= 0 and not blk.broken:
                            blk.broken = True
                            self.scores[self.player-1]+=c.BLOCKPOINT
        if self.checkWin():
                            self.missile.oop = True 
                            self.endTurn()           # This will transition to game over state

    def update_bird(self,proj):
            proj.rect = pygame.Rect(
            proj.x - c.BLOCKSIZE[0] // 2,
            proj.y - c.BLOCKSIZE[1] // 2,
            c.BLOCKSIZE[0],
            c.BLOCKSIZE[1]
            )

            for i in range(c.FORTSIZE[0]):
                for j in range(c.FORTSIZE[1]):
                    proj.rect = pygame.Rect(
                    proj.x - c.BLOCKSIZE[0] // 2,
                    proj.y - c.BLOCKSIZE[1] // 2,
                    c.BLOCKSIZE[0],
                    c.BLOCKSIZE[1]
                    )
                    if self.lotr_theme:
                            current_level = self.level_manager.get_current_level()
                            level_name = current_level["name"]

                            if level_name == "Helms Deep":
                                self.wind_modifier = 1.2  # Stronger wind at Helms Deep
                            elif level_name == "Minas Tirith":
                                pass  # Standard physics
                            elif level_name == "Mordor":
                                self.gravity_modifier = 1.3  # Stronger gravity in Mordor
                    nblk = self.fortresses[2-self.player].blocks[i, j]
                    if self.circle_square_collision(proj.x, proj.y, proj.radius, nblk.rect) and not nblk.broken:
                            nblk.hit(proj.damage(nblk.num))
                            self.scores[self.player-1]+=proj.damage(nblk.num)
                            self.resolve_collision(nblk, proj)

                if proj.y > c.GRND:
                    proj.y = c.GRND
                    proj.upBounce()

                if proj.x > 790*(SCALE) or proj.x < 10*(SCALE):
                    proj.oop = True
                if proj.y < 10*(SCALE) or proj.y > 590*(SCALE):
                    proj.oop = True
                if proj.collides >= 5:
                    proj.oop = True

            self.a_block_was_hit()

    def start_turn_timer(self):
        self.turn_start_time = pygame.time.get_ticks()
        self.timer_running = True

    def update_turn_timer(self):
        if self.timer_running:
            self.turn_time = (pygame.time.get_ticks() - self.turn_start_time) // 1000
            # Check if time limit is exceeded - implement auto-end turn
            if self.turn_time >= self.turn_time_limit:
                self.timer_running = False
                
                if self.selected and not self.airborne:
                    self.missile.oop = True  
                
                self.endTurn()
            return self.turn_time
        return 0
    
    def determine_turn_limit_winner(self):
        if self.scores[0] > self.scores[1]:
            self.winner = f"{self.player1_name} wins by Score!"
        elif self.scores[1] > self.scores[0]:
            self.winner = f"{self.player2_name} wins by Score!"
        else:
            self.winner = "Draw! No winner"

    def endTurn(self):
            # Update turn counts before checking limits
        if self.player == 1:
            self.turn_count1 += 1
        else:
            self.turn_count2 += 1

        if self.turn_count1 >= self.MAX_TURNS and self.turn_count2 >= self.MAX_TURNS:
                self.determine_turn_limit_winner()
                self.transition_to_state(GAME_OVER)
                return

        self.selected = False
        self.airborne = False
        if self.checkWin():
            self.transition_to_state(GAME_OVER)
            self.timer_running = False
        else:
            self.frndfort,self.oppofort=self.oppofort,self.frndfort
            self.player = 3 - self.player
            self.update_arsenal(2 - self.player)
            self.start_turn_timer()

    #  function moved into class
    def flipImage(self, img):
        return pygame.transform.flip(img, True, False)

    #  Main game loop function
    def run(self):
            clock = pygame.time.Clock()
            running = True
            
            while running:
                dt = clock.tick(240) / 1000  # fps limit as well as dt 
                
                # Handle events based on current state
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    if self.state == GAMEPLAY:
                        self.handle_gameplay_events(event)
                    elif self.state == MENU:
                        self.handle_menu_events(event)
                    elif self.state == GAME_OVER:
                        self.handle_gameover_events(event)
                    elif self.state == SETTINGS:
                        self.handle_settings_events(event)
                    elif self.state == LEVEL_SELECT:
                        self.handle_level_select_events(event)
    
                # Draw based on state

                # Update logic based on current state
                if self.state == GAMEPLAY:
                    #  Update timer
                    self.update_turn_timer()
                    self.update_gameplay(dt)
                
                # Draw everything
                screen.fill((255, 255, 255))
                
                if self.state == MENU:
                    self.draw_menu()
                elif self.state == GAMEPLAY:
                    self.draw_gameplay()
                elif self.state == GAME_OVER:
                    self.draw_gameover()
                elif self.state==SETTINGS:
                    self.draw_settings()
                elif self.state == LEVEL_SELECT:
                    self.draw_level_select()
                
                pygame.display.flip()  #  Refresh display
            
            pygame.quit() 

    def handle_menu_events(self, event):
        p1_name = self.p1_input.handle_event(event)
        if p1_name:
            self.player1_name = p1_name
            
        p2_name = self.p2_input.handle_event(event)
        if p2_name:
            self.player2_name = p2_name
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.is_clicked(event.pos):
                # Capture current input values regardless of Enter key
                self.player1_name = self.p1_input.text or "Player 1"
                self.player2_name = self.p2_input.text or "Player 2"
                self.transition_to_state(GAMEPLAY)
                self.start_turn_timer()
            elif self.settings_button.is_clicked(event.pos):
                # Transition to settings menu
                self.transition_to_state(SETTINGS)

    #  Handle gameplay events - Based on  event handling
    def handle_gameplay_events(self, event):
        #  Selection logic moved here
        if event.type == pygame.MOUSEBUTTONDOWN and not self.selected:
            for proj in self.arsenals[self.player-1]:
                if dist(event.pos, (proj.x, proj.y)) < c.TOUCH_TOL and self.player == 1 and not self.selected:
                    self.selected = True
                    self.missile = Projectile(proj.num, proj.x, proj.y)
                    proj.picked = True
                    self.missile.moveTo(c.CATAPULT_1[0], c.CATAPULT_1[1])
                    
                if dist(event.pos, (proj.x, proj.y)) < c.TOUCH_TOL and self.player == 2 and not self.selected:
                    self.selected = True
                    self.missile = Projectile(proj.num, proj.x, proj.y)
                    proj.picked = True
                    self.missile.moveTo(c.CATAPULT_2[0], c.CATAPULT_2[1])
                
        #  Dragging logic moved here
        elif event.type == pygame.MOUSEBUTTONDOWN and self.selected and not self.airborne:
            if dist(event.pos, self.missile.pos) < c.TOUCH_TOL*2:
                self.drag_start = event.pos
                self.dragging = True

        #  Launching logic moved here
        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
            self.dragging = False
            if dist(event.pos, self.drag_start) < 10*(SCALE):
                self.missile.moveTo(c.CATAPULT_1[0], c.CATAPULT_1[1])
            else:
                self.airborne = True
                self.missile.vx = c.SHOT_CONST * (c.CATAPULTS[self.player-1][0] - self.missile.x)
                self.missile.vy = c.SHOT_CONST * (c.CATAPULTS[self.player-1][1] - self.missile.y)

        elif event.type==pygame.MOUSEBUTTONDOWN and self.airborne and not isinstance(self.missile,list):
            self.missile.activate(self.lotr_theme)
            if self.missile.num==3 and self.missile.collides==0:
                self.activate_explode_missile()

            if self.missile.num==2 and self.missile.collides==0 and not self.lotr_theme:
                self.split_blues()
        
    
    def handle_settings_events(self, event):
        # Handle toggle for LOTR theme
        if self.lotr_toggle.handle_event(event):
                    self.toggle_theme()
        
        # Handle air impact slider
        self.air_slider.handle_event(event)
        
        # Back button to return to main menu
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_clicked(event.pos):
                self.transition_to_state(MENU)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.lotr_theme and self.level_select_button.is_clicked(event.pos):
                self.transition_to_state(LEVEL_SELECT)

        #  Dragging logic moved here
        elif event.type == pygame.MOUSEBUTTONDOWN and self.selected and not self.airborne:
            if dist(event.pos, self.missile.pos) < c.TOUCH_TOL*2:
                self.drag_start = event.pos
                self.dragging = True
                
        #  Launching logic moved here
        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
            self.dragging = False
            if dist(event.pos, self.drag_start) < 10*(SCALE):
                self.missile.moveTo(c.CATAPULT_1[0], c.CATAPULT_1[1])
            else:
                self.missile.vx = c.SHOT_CONST * (c.CATAPULTS[self.player-1][0] - self.missile.x)
                self.missile.vy = c.SHOT_CONST * (c.CATAPULTS[self.player-1][1] - self.missile.y)

    #  Handle game over events
    def handle_gameover_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_again_button.is_clicked(event.pos):
                self.player1_name,self.player2_name=self.player2_name,self.player1_name
                self.init_game()
                self.transition_to_state(GAMEPLAY)
            elif self.menu_button.is_clicked(event.pos):
                self.init_game()
                self.transition_to_state(MENU)
    def update_wind(self):
        if random.random() < 0.05:  # 10% chance of big gust
            change = random.uniform(-5 * c.DELTA, 5 * c.DELTA)
        else:
            change = random.uniform(-1.5 * c.DELTA, 1.5 * c.DELTA)

        self.wind += change
        self.wind = max(min(self.wind, c.MAX_WIND), -c.MAX_WIND)
    
    def handle_level_select_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check level button clicks
            for i, button in enumerate(self.level_buttons):
                if button.is_clicked(event.pos):
                    self.level_manager.set_level(i,self)
                    self.play_level_oneliner(i)
                    self.transition_to_state(GAMEPLAY)
                    return
            
            # Back button
            if self.back_button.is_clicked(event.pos):
                self.transition_to_state(SETTINGS)

    #  Update gameplay - Based on  main loop logic
    def update_gameplay(self, dt):
        #  Collision detection with blocks
        if self.airborne and not isinstance(self.missile,list):
            self.update_bird(self.missile)
            if self.missile.oop:
                self.endTurn()
        
        if self.airborne and isinstance(self.missile,list):
            for proj in self.missile:
                    self.update_bird(proj)
            count=0
            for proj in self.missile:
                if proj.oop:
                    count+=1
                if count==3:
                    self.endTurn()
        
        #  Dragging mechanics
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.drag_start[0]
            dy = mouse_y - self.drag_start[1]
            base_x, base_y = c.CATAPULTS[self.player - 1]
            d = dist((mouse_x, mouse_y), self.drag_start)

            if d < c.DRAGLMT:
                self.missile.moveTo(base_x + dx, base_y + dy)
            else:   
                scale = c.DRAGLMT / d
                self.missile.moveTo(int(base_x + dx * scale), int(base_y + dy * scale))
                
            self.a_block_was_hit()

        if self.airborne and not isinstance(self.missile,list):
            self.missile.x += self.missile.vx * dt
            self.missile.y += self.missile.vy * dt
            self.missile.pos = (self.missile.x, self.missile.y)
            self.missile.vy += c.G * dt * self.gravity_modifier
            self.missile.vx+=((self.wind/1.3)**c.windpower)*dt* self.wind_modifier
        elif self.airborne:
            for proj in self.missile:
                proj.x += proj.vx * dt
                proj.y += proj.vy * dt
                proj.pos = (proj.x, proj.y)
                proj.vy += c.G * dt
        
        self.update_wind()

        for x in range(2):
            # First pass: Mark blocks that have lost support and should fall
            for i in range(c.FORTSIZE[0]):
                for j in range(c.FORTSIZE[1]):
                    blk = self.fortresses[x].blocks[i][j]
                    
                    if blk.broken:
                        continue
                    
                    # Bottom row blocks are grounded if not broken
                    if i == 4:
                        blk.botrow = True
                        blk.grounded = True
                        blk.falling = False
                        blk.vy = 0
                        continue
                    else:
                        blk.botrow = False
                    
                    # Check if this block has support
                    has_support = False
                    block_below = None
                    
                    # Look for the first non-broken block below
                    for k in range(i+1, 5):
                        if not self.fortresses[x].blocks[k][j].broken:
                            block_below = self.fortresses[x].blocks[k][j]
                            has_support = True
                            break
                    
                    # Store reference to block below
                    blk.below = block_below
                    
                    # If no support or block below is falling, this block should fall
                    if not has_support:
                        blk.grounded = False
                        blk.falling = True
                    elif block_below.falling:
                        blk.grounded = False
                        blk.falling = True
                    else:
                        # Block below is stable - check if we're at the right position
                        landing_y = block_below.y - c.BLOCKSIZE[1]
                        if abs(blk.y - landing_y) > 2:  
                            blk.grounded = False
                            blk.falling = True
                        else:
                            # Snap to position
                            blk.y = landing_y
                            blk.grounded = True
                            blk.falling = False
                            blk.vy = 0
            
            # Second pass: Apply physics to falling blocks
            for i in range(c.FORTSIZE[0]):
                for j in range(c.FORTSIZE[1]):
                    blk = self.fortresses[x].blocks[i][j]
                    
                    if blk.broken:
                        continue
                        
                    if not blk.falling:
                        continue
                    
                    blk.vy += blk.g * dt
                    new_y = blk.y + blk.vy * dt
                    
                    # Update collision rect
                    blk.rect = pygame.Rect(
                        blk.x - c.BLOCKSIZE[0] // 2,
                        blk.y - c.BLOCKSIZE[1] // 2,
                        c.BLOCKSIZE[0],
                        c.BLOCKSIZE[1]
                    )
                    
                    if new_y >= self.blockground:
                        blk.y = self.blockground
                        blk.grounded = True
                        blk.falling = False
                        blk.vy = 0
                        continue
                    
                    # Check for collision with block below
                    if blk.below is not None:
                        landing_y = blk.below.y - c.BLOCKSIZE[1]
                        
                        if new_y >= landing_y:
                            if blk.below.grounded:
                                blk.y = landing_y
                                blk.grounded = True
                                blk.falling = False
                                blk.vy = 0
                            else:
                                blk.y = new_y
                        else:
                            blk.y = new_y
                    else:
                        blk.y = new_y
            
            # Fallback logic (just in case)
            any_falling = False
            for i in range(c.FORTSIZE[0]):
                for j in range(c.FORTSIZE[1]):
                    blk = self.fortresses[x].blocks[i][j]
                    if not blk.broken and blk.falling:
                        any_falling = True
                        break
            
            # If no blocks are falling but some should be (broken blocks below others)
            if not any_falling:
                for i in range(c.FORTSIZE[0]-1):  # Skip bottom row
                    for j in range(c.FORTSIZE[1]):
                        blk = self.fortresses[x].blocks[i][j]
                        below_blk = self.fortresses[x].blocks[i+1][j]
                        
                        if not blk.broken and below_blk.broken:
                            blk.falling = True
                            blk.grounded = False
                            blk.vy = 0  # Start with zero velocity
                            break

    def draw_menu(self):
        # Background
        screen.blit(bgfine, (0, 0))
        
        # Create semi-transparent overlay
        overlay = pygame.Surface(c.SCREEN, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Black with 150 alpha (semi-transparent)
        screen.blit(overlay, (0, 0))
        
        titletext="Angry Birds PvP" if not self.lotr_theme else "Fortresses of Middle Earth"
        title_text = (font_large if not self.lotr_theme else font_medium).render(titletext, True, (255, 255, 255))
        screen.blit(title_text, ((400*(SCALE) - title_text.get_width() // 2), 100*(SCALE)))
        
        instr_text = font_small.render("Enter player names and click Start", True, (255, 255, 255))
        screen.blit(instr_text, ((400*(SCALE) - instr_text.get_width() // 2), 160*(SCALE)))
        
        # Draw input labels
        p1_label = font_small.render("Player 1:", True, (255, 255, 255))
        screen.blit(p1_label, ((200*(SCALE)-p1_label.get_width()), 205*(SCALE)))
        
        p2_label = font_small.render("Player 2:", True, (255, 255, 255))
        screen.blit(p2_label, ((200*(SCALE)-p1_label.get_width()), 275*(SCALE)))
        
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.update(mouse_pos)
        self.settings_button.update(mouse_pos)

        # Draw input boxes and buttons
        self.p1_input.draw(screen)
        self.p2_input.draw(screen)
        self.start_button.draw(screen)
        self.settings_button.draw(screen)  # Add settings button


    def draw_wind_arrow(self, buffer):
        import math

        center_x = 400 * SCALE
        arrow_y = 140 * SCALE

        # Wind normalization
        max_wind = max(abs(c.MAX_WIND), 1e-5)  # avoid division by zero
        norm = min(abs(self.wind) / max_wind, 1.0)
        arrow_length = 80 * SCALE
        length = int(norm * arrow_length)

        # Color selection
        if self.wind < 0:
            color = (int(100 + 155 * norm), int(100 + 155 * (1 - norm)), 255)
        elif self.wind > 0:
            color = (255, int(100 + 155 * (1 - norm)), int(100 + 155 * norm))
        else:
            color = (150, 150, 150)

        # Arrow direction and positioning
        direction = -1 if self.wind < 0 else 1
        start = (center_x, arrow_y + 20 * SCALE)
        tip = (center_x + direction * length, arrow_y + 20 * SCALE)
        shaft_length = max(0, length - 16 * SCALE)
        end = (center_x + direction * shaft_length, arrow_y + 20 * SCALE)

        # Shaft with black outline
        pygame.draw.line(buffer, (0, 0, 0), start, end, int(7 * SCALE))
        if shaft_length > 0:
            pygame.draw.line(buffer, color, start, end, int(5 * SCALE))

        # Arrowhead
        if length > 0:
            head_length = 16 * SCALE
            head_angle = math.pi / 7

            def arrow_point(base, angle_offset, scale=1.0, shift=0):
                x = base[0] - scale * head_length * math.cos(angle_offset) * direction
                y = base[1] - scale * head_length * math.sin(angle_offset)
                return (x + shift * SCALE * direction, y)

            left = arrow_point(tip, -head_angle)
            right = arrow_point(tip, head_angle)
            outline_left = arrow_point(tip, -head_angle, scale=(1 + 5 / head_length), shift=2)
            outline_right = arrow_point(tip, head_angle, scale=(1 + 5 / head_length), shift=2)

            pygame.draw.polygon(buffer, (0, 0, 0), [tip, outline_left, outline_right])
            pygame.draw.polygon(buffer, color, [tip, left, right])

        font = font_small if self.lotr_theme else font_medium
        wind_str = f"Wind {int(self.wind)}"
        text_surface = font.render(wind_str, True, color)
        outline_surface = font.render(wind_str, True, (0, 0, 0))
        text_x = center_x - text_surface.get_width() // 2
        text_y = arrow_y - 28 * SCALE

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            buffer.blit(outline_surface, (text_x + dx, text_y + dy))
            buffer.blit(text_surface, (text_x, text_y))

    def draw_gameplay(self):
        #  Draw background and catapults
        buffer = pygame.Surface(c.SCREEN)
        buffer.blit(bgfine, (0, 0))

        current_level = None
        if self.lotr_theme:
            current_level = self.level_manager.get_current_level()
        if self.lotr_theme:
            cat=lotr_catapult
        else:
            cat=catapultright
        if not self.lotr_theme:
            buffer.blit(cat, (150*(SCALE), 445*(SCALE)))
            buffer.blit(self.flipImage(cat), ((650*(SCALE)-c.CATSCALE[0]), 445*(SCALE)))
        
        else:
            buffer.blit(cat, (142*(SCALE), c.GRND-70*(SCALE)))
            buffer.blit(self.flipImage(cat), ((800-142)*(SCALE)-c.LOTRCATSCALE[0], c.GRND-70*(SCALE)))

        if self.lotr_theme and current_level:
            # Draw good and evil figures
            good_img = lotr_good_figures[current_level["good_figure"]]
            evil_img = lotr_evil_figures[current_level["evil_figure"]]
            
            # Scale them up for display
            scaled_good = pygame.transform.scale(good_img, (60*(SCALE), 60*(SCALE)))
            scaled_evil = pygame.transform.scale(evil_img, (60*(SCALE), 60*(SCALE)))
            
            # Draw the characters on each side
            buffer.blit(scaled_good, (50*(SCALE), 150*(SCALE)))
            buffer.blit(self.flipImage(scaled_evil), (690*(SCALE), 150*(SCALE)))
            
        
        #  Draw player names and turn indicator
        p1_text = font_small.render(self.player1_name, True, (0, 0, 0))
        buffer.blit(p1_text, (50*(SCALE), 30*(SCALE)))
        
        p2_text = font_small.render(self.player2_name, True, (0, 0, 0))
        buffer.blit(p2_text, ((750*(SCALE) - p2_text.get_width()), 30*(SCALE)))
        
        turn_text = font_medium.render(f"Your turn {self.player1_name if self.player == 1 else self.player2_name}", True, (0, 0, 0))
        buffer.blit(turn_text, ((400*(SCALE) - turn_text.get_width() // 2), 20*(SCALE)))

        #  Draw fortress blocks
        for i in range(c.FORTSIZE[0]):       
            for j in range(c.FORTSIZE[1]):
                if not self.f1.blocks[i, j].broken:
                    self.draw_block(self.f1.blocks[i, j],buffer)
                if not self.f2.blocks[i, j].broken:
                    self.draw_block(self.f2.blocks[i, j],buffer)

        #  Draw arsenal projectiles
        for i in range(2):
            for proj in self.arsenals[i]:
                if not proj.picked:
                    if proj.vx > 0 or (proj.vx == 0 and i == 0):
                        buffer.blit(imgref[proj.num], (proj.x - c.BIRD_SIZE_X//2, proj.y - c.BIRD_SIZE_Y//2))
                    else:
                        buffer.blit(self.flipImage(imgref[proj.num]), (proj.x - c.BIRD_SIZE_X//2, proj.y - c.BIRD_SIZE_Y//2))
                        

        if not isinstance(self.missile,list):
            for i in range(2):
                if self.player == i + 1 and self.selected and self.missile and not self.missile.oop:

                    if self.missile.vx > 0 or (self.missile.vx == 0 and i == 0):
                            buffer.blit(imgref[self.missile.num], (self.missile.x - c.BIRD_SIZE_X//2, self.missile.y - c.BIRD_SIZE_Y//2))
                    else:
                            buffer.blit(self.flipImage(imgref[self.missile.num]), (self.missile.x - c.BIRD_SIZE_X//2, self.missile.y - c.BIRD_SIZE_Y//2))
        
        else:
            for proj in self.missile:
                    if not proj.oop:
                        if proj.vx > 0 or (proj.vx == 0 and i == 0):
                                buffer.blit(imgref[proj.num], (proj.x - c.BIRD_SIZE_X//2, proj.y - c.BIRD_SIZE_Y//2))
                        else:
                                buffer.blit(self.flipImage(imgref[proj.num]), (proj.x - c.BIRD_SIZE_X//2, proj.y - c.BIRD_SIZE_Y//2))

        remaining= max(0, self.turn_time_limit - self.turn_time)  
        time_color = (0, 0, 0)  

        if remaining < 5:
            time_color = (255, 0, 0)  

        timer_text = font_medium.render(f"{remaining} seconds remaining", True, time_color)
        buffer.blit(timer_text, (400*(SCALE) - timer_text.get_width() // 2, 60*(SCALE)))  

        self.draw_wind_arrow(buffer)

        score1_text = font_medium.render(f"{int(self.scores[0])}", True, (0, 0, 0))
        buffer.blit(score1_text, (50*(SCALE), 50*(SCALE)))
        score2_text = font_medium.render(f"{int(self.scores[1])}", True, (0, 0, 0))
        buffer.blit(score2_text, ((750*(SCALE) - score2_text.get_width()), 50*(SCALE)))

        turns_text_one = font_small.render(f"Turn {min(self.turn_count1+1,self.MAX_TURNS)} of {self.MAX_TURNS}",True, (0, 0, 0))
        turns_text_two = font_small.render(f"Turn {min(self.turn_count2+1,self.MAX_TURNS)} of {self.MAX_TURNS}",True, (0, 0, 0))

        buffer.blit(turns_text_one, (50*(SCALE), 100*(SCALE)))
        buffer.blit(turns_text_two, (750*(SCALE) -turns_text_two.get_width(),100*(SCALE)))

        # Determine offset if shaking
        if self.is_shaking():
            offset_x = random.randint(-self.shake_magnitude, self.shake_magnitude)
            offset_y = random.randint(-self.shake_magnitude, self.shake_magnitude)
        else:
            offset_x, offset_y = 0, 0

        screen.blit(buffer, (offset_x, offset_y))

    def draw_gameover(self):
        screen.blit(bgfine, (0, 0))
        
        overlay = pygame.Surface(c.SCREEN, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Draw winner announcement
        winner_text = font_large.render(f"{self.winner}", True, (255, 255, 255))
        screen.blit(winner_text, (400*(SCALE) - winner_text.get_width() // 2, 120*(SCALE)))
        
        # Display final scores
        score_text = font_medium.render(f"{self.player1_name} scored {int(self.scores[0])} vs {self.player2_name} scored {int(self.scores[1])}", True, (255, 255, 255))
        screen.blit(score_text, (400*(SCALE) - score_text.get_width() // 2, 200*(SCALE)))
        
        # Draw turns taken
        turns_text = font_small.render(f"Turns: {self.player1_name} ({self.turn_count1}) - {self.player2_name} ({self.turn_count2})", True, (255, 255, 255))
        screen.blit(turns_text, (400*(SCALE) - turns_text.get_width() // 2, 250*(SCALE)))
        
        self.play_again_button.draw(screen)
        self.menu_button.draw(screen)


    def draw_settings(self):
        screen.blit(bgfine, (0, 0))
        
        overlay = pygame.Surface(c.SCREEN, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        title_text = font_large.render("Game Settings", True, (255, 255, 255))
        screen.blit(title_text, (400*(SCALE) - title_text.get_width() // 2, 80*(SCALE)))
        
        mouse_pos=pygame.mouse.get_pos()
        self.level_select_button.update(mouse_pos)
        self.back_button.update(mouse_pos)
        self.lotr_toggle.draw(screen)
        
        if self.lotr_theme:
            self.level_select_button.draw(screen)
        self.air_slider.draw(screen)
        self.back_button.draw(screen)

    def draw_level_select(self):
        screen.blit(bgfine, (0, 0))
        
        overlay = pygame.Surface(c.SCREEN, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        title_text = font_large.render("Select LOTR Level", True, (255, 255, 255))
        screen.blit(title_text, (400*(SCALE) - title_text.get_width() // 2, 100*(SCALE)))
        
        for i, button in enumerate(self.level_buttons):
            button.update(pygame.mouse.get_pos())
            button.draw(screen)
            
            # Show level preview image (smaller version)
            level_img = [lotr_bg_one, lotr_bg_two, lotr_bg_three][i]
            preview = pygame.transform.scale(level_img, (100*(SCALE), 70*(SCALE)))
            preview = self.rounded_surface(preview,int(15*c.SCREEN_X//800))  # Adjust radius as needed
            screen.blit(preview, (520*(SCALE), (225-(70//2) + i*70)*(SCALE)))

        self.back_button.draw(screen)

