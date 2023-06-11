from config import *
from audio import *
import pygame, random
from math import *

from config import TILESIZE

class Spritesheet: #The spritesheet handler for the game
    def __init__(self, file) -> None:
        self.sheet = pygame.image.load(file).convert_alpha()
    
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet, (0,0), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite

class Background(pygame.sprite.Sprite):
    def __init__(self,game, x, y):
        self.game = game
        self._layer = 1
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = 0
        self.y = 0
        self.width = WIN_WIDTH
        self.height = WIN_HEIGHT
        self.image = self.game.background_spritesheet.get_sprite(x*self.width,y*self.width,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.color = [0,0,0]
        self.color_direction = [1,1,1]
        if self.game.area == 5 and self.game.level == 5:
            self.image = pygame.Surface((WIN_WIDTH,WIN_HEIGHT))
    
    def update(self):
        if self.game.area == 5 and self.game.level == 5:
            self.color_change()
            self.image.fill(tuple(self.color),self.image.get_rect())
            pygame.display.update()
    
    def color_change(self): #for the final boss, changes the colour spectrum randomly over a smooth direction 
        for x in range(3):
            self.color[x] += self.color_direction[x]
            if self.color[x] >= 255 or self.color[x] <= 0:
                self.color_direction[x] *= -1
                self.color_direction = [random.randint(-1,1),random.randint(-1,1),random.randint(-1,1)]
            if self.color[x] > 255:
                self.color[x] = 255
                self.color_direction = [random.randint(-1,1),random.randint(-1,1),random.randint(-1,1)]
            if self.color[x] < 0:
                self.color[x] = 0
                self.color_direction = [random.randint(-1,1),random.randint(-1,1),random.randint(-1,1)]

##########################################

class Profile(pygame.sprite.Sprite): #Profile Handler for Player
    def __init__(self, player):
        self.player = player
        self._layer = 7
        self.groups = self.player.game.profile
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = 9 * TILESIZE
        self.y = 12 * TILESIZE
        self.max_health_bar = Image(self.player.game, self.x, self.y, self.player.game.profile_spritesheet.get_sprite(336,0,336,192),5) #gets the max health from the profile UI spritesheet
        self.health_bar = Image(self.player.game, self.x, self.y, self.player.game.profile_spritesheet.get_sprite(336*4,192,336,192), 5) #gets the current health from the profile UI spritesheet
        self.max_mana_bar = Image(self.player.game,self.x,self.y,self.player.game.profile_spritesheet.get_sprite(336*4,192*2,336,192)) #gets the max mana from the profile UI spritesheet
        self.mana_bar = Image(self.player.game,self.x,self.y,self.player.game.profile_spritesheet.get_sprite(336*3,192*3,336,192), 5) #gets the max mana from the profile UI spritesheet
        self.max_experience_bar = Image(self.player.game,self.x,self.y,self.player.game.profile_spritesheet.get_sprite(336*2,192*4,336,192))
        self.experience_bar = Image(self.player.game,self.x,self.y,self.player.game.profile_spritesheet.get_sprite(336*5,192*5,336,192))
        self.image = self.player.game.profile_spritesheet.get_sprite(336*self.player.power*3,192*6,56*6,32*6)
        self.rect = self.image.get_rect() #gets the correct player to display in the profile UI
        self.rect.x = self.x 
        self.rect.y = self.y 
        self.original_health_bar = self.health_bar.image
        
        self.health_alert_animation = 0 #value for calculating timing for the alert flashing
        self.health_alert_playing = False


    def update(self): #updates all the parts of the profile
        self.max_health_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.max_health / 2 - 2),0,336,192) #updates the max health based on the max health
        self.health_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.health),192,336,192)
        self.max_mana_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.max_mana - 3),192*2,336,192)
        self.mana_bar.image = self.player.game.profile_spritesheet.get_sprite(336*floor(self.player.mana),192*3,336,192)
        self.max_experience_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.max_experience / 2 - 4),192*4,336,192)
        self.experience_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.experience),192*5,336,192)
        self.original_health_bar = self.health_bar.image
        if pygame.time.get_ticks() - self.player.last_hit < self.player.hit_cooldown - 100: #checking whether the player was hit or not recently
            self.image = self.player.game.profile_spritesheet.get_sprite(336*self.player.power*3 + 336,192*6,56*6,32*6)
            self.image.set_alpha(100)
            self.health_alert_animation = 0
            
            self.flashing_health(True)
        elif float(self.player.health / self.player.max_health) <= 0.25:
            self.image = self.player.game.profile_spritesheet.get_sprite((336*self.player.power*3) + (336*2),192*6,56*6,32*6)
            self.flashing_health(False)
        else:
            self.image = self.player.game.profile_spritesheet.get_sprite(336*self.player.power*3,192*6,56*6,32*6)
            self.health_bar.image = self.original_health_bar
            self.health_alert_animation = 0
        
        if self.health_alert_animation > 0 and not self.health_alert_playing:
            SFX.low_hp_alert.set_volume(0.8)
            SFX.low_hp_alert.play()
            SFX.low_hp_alert.fadeout(2000)
            self.health_alert_playing = True
        elif self.health_alert_animation == 0:
            SFX.low_hp_alert.stop()
            self.health_alert_playing = False
    
    def flashing_health(self,once):
        if once: #plays the flash once when hit once
            self.original_health_bar = self.health_bar.image
            self.hit_image = self.health_bar.image.copy()
            var = pygame.PixelArray(self.hit_image)
            var.replace(pygame.Color(141,216,148), pygame.Color(255,0,0))
            var.replace(pygame.Color(69,147,165),pygame.Color(255,25,25))
            del var
            self.health_bar.image = self.hit_image
        else: #plays the alert sound and repeatedly flashes on low health
            self.health_alert_animation += 0.025
            if floor(self.health_alert_animation) >= 1:
                self.original_health_bar = self.health_bar.image
                self.hit_image = self.health_bar.image.copy()
                var = pygame.PixelArray(self.hit_image)
                var.replace(pygame.Color(141,216,148), pygame.Color(255,0,0))
                var.replace(pygame.Color(69,147,165),pygame.Color(255,25,25))
                del var
                self.health_bar.image = self.hit_image
                if self.health_alert_animation >= 2:
                    self.health_alert_animation = 0.025
            else:
                self.health_bar.image = self.original_health_bar

class Image(pygame.sprite.Sprite): #Images without any functions or movement (just for display and updated framing, mainly UI)
    def __init__(self,game, x, y, image,layer = 4):
        self.game = game
        self._layer = layer
        self.groups = self.game.profile #sets to the profile sprite group, which is on a higher layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Player(pygame.sprite.Sprite): #The Player
    def __init__(self, game, x, y, power = 0):
        self.game = game
        self.power = power

        self.profile = Profile(self)
        
        self.level = 1
        self.max_health = 4
        self.health = self.max_health
        
        self.max_mana = 3
        self.mana = self.max_mana

        self.experience = 0
        self.max_experience = self.level * 2 + 6

        self._layer = PLAYER_LAYER #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.character_spritesheet.get_sprite(1,1,self.width,self.height)
        self.weapon = self.game.weapon_spritesheet.get_sprite(self.power*48,0,self.width,self.height)
        self.x_change = 0 #x_vel
        self.y_change = 0 #y_vel
        
        self.facing = "down"
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.weapon_angle = 90
        self.weapon_copy = Image(self.game,self.x+30,self.y,pygame.transform.rotate(self.weapon,self.weapon_angle),PLAYER_LAYER+1)

        self.dash_cooldown = 500

        self.basic_cooldowns = [500,600,700] #cooldowns for basic attacks
        self.basic_cooldown = self.basic_cooldowns[self.power]
        self.basic_combo = 0

        self.special_cooldown = 500
        self.last_dashed = 0
        self.last_basic = 0
        self.special_basic = False
        
        self.dashing = 1
        self.guarding = False
        if self.power == 0:
            self.guarding_cooldown = 300
        else:
            self.guarding_cooldown = 500
        self.last_guarded = 0
        self.last_special = 0

        self.hit_cooldown = 1200
        self.last_hit = 0
        self.times_hit = 0
        for i in range(self.game.level - 1):
            self.level_up()
        for i in range(self.game.area - 1):
            self.level_up()
        self.stat_tree = {
            0:["HP"], #Lionheart Stat Tree (For pygame project part 2!)
            1:[{"learn_skill":0}], #Odyssey Stat Tree (For pygame project part 2!)
            2:[]  #Acuity Stat Tree (For pygame project part 2!)
        }

    def update(self):
        self.animate()
        self.movement()
        self.collide()
        self.x_change = 0
        self.y_change = 0
        self.level_clear_check()
        self.exp_check()
    
    def exp_check(self):
        if self.experience > self.max_experience: #checks if the experience exceeds the experience required to next level
            self.level_up()

    def level_up(self):
        SFX.level_up.play()
        self.experience -= self.max_experience
        self.hit_cooldown -= 100
        self.basic_cooldowns[self.power] -= 10
        if self.experience < 0:
            self.experience = 0
        self.level += 1
        self.max_experience = self.level * 2 + 6
        self.max_health += 2
        self.health += 2
        if self.level % 3 == 0:
            self.max_mana += 1
            self.mana += 1
    
    def level_clear_check(self): #checks if the level has been cleared and that the player is on the top of the level
        if self.y <= 0 and self.game.level_cleared:
            self.rect.y = WIN_HEIGHT - 32
            self.y = self.rect.y
            self.game.next_level()

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change = (PLAYER_SPEED) if self.y_change == 0 else (cos(radians(45)) * PLAYER_SPEED)
        if keys[pygame.K_d]:
            self.x_change = (PLAYER_SPEED) if self.y_change == 0 else (cos(radians(45)) * PLAYER_SPEED)
        
        if keys[pygame.K_w]:
            self.y_change -= (PLAYER_SPEED) if self.x_change == 0 else (cos(radians(45)) * PLAYER_SPEED)
        if keys[pygame.K_s]:
            self.y_change += (PLAYER_SPEED) if self.x_change == 0 else (cos(radians(45)) * PLAYER_SPEED)
        
        self.x_change = 0

        if keys[pygame.K_a]:
            self.x_change -= (PLAYER_SPEED) if self.y_change == 0 else (cos(radians(45)) * PLAYER_SPEED)
        if keys[pygame.K_d]:
            self.x_change += (PLAYER_SPEED) if self.y_change == 0 else (cos(radians(45)) * PLAYER_SPEED)

        self.x_change *= self.dashing
        self.y_change *= self.dashing
        if pygame.time.get_ticks() - self.last_dashed > self.dash_cooldown / 1.5:
            self.dashing = 1
        if keys[pygame.K_SPACE] and not self.guarding:
            self.dash()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] and not self.dashing:
            if pygame.time.get_ticks() - self.last_guarded > self.guarding_cooldown:
                self.guard()
            else:
                self.guarding = False
        if self.x_change == 0:
            if self.y_change > 0:
                self.facing = "down"
            elif self.y_change < 0:
                self.facing = "up"
        elif self.y_change == 0:
            if self.x_change < 0:
                self.facing = "left"
            elif self.x_change >0:
                self.facing = "right"
        else:
            if self.y_change > 0:
                if self.x_change < 0:
                    self.facing = "down_left"
                elif self.x_change > 0:
                    self.facing = "down_right"
            else:
                if self.x_change < 0:
                    self.facing = "up_left"
                elif self.x_change > 0:
                    self.facing = "up_right"
        
        if self.guarding:
            self.x_change = 0
            self.y_change = 0
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x = self.rect.x
        self.y = self.rect.y

    def collide(self):
        if self.y > (WIN_HEIGHT - TILESIZE):
            self.rect.y = (WIN_HEIGHT - TILESIZE)
        elif self.y < 0:
            self.rect.y = 0
        if self.x > (WIN_WIDTH - TILESIZE):
            self.rect.x = (WIN_WIDTH-TILESIZE)
        elif self.x < 1:
            self.rect.x = 0 
        
        hits = pygame.sprite.spritecollide(self,self.game.enemies, False)
        if hits:
            if pygame.time.get_ticks() - self.last_hit > self.hit_cooldown and pygame.time.get_ticks() - self.last_dashed > self.dash_cooldown + 400 and pygame.time.get_ticks() - self.last_guarded > self.guarding_cooldown + 300:
                try:
                    if hits[0].can_hurt:
                        if not self.guarding:
                            self.last_hit = pygame.time.get_ticks()
                            SFX.player_hurt.play()
                            self.health -= 1
                            self.times_hit += 1
                except:
                    if not self.guarding:
                        self.last_hit = pygame.time.get_ticks()
                        SFX.player_hurt.play()
                        self.health -= 1
                        self.times_hit += 1
                        
        #Checks if the player dashed, or got hit (to become transparent to show i-frames)
        if pygame.time.get_ticks() - self.last_hit <= self.hit_cooldown or pygame.time.get_ticks() - self.last_dashed < self.dash_cooldown + 400 and pygame.time.get_ticks() - self.last_guarded > self.guarding_cooldown + 300:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)
    def handle_weapon(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.weapon_angle = (180 / pi) * -atan2(mouse_y-self.y, mouse_x-self.x)
        self.weapon_copy.image = pygame.transform.rotate(self.weapon,self.weapon_angle)
        self.weapon_copy.x = self.x + 32
        self.weapon_copy.y = self.y
        self.weapon_copy.rect.x = self.x + 32
        self.weapon_copy.rect.y = self.y
    
    def animate(self):
        self.handle_weapon()
        down = self.game.character_spritesheet.get_sprite(0,self.power*48, self.width, self.height)
        right = self.game.character_spritesheet.get_sprite(48,(self.power)*48, self.width, self.height)
        left = pygame.transform.flip(right, True, False)
        
        up = self.game.character_spritesheet.get_sprite(48*3,self.power*48, self.width, self.height)
        
        down_right = self.game.character_spritesheet.get_sprite(48*2,(self.power)*48, self.width, self.height)
        down_left = pygame.transform.flip(down_right, True, False)
        
        up_right = self.game.character_spritesheet.get_sprite(48*4,self.power*48, self.width, self.height)
        up_left = pygame.transform.flip(up_right, True, False)
        
        self.image = locals()[self.facing]
    
    def dash(self):
        if (pygame.time.get_ticks() - self.last_dashed > self.dash_cooldown or self.last_dashed == 0) and self.mana >= 1 and (self.x_change != 0 or self.y_change != 0):
            self.dashing = 4
            self.mana -= 1
            SFX.dash.play()
            self.last_dashed = pygame.time.get_ticks()
    
    def guard(self):
        if self.guarding == False:
            if self.power == 0 or self.mana - 1 >= 0:
                SFX.shield.play()
                if self.power != 0:
                    self.mana -= 1
                PlayerGuard(self.game,self.x,self.y)
                self.guarding = True
        
        
    def basic_attack(self):
        if (pygame.time.get_ticks() - self.last_basic > self.basic_cooldown or self.last_basic == 0):
            self.last_basic = pygame.time.get_ticks()
            if int(self.mana + 0.1) < self.max_mana:
                self.mana += 0.1
            else:
                self.mana = self.max_mana
            if self.basic_combo == 3:
                self.special_basic = True
                self.basic_combo = 0
            else:
                self.basic_combo += 1
            if self.special_basic:
                [lambda: SFX.throw_circle.play(),lambda: SFX.throw_circle.play(),lambda: SFX.orb_throw.play()][self.game.player.power]()
                self.basic = BasicAttack(self.game, self.x+16,self.y-16, (self.game.mouse_pos[0]-96,self.game.mouse_pos[1]-96),True)
                self.basic = BasicAttack(self.game, self.x+32,self.y, (self.game.mouse_pos[0],self.game.mouse_pos[1]))
                self.basic = BasicAttack(self.game, self.x+48,self.y+16, (self.game.mouse_pos[0]+96,self.game.mouse_pos[1]+96))
            else:
                [lambda: SFX.throw_one.play(),lambda: SFX.throw_one.play(),lambda: SFX.orb_throw.play()][self.game.player.power]()
                self.basic = BasicAttack(self.game, self.x+32,self.y, (self.game.mouse_pos[0],self.game.mouse_pos[1]),True)
            self.basic_cooldown = self.basic_cooldowns[self.power] + random.randint(-50,50)
            self.special_basic = False
    def special_attack(self):
        if (pygame.time.get_ticks() - self.last_special > self.special_cooldown or self.last_special == 0) and self.mana >= 1:
            self.last_special = pygame.time.get_ticks()
            self.mana -= 1
            if self.power == 0:
                #SFX.throw_one.play()
                self.special = SpecialAttack(self.game, self.x+32,self.y-8, (self.game.mouse_pos[0]+10,self.game.mouse_pos[1]+10))
                #self.special = SpecialAttack(self.game, self.x+16,self.y+8, (self.game.mouse_pos[0]-10,self.game.mouse_pos[1]-10))
            elif self.power == 1:
                #self.special = SpecialAttack(self.game, self.x+32,self.y, (self.game.mouse_pos[0],self.game.mouse_pos[1]))
                SFX.throw_two.play()
                self.special = SpecialAttack(self.game, self.x+16,self.y, (self.game.mouse_pos[0]+45,self.game.mouse_pos[1]+50))
                self.special = SpecialAttack(self.game, self.x,self.y, (self.game.mouse_pos[0],self.game.mouse_pos[1]))
                self.special = SpecialAttack(self.game, self.x+48,self.y, (self.game.mouse_pos[0]-45,self.game.mouse_pos[1]-50))
            elif self.power == 2:
                #self.special = SpecialAttack(self.game, self.x+32,self.y, (self.game.mouse_pos[0],self.game.mouse_pos[1]))
                SFX.orb_special.play()
                self.special = SpecialAttack(self.game, self.x+32,self.y, (self.game.mouse_pos[0],self.game.mouse_pos[1]))
                #self.special = SpecialAttack(self.game, self.x+48,self.y, (self.game.mouse_pos[0]-48,self.game.mouse_pos[1]-50))
### GUARD

class PlayerGuard(pygame.sprite.Sprite):
    def __init__(self,game,x,y) -> None:
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.game = game
        self.is_shield = True
        self._layer = PLAYER_LAYER+2#Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.character_spritesheet.get_sprite(240,48,96,96) #shield image
        self.image = pygame.transform.scale(self.image,(120,120))
        self.spawn_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.image.set_alpha(0)
        self.alpha = 200
    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > 500:
            self.alpha -= 10
        if self.alpha < 10:
            self.game.player.guarding = False    
        if not self.game.player.guarding:
            self.game.player.last_guarded = pygame.time.get_ticks()
            self.kill()
        self.rect.x = self.game.player.x - 36
        self.rect.y = self.game.player.y - 36
        self.x = self.rect.x 
        self.y = self.rect.y 
        if self.game.player.mana < self.game.player.max_mana-0.005:
            self.game.player.mana += 0.005
        self.image.set_alpha(self.alpha)

############################# PLAYER ATTACKS
class BasicAttack(pygame.sprite.Sprite):
    def __init__(self,game,x,y,mouse_pos,makes_sound = False) -> None:
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.game = game
        
        self._layer = PLAYER_LAYER #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.attacks

        pygame.sprite.Sprite.__init__(self, self.groups)
        self.mouse_x, self.mouse_y = mouse_pos
        self.speed = 7
        self.angle = atan2(y-self.mouse_y,x-self.mouse_x)
        self.x_vel = cos(self.angle) * self.speed
        self.y_vel = sin(self.angle) * self.speed
        
        self.image = self.game.attack_spritesheet.get_sprite(48*self.game.player.power,0,self.width,self.height)
        
        if self.game.player.power == 0:
            self.image = self.game.attack_spritesheet.get_sprite(0,96*9,self.width*2,self.height)
        elif self.game.player.power == 1:
            self.image = self.game.attack_spritesheet.get_sprite(0,0,18,48)
            self.speed = 9
        elif self.game.player.power == 2:
            self.image = self.game.attack_spritesheet.get_sprite(48,0,24,24)
            self.speed = 6
        self.hit_sfx = [SFX.sword_hit,SFX.arrow_hit,SFX.orb_hit][self.game.player.power]
        self.two_hit_sfx = [SFX.sword_hit2,SFX.arrow_hit,SFX.orb_hit][self.game.player.power]
        self.three_hit_sfx = [SFX.sword_hit3,SFX.sword_hit3,SFX.orb_throw][self.game.player.power]

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        
        self.current_level = self.game.level
        self.angle = (180 / pi) * -atan2(self.mouse_y-self.y, self.mouse_x-self.x)-90
        self.arrow_copy = pygame.transform.rotate(self.image,self.angle)
        self.image = self.arrow_copy
        
        self.alpha = 255
        self.makes_sound = makes_sound #since there are several instances, there must only be one sound playing at once (to not make it sound really loud)

        self.animation_frame = 0
        self.has_collided = False
        self.sound_played = False
        self.is_special = self.game.player.special_basic #if the basic attack is special
    
    def update(self):
        self.collide()
        if self.game.player.power == 0:
            if not self.animation_frame > 2:
                self.x = self.game.player.x - (self.x_vel * self.speed*2)
                self.y = self.game.player.y - (self.y_vel * self.speed*2)
            self.image = self.game.attack_spritesheet.get_sprite(0,96+(48*floor(self.animation_frame))+24,self.width*2,24)
            self.attack_copy = pygame.transform.rotate(self.image,self.angle)
            self.image = self.attack_copy
            self.image.set_alpha(int(self.alpha))
            self.alpha -= 4
            if self.animation_frame < 5:
                self.animation_frame += 0.1
            else:
                self.kill()
        else:   
            self.x -= self.x_vel
            self.y -= self.y_vel
        self.rect.x = self.x
        self.rect.y = self.y
        if self.x > WIN_WIDTH or self.x < -TILESIZE:
            self.kill()
        if self.y > WIN_HEIGHT or self.y < -TILESIZE:
            self.kill()
        if self.game.level != self.current_level:
            self.kill()
        
        if self.has_collided and self.game.player.power != 0:
            self.image.set_alpha(self.alpha)
            self.alpha -= 20
            if self.alpha < 20:
                self.kill()
        pygame.time.delay(0)
    def collide(self):
        hits = pygame.sprite.spritecollide(self,self.game.enemies, False)
        if hits:
            try:
                for hit in hits:
                    if not self.has_collided:
                            try:
                                if hit.can_hit:
                                    if self.game.player.power == 0:
                                        hit.health -= random.randint(1,2)
                                    else:
                                        hit.health -= 1
                                    if self.sound_played == False and self.makes_sound:
                                            self.hit_sfx.play()
                                            self.sound_played = True
                                self.has_collided = True
                            except:
                                pass
            except: 
                pass

class SpecialAttack(pygame.sprite.Sprite):
    def __init__(self,game,x,y,mouse_pos) -> None:
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.game = game
        self._layer = PLAYER_LAYER #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        mouse_x, mouse_y = mouse_pos
        self.speed = 8
        self.angle = atan2(y-mouse_y,x-mouse_x)
        self.x_vel = cos(self.angle) * self.speed
        self.y_vel = sin(self.angle) * self.speed
        
        self.image = [self.game.attack_spritesheet.get_sprite(self.width*2,96+24,self.width*2,24), self.game.attack_spritesheet.get_sprite(0,48,18,48), self.game.attack_spritesheet.get_sprite(48,48,36,36)][self.game.player.power]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        angle = (180 / pi) * -atan2(mouse_y-self.y, mouse_x-self.x)-90
        self.arrow_copy = pygame.transform.rotate(self.image,angle)
        self.image = self.arrow_copy
        self.alpha = 255

        self.has_collided = False
        self.game.player.basic_cooldown = 800
    def update(self):
        self.collide()
        self.x -= self.x_vel
        self.y -= self.y_vel
        self.rect.x = self.x
        self.rect.y = self.y
        if self.x > WIN_WIDTH:
            self.kill()
        if self.y > WIN_HEIGHT:
            self.kill()
        if self.game.player.power == 0:
            self.x_vel *= 0.98
            self.y_vel *= 0.98
            self.alpha -= 3
            self.image.set_alpha(self.alpha)
            if self.alpha < 1:
                self.kill()
        pygame.time.delay(0)
    def collide(self):
        hits = pygame.sprite.spritecollide(self,self.game.enemies, False)
        if hits:
            for hit in hits:
                if not self.has_collided:
                    try:
                        if hit.can_hit:
                            hit.health -= 3 - self.game.player.power
                            if self.game.player.power == 0:
                                SFX.sword_special_hit.play()
                            else:
                                SFX.orb_hit.play()
                    except: pass
            self.has_collided = True
class Spell(pygame.sprite.Sprite):
    pass

################################################

class HealthOrb(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game

        self._layer = PLAYER_LAYER #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.drops
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.drops_spritesheet.get_sprite(60,12,24,24)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        target_x, target_y = random.randint(-WIN_WIDTH,WIN_WIDTH), random.randint(-WIN_HEIGHT,WIN_HEIGHT) #gets any position
        self.speed = 2
        self.angle = atan2(y-target_y,x-target_x)
        self.x_vel = cos(self.angle) * self.speed
        self.y_vel = sin(self.angle) * self.speed

        self.has_collided = False
        self.alpha = 255
        self.on_level = self.game.level #storing information of what level the sprite is on so it can be deleted if ignored
    def update(self):
        self.collide()
        self.movement()
        self.x -= self.x_vel
        self.y -= self.y_vel
        self.rect.x = self.x
        self.rect.y =self.y
        self.x_vel *= 0.97
        self.y_vel *= 0.97
        if self.has_collided:
            self.image.set_alpha(self.alpha)
            self.alpha -= 25
            if self.alpha < 1:
                SFX.health_orb.play()
                self.kill()
        if self.on_level != self.game.level:
            self.kill()  
    def movement(self):
        pass
    def collide(self):
        if self.y > (WIN_HEIGHT - TILESIZE):
            self.rect.y = (WIN_HEIGHT - TILESIZE)
        elif self.y < 0:
            self.rect.y = 0
        if self.x > (WIN_WIDTH - TILESIZE):
            self.rect.x = (WIN_WIDTH-TILESIZE)
        elif self.x < 1:
            self.rect.x = 0 
        hits = pygame.sprite.spritecollide(self,self.game.players, False)
        if hits:
            for hit in hits:
                try:
                    if hit.health < hit.max_health and not self.has_collided:
                        hit.health += 1
                        self.has_collided = True
                except: pass

class ManaOrb(pygame.sprite.Sprite): #Mana Orbs that drop when killing an enemy
    def __init__(self, game, x, y):
        self.game = game

        self._layer = PLAYER_LAYER #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.drops
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.drops_spritesheet.get_sprite(6,6,36,36)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        target_x, target_y = random.randint(-WIN_WIDTH,WIN_WIDTH), random.randint(-WIN_HEIGHT,WIN_HEIGHT) #gets any position
        self.speed = 2
        self.angle = atan2(y-target_y,x-target_x)
        self.x_vel = cos(self.angle) * self.speed
        self.y_vel = sin(self.angle) * self.speed
        self.on_level = self.game.level
        self.has_collided = False
        self.alpha = 255
    def update(self):
        self.collide()
        self.movement()
        self.x -= self.x_vel
        self.y -= self.y_vel
        self.rect.x = self.x
        self.rect.y =self.y
        self.x_vel *= 0.97
        self.y_vel *= 0.97
        if self.has_collided == True:
            self.image.set_alpha(self.alpha)
            self.alpha -= 25
            if self.alpha < 10:
                SFX.mana_orb.play()
                self.kill()
        if self.on_level != self.game.level:
            self.kill()
    def movement(self):
        pass
    def collide(self):
        if self.y > (WIN_HEIGHT - TILESIZE):
            self.rect.y = (WIN_HEIGHT - TILESIZE)
        elif self.y < 0:
            self.rect.y = 0
        if self.x > (WIN_WIDTH - TILESIZE):
            self.rect.x = (WIN_WIDTH-TILESIZE)
        elif self.x < 1:
            self.rect.x = 0 
        hits = pygame.sprite.spritecollide(self,self.game.players, False)
        if hits:
            for hit in hits:
                try:
                    if hit.mana < hit.max_mana and not self.has_collided:
                        hit.mana = floor(hit.mana)
                        hit.mana += 1
                        self.has_collided = True
                except: pass
                

############### Enemy Stuffs

class Projectile(pygame.sprite.Sprite): #Simple projectiles for enemies! You can change the image and also the target position!! Easy :)
    def __init__(self,game,x,y,target_pos,image,speed=4,rotate=True) -> None:
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.game = game
        self._layer = PLAYER_LAYER+1 #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.target_x, self.target_y = target_pos
        self.speed = speed
        self.angle = atan2(y-self.target_y,x-self.target_x)
        self.x_vel = cos(self.angle)
        self.y_vel = sin(self.angle) 
        
        self.image = image
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.current_level = self.game.level
        if rotate:
            self.angle = (180 / pi) * -atan2(self.target_y-self.y, self.target_x-self.x)-90
            self.arrow_copy = pygame.transform.rotate(self.image,self.angle)
            self.image = self.arrow_copy
        self.animation_frame = 0
        self.has_collided = False
    def update(self):
        self.x -= self.x_vel* self.speed
        self.y -= self.y_vel* self.speed
        self.custom_update()
        self.collide()
        self.rect.x = self.x
        self.rect.y = self.y
        if self.x > WIN_WIDTH or self.x < -TILESIZE:
            self.kill()
        if self.y > WIN_HEIGHT or self.y < -TILESIZE:
            self.kill()
        if self.game.level != self.current_level:
            self.kill()
        pygame.time.delay(0)
    def collide(self):
        hits = pygame.sprite.spritecollide(self,self.game.players,False)
        if hits:
            try:
                for hit in hits:
                    if hit.is_shield and not self.has_collided:
                        self.speed *= -1
                        self.has_collided = True
            except: pass
    def custom_update(self): #for custom objects to have certain perameters and functions that update
        pass

class GroundAttack(pygame.sprite.Sprite):
    def __init__(self,game,x,y,spritesheet,frames,rect_x=TILESIZE,rect_y=TILESIZE,time = 0.1,linger=0,mega=False) -> None:
        self.x = x
        self.y = y
        self.mega = mega
        self.game = game
        self._layer = PLAYER_LAYER+1 #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.spritesheet = spritesheet
        self.image = spritesheet.get_sprite(0,0,rect_x,rect_y)
        if self.mega:
            self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.rect.x = self.x
        self.rect.y = self.y

        self.time = time #amount of frames for showing each frame
        self.frames = frames #The maximum count of animations to be incremented

        self.alpha = 255
        self.current_level = self.game.level
        self.can_hurt = False
        self.animation_frame = 0

        self.linger = linger #fade amount (14 max)
        self.has_collided = False
    def update(self):
        self.custom_update()
        self.collide()
        self.animate()
        if self.game.level != self.current_level:
            self.kill()
        pygame.time.delay(0)
    def animate(self):
        self.image = self.spritesheet.get_sprite(floor(self.animation_frame)*self.rect_x,0,self.rect_x,self.rect_y)
        self.image.set_alpha(int(self.alpha))
        if self.mega:
            self.image = pygame.transform.scale2x(self.image)
        
        if self.animation_frame > self.frames / 2:
            self.alpha -= 15 - self.linger
        
        if self.animation_frame > self.frames / 3 and self.animation_frame < self.frames / 1.5 and self.linger != 15:
            self.can_hurt = True
        else:
            self.can_hurt = False
        if self.animation_frame < self.frames:
            self.animation_frame += self.time
        elif self.alpha < 20:
            self.kill()
    def collide(self):
        hits = pygame.sprite.spritecollide(self,self.game.players,False)
        if hits:
            try:
                for hit in hits:
                    if hit.is_shield and not self.has_collided:
                        self.has_collided = True
            except: pass
    def custom_update(self): #for custom objects to have certain perameters and functions that update
        pass
####
class EnemyHealthBar(pygame.sprite.Sprite):
    def __init__(self, enemy):
        self.enemy = enemy
        self._layer = 7
        self.groups = self.enemy.game.profile
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = 9 * TILESIZE
        self.y = 24
        self.max_health_bar = Image(self.enemy.game, self.x, self.y, self.enemy.game.enemy_health_spritesheet.get_sprite(336,0,336,192),5) #gets the max health from the profile UI spritesheet
        self.health_bar = Image(self.enemy.game, self.x, self.y, self.enemy.game.enemy_health_spritesheet.get_sprite(336*4,192,336,192), 5) #gets the current health from the profile UI spritesheet
        self.max_health_dots = Image(self.enemy.game,self.x,self.y,self.enemy.game.enemy_health_spritesheet.get_sprite(336*4,192*2,336,192)) #gets the max mana from the profile UI spritesheet
        self.health_dots = Image(self.enemy.game,self.x,self.y,self.enemy.game.enemy_health_spritesheet.get_sprite(336*3,192*3,336,192), 5) #gets the max mana from the profile UI spritesheet
        self.image = pygame.Surface((0,0))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect() #gets the correct player to display in the profile UI
        self.rect.x,self.rect.y = self.x, self.y

    def update(self): #updates all the parts of the profile
        if self.enemy.max_health > 50: #In case not a perfect value
            if self.enemy.health > 50:
                self.max_health_bar.image = self.enemy.game.enemy_health_spritesheet.get_sprite(52*6*(23),0,52*6,48)
            else:
                self.max_health_bar.image = self.enemy.game.enemy_health_spritesheet.get_sprite(52*6*(22),0,52*6,48) #updates the max health based on the max health
        else:
            self.max_health_bar.image = self.enemy.game.enemy_health_spritesheet.get_sprite(52*6*(((self.enemy.max_health if self.enemy.max_health <= 50 else 50) / 2 - 2)),0,52*6,48) #updates the max health based on the max health
        self.health_bar.image = self.enemy.game.enemy_health_spritesheet.get_sprite(52*6*(self.enemy.health % 50),48,52*6,48)
        self.max_health_dots.image = self.enemy.game.enemy_health_spritesheet.get_sprite(52*6*(int(self.enemy.max_health / 50) - 1 if self.enemy.max_health > 50 else 0),96,52*6,48)
        self.health_dots.image = self.enemy.game.enemy_health_spritesheet.get_sprite(52*6*(int(self.enemy.health / 50) if self.enemy.health > 50 else 0),144,52*6,48)
        
        if self.enemy.health > 0:
            self.max_health_bar.image.set_alpha(255)
            self.health_bar.image.set_alpha(255)
            self.max_health_dots.image.set_alpha(255)
            self.health_dots.image.set_alpha(255)
        else:
            self.max_health_bar.image.set_alpha(0)
            self.health_bar.image.set_alpha(0)
            self.max_health_dots.image.set_alpha(0)
            self.health_dots.image.set_alpha(0)
            
##############
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x=7, y=7, image_coords = (0,0),has_weapon = True,width=(48,48)):
        self.game = game
        self.max_health = 10
        self.health = self.max_health
        self.speed = 1.5

        self.has_weapon = has_weapon
        self._layer = PLAYER_LAYER #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = width[0]
        self.height = width[1]

        self.image = self.game.enemy_spritesheet.get_sprite(image_coords[0]*48,image_coords[1]*48,self.width,self.height)
        if self.has_weapon:
            self.weapon = self.game.enemy_spritesheet.get_sprite(image_coords[0]*48,image_coords[1]*48+48,self.width,self.height)
            self.weapon_angle = 90
            self.weapon_copy = Image(self.game,self.x+20,self.y,pygame.transform.rotate(self.weapon,self.weapon_angle),PLAYER_LAYER+1)
        
        self.original_image = self.image
        
        self.hit_image = self.image.copy()
        var = pygame.PixelArray(self.hit_image)
        var.replace(pygame.Color(255,255,255), pygame.Color(255,0,0))
        del var

        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)

        self.x_change = 0 #x_vel
        self.y_change = 0 #y_vel

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.last_hit = 0
        self.hit_cooldown = 100
        self.alpha = 255
        self.can_hit = True
    def update(self):
        self.movement()
        if self.has_weapon:
            self.handle_weapon()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x = self.rect.x
        self.y = self.rect.y
        self.collide()
        self.x_change = 0
        self.y_change = 0
        if self.health < 1:
            self.alpha -= 15
            self.image.set_alpha(self.alpha)
        if self.alpha < 1 and self.alive():
            self.death_loot()
            self.game.enemies_remaining -= 1
            if self.has_weapon:
                self.weapon_copy.kill()
            
            self.kill()
    def death_loot(self):
        self.game.player.experience += 1
        SFX.enemy_death.play()    
    def movement(self):
        self.chase()
    def collide(self):
        if self.y > (WIN_HEIGHT - TILESIZE):
            self.rect.y = (WIN_HEIGHT - TILESIZE)
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        elif self.y < 0:
            self.rect.y = 0
        if self.x > (WIN_WIDTH - TILESIZE):
            self.rect.x = (WIN_WIDTH-TILESIZE)
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        elif self.x < 1:
            self.rect.x = 0 
        hits = pygame.sprite.spritecollide(self,self.game.attacks, False)
        if hits:
            if pygame.time.get_ticks() - self.last_hit > self.hit_cooldown:
                self.last_hit = pygame.time.get_ticks()
                if self.game.enemy_health_display == None:
                    self.game.enemy_health_display = EnemyHealthBar(self)
                else:
                    self.game.enemy_health_display.enemy = self
                try:
                    if self.game.player.mana + 0.05 < self.game.player.max_mana:
                        self.game.player.mana += 0.05
                except: pass
        if (hits or pygame.time.get_ticks() - self.last_hit <= self.hit_cooldown) and self.can_hit:
            self.image = self.hit_image
        else:
            self.image = self.original_image

    def chase(self):
        player_x,player_y = self.game.player.x,self.game.player.y
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(player_x - self.x, player_y - self.rect.y)
        dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
        dirvect.scale_to_length(self.speed)
        self.x_change, self.y_change = dirvect.x, dirvect.y
    def handle_weapon(self):
        mouse_x, mouse_y = self.game.player.x, self.game.player.y
        self.weapon_angle = (180 / pi) * -atan2(mouse_y-self.y, mouse_x-self.x)
        self.weapon_copy.image = pygame.transform.rotate(self.weapon,self.weapon_angle)
        self.weapon_copy.x = self.x + 32
        self.weapon_copy.y = self.y
        self.weapon_copy.rect.x = self.x + 32
        self.weapon_copy.rect.y = self.y

# Area 1 Enemies
class Thief(Enemy):
    def __init__(self, game, x=7, y=7):
        super().__init__(game, x, y, (0,0))
        self.shuriken_cooldown = 7500
        self.last_shuriken = pygame.time.get_ticks() + random.randint(0,7500)
        self.max_health = 12
        self.health = self.max_health
        self.shuriken_image = self.game.enemy_spritesheet.get_sprite(6,48+6,36,36)
    def throw_shuriken(self):
        if (pygame.time.get_ticks() - self.last_shuriken > self.shuriken_cooldown or self.last_shuriken == 0):
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.last_shuriken = pygame.time.get_ticks()
            SFX.throw_two.play()
            Projectile(self.game,self.x,self.y,(self.game.player.x-45,self.game.player.y-45),self.shuriken_image)
            Projectile(self.game,self.x,self.y,(self.game.player.x+45,self.game.player.y+45),self.shuriken_image)
    def chase(self):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
        
        if abs(dirvect.x) > 210.0 or abs(dirvect.y) > 210.0:
            self.throw_shuriken()
            self.speed = 1.5
        elif abs(dirvect.x) < 70.0 or abs(dirvect.y) < 70.0:
            self.speed = 1.5
            self.player_x,self.player_y = self.game.player.x, self.game.player.y
        else:
            self.speed = 1.5
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            #dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
        if pygame.time.get_ticks() - self.last_shuriken > self.shuriken_cooldown - 500:
            dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
            self.avoid()
        # Move along this normalized vector towards the player at current speed.
        if dirvect.x != 0 and dirvect.y != 0:
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
        else:
            dirvect = pygame.math.Vector2(random.randint(-1,1),random.randint(-1,1))
            self.speed = 0
        self.x_change, self.y_change = dirvect.x, dirvect.y
    def avoid(self):
        self.speed = -3
    def death_loot(self):
        self.game.player.experience += 2
        SFX.enemy_death.play()
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)

class Archer(Enemy):
    def __init__(self, game, x,y):
        super().__init__(game, x, y,(1,0)) #(1,0) is the tilemap coordinate for the Archer
        self.arrow_cooldown = 5000
        self.last_arrow = pygame.time.get_ticks() + random.randint(0,5000)
        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        self.max_health = 12
        self.health = self.max_health
        self.arrow_image = self.game.enemy_spritesheet.get_sprite(48,96,18,48)
    def throw_arrow(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.arrow_cooldown or self.last_arrow == 0): #If able to shoot arrow, shoot a shot of three
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.last_arrow = pygame.time.get_ticks()
            SFX.throw_circle.play()
            Projectile(self.game,self.x,self.y,(self.game.player.x,self.game.player.y),self.arrow_image) #shoots three arrows towards the player in a triple shot format
            Projectile(self.game,self.x,self.y,(self.game.player.x-115,self.game.player.y-115),self.arrow_image)
            Projectile(self.game,self.x,self.y,(self.game.player.x+115,self.game.player.y+115),self.arrow_image)
    def chase(self):
        self.roam()
    def roam(self):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
        
        if abs(dirvect.x) > 100.0 or abs(dirvect.y) > 100.0:
            self.throw_arrow()
            self.speed = 2
        if pygame.time.get_ticks() - self.last_arrow > self.arrow_cooldown:
            self.player_x, self.player_y = self.game.player.x,self.game.player.y
            dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
            self.speed = -2
        if dirvect.x != 0 and dirvect.y != 0:
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
        else:
            dirvect = pygame.math.Vector2(0,0)
            self.speed = 0
        # Move along this normalized vector towards the player at current speed.
        
        self.x_change, self.y_change = dirvect.x, dirvect.y
    def death_loot(self):
        self.game.player.experience += 1
        SFX.enemy_death.play()
        ManaOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
# Area 2 Enemies

class Block(Enemy):
    def __init__(self, game, x, y, target_pos, speed=2,type=1,oneshot=True,wait_time=0,random_wait=False,image_coords=(2,3),image_size=(48,48)) -> None:
        super().__init__(game,x,y,image_coords,False,image_size)
        self.speed = speed
        self.initial_pos = (x*TILESIZE,y*TILESIZE)
        self.final_pos = (target_pos[0]*TILESIZE, target_pos[1]*TILESIZE)
        self.state = 0
        self.health = 8
        self.oneshot = oneshot
        self.can_hit = False
        self.can_hurt = False
        self.target_x = target_pos[0]*TILESIZE
        self.target_y = target_pos[1]*TILESIZE
        self.angle = atan2(self.y-self.target_y,self.x-self.target_x)
        self.x_change = cos(self.angle)*-1 * self.speed
        self.y_change = sin(self.angle)*-1 * self.speed
        self.current_level = self.game.level
        
        if self.game.level == 5:
            self.game.enemies_remaining += 1
        self.alpha = 0
        
        self.type = type #0 = Constant, 1 = Ease In Out, 2 = Exponential, 3 = 1s Delay, 4 = Random
        self.last_wait = pygame.time.get_ticks() 
        self.wait_time = wait_time
        self.random_wait = random_wait
    def movement(self):
        self.tick()
        if self.wait_time == 0 or pygame.time.get_ticks() - self.last_wait > self.wait_time:
            self.can_hurt = True
            if abs(self.x-self.target_x) < 10 and abs(self.y-self.target_y) < 10:
                if self.state == 0:
                    if self.oneshot == True:
                        self.alpha -= 3
                        self.image.set_alpha(self.alpha)
                        self.x_change,self.y_change = 0,0
                    else:
                        if self.wait_time == 0 or pygame.time.get_ticks() - self.last_wait > self.wait_time:
                            self.target_x,self.target_y = self.initial_pos
                            self.state = 1
                        else:
                            self.last_wait = pygame.time.get_ticks()
                            if self.random_wait == True:
                                self.wait_time = random.randint(500,2000)
                            else:
                                self.wait_time = 1000

                else:
                    self.target_x,self.target_y = self.final_pos
                    self.state = 0
        else:
            self.x_change,self.y_change = 0,0
            self.can_hurt = False
            self.alpha += 3
            self.image.set_alpha(self.alpha)
    def death_loot(self):
        pass
    def tick(self):
        self.angle = atan2(self.y-self.target_y,self.x-self.target_x)
        if self.type == 0:
            self.x_change = cos(self.angle) * -1 * self.speed*2
            self.y_change = sin(self.angle) * - 1 * self.speed*2
        elif self.type == 1:
            self.x_change = cos(self.angle) * -1 * self.speed/2 * (abs(round(float(self.x-self.target_x)))+40) / 80.0
            self.y_change = sin(self.angle) * - 1 * self.speed/2 * (abs(round(float(self.y-self.target_y)))+40) / 80.0
        else:
            self.x_change = cos(self.angle) * -1 * self.speed*4 / (abs(round(float(self.x-self.target_x))+1)) * 50.0
            self.y_change = sin(self.angle) * - 1 * self.speed*4 / (abs(round(float(self.y-self.target_y))+1)) * 50.0

        if self.game.level != self.current_level:
            self.kill()
class SmallBlock(Block):
    def __init__(self, game, x, y, target_pos, speed=2, type=0, oneshot=False, wait_time=0, random_wait=False, image_coords=(2, 3), image_size=(48, 48)) -> None:
        super().__init__(game, x, y, target_pos, speed, type, oneshot, wait_time, random_wait, image_coords, image_size)
class MediumBlock(Block):
    def __init__(self, game, x, y, target_pos, speed=3, type=1, oneshot=False, wait_time=0, random_wait=False, image_coords=(3, 2), image_size=(96, 96)) -> None:
        super().__init__(game, x, y, target_pos, speed, type, oneshot, wait_time, random_wait, image_coords, image_size)
class LargeBlock(Block):
    def __init__(self, game, x, y, target_pos, speed=3, type=0, oneshot=True, wait_time=1000, random_wait=False, image_coords=(2, 4), image_size=(144, 144)) -> None:
        super().__init__(game, x, y, target_pos, speed, type, oneshot, wait_time, random_wait, image_coords, image_size)
class Rock(Projectile):
    def __init__(self, game, x, y, target_pos, image, speed=2) -> None:
        super().__init__(game, x, y, target_pos, image, speed)
        self.wait = random.randint(1000,3000)
        self.spawn_time = pygame.time.get_ticks()
    def custom_update(self):
        if self.spawn_time == 0:
            return
        if pygame.time.get_ticks() - self.spawn_time > self.wait:
            self.spawn_time = 0
            self.target_x,self.target_y = self.game.player.x+24,self.game.player.y+24
            dirvect = pygame.math.Vector2(self.target_x - self.x, self.target_y - self.y).normalize()
            dirvect.scale_to_length(self.speed*-2)
            self.x_vel, self.y_vel = dirvect.x, dirvect.y
        else:
            self.x_vel = cos(pygame.time.get_ticks()) *2
            self.y_vel = sin(pygame.time.get_ticks()) *2
class BanditAttack(Projectile):
    def __init__(self, game, x, y, target_pos, image, speed=4, decay=0) -> None:
        super().__init__(game, x, y, target_pos, image, speed)
        self.alpha = 255
    def custom_update(self):
        if self.game.player.power == 0:
            self.alpha -= 1
            self.speed = 3
            self.image.set_alpha(self.alpha)
            if self.alpha < 1:
                self.kill()
class Bandit(Enemy):
    def __init__(self, game, x,y):
        super().__init__(game, x, y,(2,0))
        self.arrow_cooldown = 5000
        self.last_arrow = pygame.time.get_ticks() + random.randint(0,1000)
        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        self.max_health = 18
        self.health = self.max_health
        self.swipe_image = self.game.enemy_spritesheet.get_sprite(96,96,48,48)
    def throw_arrow(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.arrow_cooldown or self.last_arrow == 0): #If able to shoot arrow, shoot a shot of three
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = random.randint(-2,2)
            self.last_arrow = pygame.time.get_ticks()
            self.arrow_cooldown = 1000
    def dash(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.arrow_cooldown or self.last_arrow == 0):
            self.player_x,self.player_y = self.game.player.x,self.game.player.y
            if random.randint(0,1):
                self.speed = 3
                SFX.throw_one.play()
                BanditAttack(self.game,self.x+32,self.y,(self.game.player.x,self.game.player.y),self.swipe_image)
            else:
                self.speed = -3
                SFX.throw_one.play()
                BanditAttack(self.game,self.x+32,self.y,(self.game.player.x-10,self.game.player.y-10),self.swipe_image)
            self.last_arrow = pygame.time.get_ticks()
            self.arrow_cooldown = 500

    def chase(self):
        self.roam()
    def roam(self):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
        
        if abs(dirvect.x) > 200.0 or abs(dirvect.y) > 200.0:
            random.choice([self.throw_arrow,self.dash])()
            self.speed = 2
        if pygame.time.get_ticks() - self.last_arrow > self.arrow_cooldown:
            self.player_x, self.player_y = self.game.player.x,self.game.player.y
            dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
            self.speed = -2
        if dirvect.x != 0 and dirvect.y != 0:
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
        else:
            dirvect = pygame.math.Vector2(0,0)
            self.speed = 0
        # Move along this normalized vector towards the player at current speed.
        
        self.x_change, self.y_change = dirvect.x, dirvect.y
    def death_loot(self):
        self.game.player.experience += 1
        SFX.enemy_death.play()
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
class SandAttack(GroundAttack):
    def __init__(self, game, x, y, spritesheet, frames, time=0.1) -> None:
        super().__init__(game, x, y, spritesheet, frames, 64, 64, time)
class Sandrider(Enemy):
    def __init__(self, game, x,y):
        super().__init__(game, x, y,(3,0))
        self.arrow_cooldown = 3000
        self.last_arrow = pygame.time.get_ticks()
        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        self.max_health = 18
        self.health = self.max_health
        self.rock_image = self.game.enemy_spritesheet.get_sprite(156,60,24,24)
    def sandfall(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.arrow_cooldown or self.last_arrow == 0): #If able to shoot arrow, shoot a shot of three
            self.speed = 2
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.last_arrow = pygame.time.get_ticks()
            self.arrow_cooldown = random.randint(800,5000)
            SFX.throw_one.play()
            SandAttack(self.game,self.game.player.x,self.game.player.y,self.game.sand_rise,10)
    def rocks(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.arrow_cooldown or self.last_arrow == 0):
            SFX.charge.play()
            Rock(self.game,self.x+32,self.y,(self.game.player.x,self.game.player.y),self.rock_image)
            Rock(self.game,self.x-32,self.y,(self.game.player.x,self.game.player.y),self.rock_image) #shoots two arrows towards the player in a triple shot format
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 3
            self.last_arrow = pygame.time.get_ticks()
            self.arrow_cooldown = 2000
    def dash(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.arrow_cooldown or self.last_arrow == 0):
            self.player_x, self.player_y = self.game.player.x,self.game.player.y
            self.last_arrow = pygame.time.get_ticks()
            self.arrow_cooldown = 400
            SandAttack(self.game,self.x,self.y,self.game.sand_rise,10)
            self.speed = 6
    def chase(self):
        self.roam()
    def roam(self):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
        if abs(dirvect.x) > 200.0 or abs(dirvect.y) > 200.0:
            random.choice([self.sandfall,self.dash,self.rocks])()
        if pygame.time.get_ticks() - self.last_arrow > self.arrow_cooldown:
            self.player_x, self.player_y = self.game.player.x,self.game.player.y
            dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
            self.speed = -2
        if dirvect.x != 0 and dirvect.y != 0:
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
        else:
            dirvect = pygame.math.Vector2(0,0)
            self.speed = 0
        # Move along this normalized vector towards the player at current speed.
        
        self.x_change, self.y_change = dirvect.x, dirvect.y
    def death_loot(self):
        self.game.player.experience += 2
        SFX.enemy_death.play()
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
        ManaOrb(self.game,self.x,self.y)

class Sentry(Enemy):
    def __init__(self, game, x,y):
        super().__init__(game, x, y,(4,0),False) #(1,0) is the tilemap coordinate for the Archer
        self.arrow_cooldown = 10000
        self.last_arrow = pygame.time.get_ticks() + random.randint(1000,5000)
        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        self.max_health = 8
        self.health = self.max_health
        self.arrow_image = self.game.enemy_spritesheet.get_sprite(48*4,48,18,48)
        self.shoot_limit = 10
        self.shoot_count = 0
    def shoot(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.arrow_cooldown or self.last_arrow == 0): #If able to shoot arrow, shoot a shot of three
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.last_arrow = pygame.time.get_ticks()
            if self.shoot_count != self.shoot_limit:
                self.arrow_cooldown = 400
                self.shoot_count += 1
            else:
                self.arrow_cooldown = random.randint(5000,10000)
                self.shoot_count = 0
            SFX.laser.play()
            SFX.laser.fadeout(300)
            Projectile(self.game,self.x+32,self.y,(self.game.player.x,self.game.player.y),self.arrow_image,9) #shoots three arrows towards the player in a triple shot format
    
    def movement(self): #no movement
        self.shoot()
    def death_loot(self):
        self.game.player.experience += 3
        SFX.enemy_death.play()
        ManaOrb(self.game,self.x,self.y)
        ManaOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)

# Area 3 Enemies
class WarriorStrike(Projectile):
    def __init__(self, game, x, y, target_pos, image, speed=4, decay=0) -> None:
        super().__init__(game, x, y, target_pos, image, speed)
        self.alpha = 255
        self.x_vel *= 1.1
        self.y_vel *= 1.1
    def custom_update(self):
        self.image.set_alpha(self.alpha)
        self.alpha -= 6
        if self.game.player.power == 0:
            self.x_vel /= 1.5
            self.y_vel /= 1.5 #Decays
        else:
            self.x_vel *= 0.95
            self.y_vel *= 0.95
        if self.alpha <= 0:
            self.kill()
class Warrior(Enemy):
    def __init__(self, game, x,y):
        super().__init__(game, x, y,(5,0))
        self.cooldown = 800
        self.last_arrow = pygame.time.get_ticks() + random.randint(0,8090)
        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        self.max_health = 30
        self.health = self.max_health
        self.arrow_image = self.game.enemy_spritesheet.get_sprite(240,144,96,30)
        self.speed = 2.5
    def throw_arrow(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0): #If able to shoot arrow, shoot a shot of three
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 2
            self.can_hit = True
            self.image.set_alpha(255)
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = random.randrange(500,2000)
            SFX.sword_shing.play()
            WarriorStrike(self.game,self.x+32,self.y,(self.game.player.x+24,self.game.player.y+24),self.arrow_image,5)
            WarriorStrike(self.game,self.x+32,self.y,(random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)),self.arrow_image,5)
    def chase(self):
        self.roam()
    def dash(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
            self.can_hit = False
            self.image.set_alpha(125)
            if random.randint(0,1):
                self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            else:
                self.player_x,self.player_y = self.game.player.x, self.game.player.y
            self.speed = 4.5
            SFX.dash.play()
            WarriorStrike(self.game,self.x+32,self.y,(random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)),self.arrow_image,7)
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = 400
    def roam(self):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
        if abs(dirvect.x) < 150.0 or abs(dirvect.y) < 150.0:
            if random.randint(0,2):
                self.throw_arrow()
            else:
                self.dash()
        if pygame.time.get_ticks() - self.last_arrow > self.cooldown:
            self.player_x,self.player_y = self.game.player.x, self.game.player.y
            self.speed = 2.5
        if dirvect.x != 0 and dirvect.y != 0:
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
        else:
            dirvect = pygame.math.Vector2(0,0)
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 0
        # Move along this normalized vector towards the player at current speed.
        
        self.x_change, self.y_change = dirvect.x, dirvect.y
    def death_loot(self):
        self.game.player.experience += 3
        SFX.enemy_death.play()
        ManaOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)

class ApprenticeOrb(Projectile):
    def __init__(self, game, x, y, target_pos, image, speed=2, decay=0) -> None:
        super().__init__(game, x, y, target_pos, image, speed)
        self.alpha = 255
    def custom_update(self):
        self.image.set_alpha(self.alpha)
        self.x_vel += cos(pygame.time.get_ticks())/5
        self.y_vel += sin(pygame.time.get_ticks())/5 #Decays
        if self.alpha <= 0:
            self.kill()
class Apprentice(Enemy):
    def __init__(self, game, x,y):
        super().__init__(game, x, y,(6,0))
        self.cooldown = 800
        self.last_arrow = pygame.time.get_ticks() + random.randint(0,8090)
        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        self.max_health = 30
        self.health = self.max_health
        self.orb_image = self.game.enemy_spritesheet.get_sprite(288,96,30,30)
        self.speed = 2.5
    def throw_arrow(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0): #If able to shoot arrow, shoot a shot of three
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 2
            self.can_hit = True
            self.image.set_alpha(255)
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = random.randrange(500,3000)
            SFX.orb_throw.play()
            for i in range(random.randint(1,4)):
                ApprenticeOrb(self.game,self.x+32,self.y,(random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)),self.orb_image)
            ApprenticeOrb(self.game,self.x+32,self.y,(self.game.player.x,self.game.player.y),self.orb_image) #shoots three arrows towards the player in a triple shot format
    def chase(self):
        self.roam()
    def dash(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
            self.can_hit = False
            self.image.set_alpha(125)
            if random.randint(0,1):
                self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            else:
                self.player_x,self.player_y = self.game.player.x, self.game.player.y
            self.speed = 4.5
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = 400
    def roam(self):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
        if abs(dirvect.x) < 150.0 or abs(dirvect.y) < 150.0:
            if random.randint(0,2):
                self.throw_arrow()
            else:
                pass #self.dash()
        if pygame.time.get_ticks() - self.last_arrow > self.cooldown:
            self.player_x,self.player_y = self.game.player.x, self.game.player.y
            self.speed = 2.5
        if dirvect.x != 0 and dirvect.y != 0:
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
        else:
            dirvect = pygame.math.Vector2(0,0)
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 0
        # Move along this normalized vector towards the player at current speed.
        
        self.x_change, self.y_change = dirvect.x, dirvect.y
    def death_loot(self):
        self.game.player.experience += 2
        SFX.enemy_death.play()
        ManaOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)

# Area 4 Enemies

class Angel(Enemy):
    pass

class GuardSword(Projectile):
    def __init__(self, game, x, y, target_pos, image, speed=4, rotate=True) -> None:
        super().__init__(game, x, y, target_pos, image, speed, rotate)
        self.angle += random.randrange(1,50)
        self.x_vel = 0
        self.y_vel = 0
        self.a_vel = 9
        self.image_copy = self.image
        self.can_hurt = False
    def custom_update(self):
        if abs(self.angle - (atan2(self.y-self.target_y,self.x-self.target_x))) < 2 or (self.a_vel < 0.4 and self.a_vel != 0):
            if abs(self.angle - (atan2(self.y-self.target_y,self.x-self.target_x))) < 2:
                self.x_vel = cos(self.angle)
                self.y_vel = sin(self.angle)
            self.angle = atan2(self.y-self.target_y,self.x-self.target_x)
            self.a_vel = 0
            self.can_hurt = True
        self.angle += self.a_vel
        self.a_vel *= 0.95
        self.image = pygame.transform.rotate(self.image_copy,self.angle)
        if self.game.player.power != 0:
            self.x_vel *= 1.1
            self.y_vel *= 1.1
class IceAttack(GroundAttack):
    def __init__(self, game, x, y, spritesheet, frames, time=0.05,linger=13) -> None:
        super().__init__(game, x, y, spritesheet, frames, 48, 96, time,linger)
class Guard(Enemy):
    def __init__(self, game, x,y):
        super().__init__(game, x, y,(10,0),False)
        self.cooldown = 800
        self.last_arrow = pygame.time.get_ticks()
        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        self.max_health = 40
        self.health = self.max_health
        self.sword_image = self.game.enemy_spritesheet.get_sprite(486,96,30,48)
        self.speed = 2.5
    def throw_arrow(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 2
            self.can_hit = True
            self.image.set_alpha(255)
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = random.randrange(500,3000)
            SFX.orb_throw.play()
            GuardSword(self.game,self.x+random.randint(-48,48),self.y+random.randint(-48,48),(self.game.player.x,self.game.player.y),self.sword_image)
            GuardSword(self.game,self.x+random.randint(-48,48),self.y+random.randint(-48,48),(self.game.player.x+32,self.game.player.y+32),self.sword_image) 
            GuardSword(self.game,self.x+random.randint(-48,48),self.y+random.randint(-48,48),(self.game.player.x-32,self.game.player.y-32),self.sword_image) 
    def chase(self):
        self.roam()
    def dash(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
            self.player_x, self.player_y = self.game.player.x,self.game.player.y
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = 400
            SFX.dash.play()
            IceAttack(self.game,self.x,self.y,self.game.ice_attack,8)
            SFX.ice_attack.play()
            self.speed = 7
    def ice_circle(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
            for i in range(8):
                IceAttack(self.game,self.x+cos(i*10)*96,self.y+sin(i*10)*96,self.game.ice_attack,8)
            SFX.ice_attack.play()
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = 1000
            self.speed = 0
    def ice_line(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
            SFX.ice_attack.play()
            angle = atan2(self.y-self.game.player.y, self.x - self.game.player.x)
            dx = cos(angle) * 48
            dy = sin(angle) * 48
            for i in range(8):
                IceAttack(self.game,self.x - dx*i,self.y-dy*i,self.game.ice_attack,8)
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = 1000
            self.speed = 0
    def roam(self):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
        if abs(dirvect.x) < 150.0 or abs(dirvect.y) < 150.0:
            if random.randint(0,1):
                self.throw_arrow()
            elif random.randint(0,1):
                self.ice_circle()
            elif random.randint(0,2):
                self.ice_line()
            else:
                self.dash()
        if pygame.time.get_ticks() - self.last_arrow > self.cooldown:
            self.player_x,self.player_y = self.game.player.x, self.game.player.y
            self.speed = 2.5
        if dirvect.x != 0 and dirvect.y != 0:
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
        else:
            dirvect = pygame.math.Vector2(0,0)
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 0
        # Move along this normalized vector towards the player at current speed.
        
        self.x_change, self.y_change = dirvect.x, dirvect.y
    def death_loot(self):
        self.game.player.experience += 2
        SFX.enemy_death.play()
        ManaOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)

#BOSSES

class Boss(pygame.sprite.Sprite): #Base class for all bosses (with displaying images, etc.)
    def __init__(self, game, image_file, x=7, y=7, image_coords=(0,0),width=(48,48)):
        self.game = game
        self.max_health = 10
        self.health = self.max_health
        self.speed = 1.5

        self._layer = PLAYER_LAYER #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = width[0]
        self.height = width[1]
        self.image_file = image_file
        self.image = image_file.get_sprite(image_coords[0]*self.width,image_coords[1]*self.height,self.width,self.height)
        
        self.original_image = self.image

        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)

        self.x_change = 0 #x_vel
        self.y_change = 0 #y_vel
        if self.max_health > 50:
            self.game.player.health = self.game.player.max_health
            self.game.player.mana = self.game.player.max_mana
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.last_hit = 0
        self.hit_cooldown = 50
        self.alpha = 255
        self.can_hit = True
    def update(self):
        self.animate()
        self.movement()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x = self.rect.x
        self.y = self.rect.y
        self.collide()
        self.x_change = 0
        self.y_change = 0
        self.image.set_alpha(self.alpha)
        if self.health < 1:
            self.alpha -= 15
            if self.alpha < 1 and self.alive():
                self.death_loot()
                self.game.enemies_remaining -= 1
                SFX.enemy_death.play()
                self.kill()
    def death_loot(self):
        self.game.player.experience = 0
        self.game.player.level_up()
        self.game.player.health = self.game.player.max_health
        self.game.player.mana = self.game.player.max_mana
            
    def movement(self):
        self.chase()
    def collide(self):
        if self.y > (WIN_HEIGHT - TILESIZE):
            self.rect.y = (WIN_HEIGHT - TILESIZE)
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        elif self.y < 0:
            self.rect.y = 0
        if self.x > (WIN_WIDTH - TILESIZE):
            self.rect.x = (WIN_WIDTH-TILESIZE)
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        elif self.x < 1:
            self.rect.x = 0 
        hits = pygame.sprite.spritecollide(self,self.game.attacks, False)
        if hits:
            if pygame.time.get_ticks() - self.last_hit > self.hit_cooldown:
                self.last_hit = pygame.time.get_ticks()
                if self.game.enemy_health_display == None:
                    self.game.enemy_health_display = EnemyHealthBar(self)
                else:
                    self.game.enemy_health_display.enemy = self
                try:
                    if self.game.player.mana + 0.05 < self.game.player.max_mana:
                        self.game.player.mana += 0.05
                except: pass
    def animate(self):
        pass
    def chase(self):
        player_x,player_y = self.game.player.x,self.game.player.y
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(player_x - self.x, player_y - self.rect.y)
        dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
        dirvect.scale_to_length(self.speed)
        self.x_change, self.y_change = dirvect.x, dirvect.y

class Rogue(Boss):
    def __init__(self, game, x=7, y=7, image_coords=(0, 0), width=(108, 96)):
        image_file = game.rogue_spritesheet
        super().__init__(game, image_file, x, y, image_coords, width)
        self.game = game
        self.idle_frame = 0
        self.shadow_frame = 0
        self.max_health = 100
        self.health = self.max_health
        self.can_hit = True
        self.width = width[0]
        self.height = width[1]
        self.cooldown = 800
        self.last_arrow = pygame.time.get_ticks() + random.randint(0,2090)
        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        self.arrow_image = self.game.rogue_spritesheet.get_sprite(240,0,48,48)
        self.can_hurt = True
        self.speed = 2.5
        self.is_shadow = False
        self.last_hit
    def throw_arrow(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0): #If able to shoot arrow, shoot a shot of three
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 2
            self.can_hit = True
            self.image.set_alpha(255)
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = 1500
            SFX.throw_two.play()
            Projectile(self.game,self.x+24,self.y,(self.game.player.x-30,self.game.player.y-30),self.arrow_image,4)
            Projectile(self.game,self.x+24,self.y,(self.game.player.x+30,self.game.player.y+30),self.arrow_image,4) #shoots three arrows towards the player in a triple shot format
    def circle_shurikens(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
            Projectile(self.game,self.x+24,self.y,(self.x - WIN_WIDTH, self.y),self.arrow_image,3)
            Projectile(self.game,self.x+24,self.y,(self.x + WIN_WIDTH, self.y),self.arrow_image,3)
            Projectile(self.game,self.x+24,self.y,(self.x, self.y-WIN_HEIGHT),self.arrow_image,3)
            Projectile(self.game,self.x+24,self.y,(self.x, self.y+WIN_HEIGHT),self.arrow_image,3)
            SFX.throw_circle.play()
            self.cooldown = 2000
            self.player_x,self.player_y = WIN_HEIGHT/2,WIN_HEIGHT/2
            self.speed = 2
            self.can_hit = True
            self.image.set_alpha(255)
            self.last_arrow = pygame.time.get_ticks()
    def random_throw(self): #teleports to random areas (for 3-5 times)
        pass
    def chase(self):
        self.roam()
    def dash(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
            self.can_hit = False
            self.image.set_alpha(125)
            if random.randint(0,1):
                self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            else:
                self.player_x,self.player_y = self.game.player.x, self.game.player.y
            self.speed = 3
            WarriorStrike(self.game,self.x+32,self.y,(random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)),self.arrow_image,3)
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = 200
    def roam(self):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
        if abs(dirvect.x) < 150.0 or abs(dirvect.y) < 150.0:
            if self.is_shadow == False:
                if random.randint(0,2):
                    self.throw_arrow()
                elif random.randint(0,1):
                    self.circle_shurikens()
                elif random.randint(0,1):
                    self.dash()
                else:
                    self.shadow()
            else:
                if random.randint(0,1):
                    self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
                else:
                    self.player_x,self.player_y = self.game.player.x, self.game.player.y
        if pygame.time.get_ticks() - self.last_arrow > self.cooldown:
            self.player_x,self.player_y = self.game.player.x, self.game.player.y
            self.speed = 2.5
            if self.is_shadow:
                if self.max_health == 100:
                    Shadow(self.game,self.x/TILESIZE,self.y/TILESIZE)
                self.is_shadow = False
                self.can_hit = True
                self.can_hurt = True
                self.last_arrow = pygame.time.get_ticks() 
        if dirvect.x != 0 and dirvect.y != 0:
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
        else:
            dirvect = pygame.math.Vector2(0,0)
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 0
        # Move along this normalized vector towards the player at current speed.
        
        self.x_change, self.y_change = dirvect.x, dirvect.y    
    def animate(self):
        if not self.is_shadow:
            if self.shadow_frame >= 0.01:
                self.shadow_frame -= 0.1
                self.image = self.game.rogue_spritesheet.get_sprite(108*floor(self.shadow_frame),96,self.width,self.height)
            else:
                self.shadow_frame = 0
                self.idle_frame += 0.02
                self.image = self.game.rogue_spritesheet.get_sprite(108*floor(self.idle_frame),0,self.width,self.height)
                if self.idle_frame >= 1.98:
                    self.idle_frame = 0
        else:
            self.idle_frame = 0
            self.shadow_frame += 0.1
            if self.shadow_frame >= 2.99:
                self.shadow_frame = 3
            self.image = self.game.rogue_spritesheet.get_sprite(108*floor(self.shadow_frame),96,self.width,self.height)    
    def shadow(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
            self.idle_frame = 0
            self.shadow_frame = 0
            self.is_shadow = True
            self.can_hit = False
            self.can_hurt = False
            self.image.set_alpha(125)
            self.speed = 3
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = 3000
            
class Shadow(Rogue):
    def __init__(self, game, x, y, image_coords=(0, 2), width=(108, 96)):
        super().__init__(game, x, y, image_coords, width)
        self.can_hit = True
        self.can_hurt = True
        self.health = 16
        self.max_health = 16
        self.game.enemies_remaining += 1
        self.shadow_shuriken_image = self.game.rogue_spritesheet.get_sprite(240,192,48,48)
        self.big_shadow_shuriken_image = self.game.rogue_spritesheet.get_sprite(288,192,96,96)
    def animate(self):
        if not self.is_shadow:
            if self.shadow_frame >= 0.01:
                self.shadow_frame -= 0.1
                self.image = self.game.rogue_spritesheet.get_sprite(108*floor(self.shadow_frame),96*3,self.width,self.height)
            else:
                self.shadow_frame = 0
                self.idle_frame += 0.02
                self.image = self.game.rogue_spritesheet.get_sprite(108*floor(self.idle_frame),96*2,self.width,self.height)
                if self.idle_frame >= 1.98:
                    self.idle_frame = 0
        else:
            self.idle_frame = 0
            self.shadow_frame += 0.1
            if self.shadow_frame >= 2.99:
                self.shadow_frame = 3
            self.image = self.game.rogue_spritesheet.get_sprite(108*floor(self.shadow_frame),96*3,self.width,self.height)    
    def throw_arrow(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0): #If able to shoot arrow, shoot a shot of three
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 1.5
            self.can_hit = True
            self.image.set_alpha(255)
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = 2000
            if random.randint(0,1):
                Projectile(self.game,self.x+32,self.y,(random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)),self.shadow_shuriken_image,4)
                Projectile(self.game,self.x+32,self.y,(random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)),self.shadow_shuriken_image,4)
            else:
                Projectile(self.game,self.x+32,self.y,(self.game.player.x,self.game.player.y),self.big_shadow_shuriken_image,3) #shoots three arrows towards the player in a triple shot format
    def death_loot(self):
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)
        HealthOrb(self.game,self.x,self.y)

class EnemyLightning(GroundAttack):
    def __init__(self, game, x, y, spritesheet, frames, time=0.04,mega=False) -> None:
        if mega:
            super().__init__(game, x, y, spritesheet, frames, 48, 96, 0.05,5,mega)
        else:
            super().__init__(game, x, y, spritesheet, frames, 48, 96, time,10,mega)
class HoningLightning(EnemyLightning):
    def __init__(self, game, x, y, spritesheet, frames, time=0.06,count=0,count_limit=10,mega=False) -> None:
        if mega:
            super().__init__(game, x, y, spritesheet, frames, 0.05,mega)
        else:
            super().__init__(game, x, y, spritesheet, frames, time,mega)
        SFX.lightning_attack.play()
        self.has_repeated = False
        self.count = count
        self.count_limit = count_limit #however many times it wants to be repeated
    def custom_update(self):
        self.angle = atan2(self.y-self.game.player.y,self.x-self.game.player.x)
        if not self.mega:
            if self.animation_frame > 1 and not self.has_repeated and self.count != self.count_limit:
                self.dx = cos(self.angle) * -60 #moves it closer to the player
                self.dy = sin(self.angle) * -60
                HoningLightning(self.game, self.x + self.dx,self.y + self.dy,self.spritesheet,self.frames,self.time,self.count+1,self.count_limit,self.mega)
                self.has_repeated = True
        else:
            if self.animation_frame > 2 and not self.has_repeated and self.count != self.count_limit:
                self.dx = cos(self.angle) * -96 #moves it closer to the player
                self.dy = sin(self.angle) * -96
                HoningLightning(self.game, self.x + self.dx,self.y + self.dy,self.spritesheet,self.frames,self.time,self.count+1,self.count_limit,self.mega)
                self.has_repeated = True
class Guardian(Boss):
    def __init__(self, game, x=7, y=7, image_coords=(0, 0), width=(108, 96)):
        image_file = game.guardian_spritesheet
        super().__init__(game, image_file, x, y, image_coords, width)
        self.game = game
        self.idle_frame = 0
        self.shadow_frame = 0
        self.max_health = 200
        self.health = self.max_health
        self.can_hit = True
        self.can_hurt = True
        self.width = width[0]
        self.height = width[1]
        self.cooldown = 800
        self.last_arrow = pygame.time.get_ticks() + random.randint(0,2090)
        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        self.arrow_image = self.game.guardian_spritesheet.get_sprite(48,198,28,48)
        
        self.attack_count = 0
        self.visible = True
        self.speed = 2.5
    def throw_arrow(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0): #If able to shoot arrow, shoot a shot of three
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 2.5
            self.can_hit = True
            self.image.set_alpha(255)
            self.last_arrow = pygame.time.get_ticks()
            if self.health > 150:
                self.cooldown = 2000
            elif self.health > 100:
                self.cooldown = 1300
            elif self.health > 50: 
                self.cooldown = 1000
            else:
                self.cooldown = 900
            if random.randint(0,1):
                Projectile(self.game,self.x+32,self.y,(random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)),self.arrow_image,5)
            else:
                Projectile(self.game,self.x+32,self.y,(self.game.player.x,self.game.player.y),self.arrow_image,5) #shoots three arrows towards the player in a triple shot format
            SFX.laser.play()
            self.attack_count += 1
    def chase(self):
        self.roam()
    def blocks(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
            self.can_hit = False
            self.image.set_alpha(0)
            if random.randint(0,3):
                self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            else:
                self.player_x,self.player_y = self.game.player.x, self.game.player.y
            self.speed = 0
            for i in range(random.randint(3,5)):
                if random.randint(0,1): #Left/Right
                    lane_y = random.randint(0,4)*3
                    if random.randint(0,1):
                        LargeBlock(self.game,0,lane_y,(14,lane_y),2,1)
                    else:
                        LargeBlock(self.game,14,lane_y,(0,lane_y),2,1)
                else: #Up/Down
                    lane_x = random.randint(0,4)*3
                    if random.randint(0,1):
                        LargeBlock(self.game,lane_x,0,(lane_x,14),2,1)
                    else:
                        LargeBlock(self.game,lane_x,14,(lane_x,0),2,1)

            SFX.charge.play()
            self.last_arrow = pygame.time.get_ticks()
            if self.health > 50:
                self.cooldown = 2000
            else:
                self.cooldown = 1200
    def honing_lightning(self,mega=False): #Hones towards the player
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
            self.player_x,self.player_y = 7*TILESIZE,7*TILESIZE
            if mega:
                HoningLightning(self.game,random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT),self.game.lightning_attack,6,0.03,0,3,mega)
            else:
                HoningLightning(self.game,random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT),self.game.lightning_attack,6,0.04,0,10,mega)
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = 1500
    def random_lightning(self,mega = False):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 2
            if not mega:
                if self.health > 100:
                    amount = 4 #amount of attacks
                elif self.health > 50:
                    amount = 7
                else:
                    amount = 12
                for i in range(amount):
                    EnemyLightning(self.game,random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT),self.game.lightning_attack,6,0.05,mega)
            else:
                amount = 8
                for i in range(amount):
                    EnemyLightning(self.game,random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT),self.game.lightning_attack,6,0.03,mega)
            SFX.lightning_attack.play()
            
            self.image.set_alpha(255)
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = random.randint(1000,1500)
    def rocks(self):
        pass
    def roam(self):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
        if abs(dirvect.x) < 150.0 or abs(dirvect.y) < 150.0:
            if self.visible:
                if pygame.time.get_ticks() - self.last_arrow > self.cooldown:
                    self.attack_count += 1
                if self.attack_count < 30:
                    if not random.randint(0,2):
                        if self.game.player.power != 0:
                                self.throw_arrow()
                    elif random.randint(0,2):
                        self.random_lightning(False)
                        
                elif self.attack_count >= 30:
                    self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
                    self.cooldown = 10000
                    if pygame.time.get_ticks() - self.last_arrow > self.cooldown:
                        self.attack_count = 0
                        self.cooldown = 800
                        self.last_arrow = pygame.time.get_ticks()
                        self.player_x,self.player_y = 7*TILESIZE, 7*TILESIZE
                if random.randint(0,2):
                    if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0) and self.health < 100 and self.attack_count < 30:
                        self.player_x,self.player_y = 7*TILESIZE, 7*TILESIZE
                        self.attack_count = 0
                        self.visible = False
                        self.can_hit = False
                        self.can_hurt = False
                        SFX.disappear.play()
                        self.attack_count = 0
                        self.last_arrow = pygame.time.get_ticks()
                        self.cooldown = 2000
                        self.player_x,self.player_y = 7*TILESIZE, 7*TILESIZE
                        return
                elif random.randint(0,2):
                    self.honing_lightning() 
            else:
                if pygame.time.get_ticks() - self.last_arrow > self.cooldown:
                    self.attack_count += 1
                if self.attack_count < 7:
                    if random.randint(0,1):
                        self.blocks()
                    elif random.randint(0,1):
                        self.random_lightning(True)
                    else:
                        self.honing_lightning(True)  
                else:
                    if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
                        self.rect.x, self.rect.y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
                        self.x = self.rect.x
                        self.y = self.rect.y
                        self.visible = True
                        self.can_hurt = True
                        self.can_hit = True
                        self.attack_count = 0
                        SFX.disappear.play()
                        self.cooldown = 4000
                        self.last_arrow = pygame.time.get_ticks()
                
        if pygame.time.get_ticks() - self.last_arrow > self.cooldown:
            self.player_x,self.player_y = self.game.player.x, self.game.player.y
            self.speed = 2
        if dirvect.x != 0 and dirvect.y != 0:
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
        else:
            dirvect = pygame.math.Vector2(0,0)
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 0
        # Move along this normalized vector towards the player at current speed.
        
        self.x_change, self.y_change = dirvect.x, dirvect.y    
    def animate(self):
        if self.visible:
            if self.alpha < 255:
                self.alpha += 5
        else:
            if self.alpha > 0:
                self.alpha -= 5
        self.idle_frame += 0.02
        self.image = self.game.guardian_spritesheet.get_sprite(108*floor(self.idle_frame),0,self.width,self.height)
        if self.idle_frame >= 1.98:
            self.idle_frame = 0  

class Hex(GroundAttack):
    def __init__(self, game, x, y, spritesheet, frames, rect_x=32*6, rect_y=24*6, time=0.05, linger=15, mega=False) -> None:
        super().__init__(game, x, y, spritesheet, frames, rect_x, rect_y, time, linger, mega)
        self.dx = 0
        self.dy = 0
        self.angle = 90
        self.timer = 0
    def custom_update(self):
        if floor(self.timer) != 4:
            self.timer += 0.01
            self.x -= self.dx
            self.y -= self.dy
            self.rect.x = self.x
            self.rect.y = self.y
            self.angle = atan2(self.y-self.game.player.y+48,self.x-self.game.player.x+48)
            self.dx = cos(self.angle) * 3
            self.dy = sin(self.angle) * 3
        else:
            self.kill()
            HexAttack(self.game,self.x,self.y,self.game.hex2_attack,5)
        if self.animation_frame >= 2.9:
            self.animation_frame = 0
            
class HexAttack(Hex):
    def __init__(self, game, x, y, spritesheet, frames, rect_x=32 * 6, rect_y=24 * 6, time=0.05, linger=5, mega=False) -> None:
        super().__init__(game, x, y, spritesheet, frames, rect_x, rect_y, time, linger, mega)
    def custom_update(self):
        pass
class EnemyFire(Projectile):
    def __init__(self, game, x, y, target_pos, image, speed=2,rotate=False,clockwise=True,type =0) -> None:
        super().__init__(game, x, y, target_pos, image, speed,rotate)
        self.clockwise = clockwise
        self.type = type #0: constant, 1: exponential out, 2: exponential slowdown
        self.x_vel /= 1.5
        self.y_vel /= 1.5
    def custom_update(self):
        if self.clockwise:
            self.x_vel -= cos(90+self.angle)/100
            self.y_vel -= sin(90+self.angle)/100
        else:
            self.x_vel += cos(90+self.angle)/100
            self.y_vel += sin(90+self.angle)/100
        self.x_vel /= 1.005
        self.y_vel /= 1.005

class Sorcerer(Boss):
    def __init__(self, game, x=7, y=7, image_coords=(0, 0), width=(120, 120)):
        image_file = game.sorcerer_spritesheet
        super().__init__(game, image_file, x, y, image_coords, width)
        self.game = game
        self.idle_frame = 0
        self.shadow_frame = 0
        self.max_health = 250
        self.health = self.max_health
        self.can_hit = True
        self.width = width[0]
        self.height = width[1]
        self.cooldown = 800
        self.last_arrow = pygame.time.get_ticks() + random.randint(0,2090)
        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        self.arrow_image = self.game.sorcerer_spritesheet.get_sprite(48,120,30,36)
        self.can_hurt = True
        self.speed = 2.5

        self.attack_count = 0
    def throw_arrow(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0): #If able to shoot arrow, shoot a shot of three
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 3
            self.can_hit = True
            self.image.set_alpha(255)
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = random.randint(500,1500)
            if random.randint(0,1):
                clockwise = True
            else:
                clockwise = False
            if random.randint(0,1):
                mode = 0
            elif random.randint(0,1):
                mode = 1
            else:
                mode = 2
            EnemyFire(self.game,self.x,self.y,(0, 0),self.arrow_image,2,False,clockwise,mode)
            EnemyFire(self.game,self.x,self.y,(WIN_HEIGHT/2, 0),self.arrow_image,2,False,clockwise,mode)
            EnemyFire(self.game,self.x,self.y,(WIN_HEIGHT/2, WIN_HEIGHT),self.arrow_image,2,False,clockwise,mode)
            EnemyFire(self.game,self.x,self.y,(WIN_HEIGHT, 0),self.arrow_image,2,False,clockwise,mode)
            EnemyFire(self.game,self.x,self.y,(0, WIN_HEIGHT/2),self.arrow_image,2,False,clockwise,mode)
            EnemyFire(self.game,self.x,self.y,(WIN_HEIGHT, WIN_HEIGHT/2),self.arrow_image,2,False,clockwise,mode)
            EnemyFire(self.game,self.x,self.y,(0, WIN_HEIGHT),self.arrow_image,2,False,clockwise,mode)
            EnemyFire(self.game,self.x,self.y,(WIN_HEIGHT, WIN_HEIGHT),self.arrow_image,2,False,clockwise,mode)
            SFX.fire_attack.play()
            self.attack_count += 1
    def chase(self):
        self.roam()
    def hex(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
            self.player_x,self.player_y = WIN_HEIGHT/2,WIN_HEIGHT/2
            self.speed = -3
            self.cooldown = 1000
            self.last_arrow = pygame.time.get_ticks()
            Hex(self.game,self.x,self.y,self.game.hex_attack,3)
            self.attack_count += 1
    def roam(self):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
        if abs(dirvect.x) < 150.0 or abs(dirvect.y) < 150.0:
            if self.attack_count < 10:
                if random.randint(0,10):
                    self.throw_arrow()
                    
                else:
                    self.hex()
            else:
                self.cooldown = 10000
                self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT) 
                self.speed = 2   
                if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
                    self.last_arrow = pygame.time.get_ticks()
                    self.player_x,self.player_y = WIN_HEIGHT/2, WIN_HEIGHT/2
                    self.cooldown = 1000
                    self.speed = 3.5  
                    self.attack_count = 0

        if pygame.time.get_ticks() - self.last_arrow > self.cooldown:
            self.player_x,self.player_y = self.game.player.x, self.game.player.y
            self.speed = 3
        if dirvect.x != 0 and dirvect.y != 0:
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
        else:
            dirvect = pygame.math.Vector2(0,0)
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 0
        # Move along this normalized vector towards the player at current speed.
        
        self.x_change, self.y_change = dirvect.x, dirvect.y    
    def animate(self):
        self.idle_frame += 0.02
        self.image = self.game.sorcerer_spritesheet.get_sprite(120*floor(self.idle_frame),0,self.width,self.height)
        if self.idle_frame >= 1.98:
            self.idle_frame = 0  

class Prince(Boss):
    def __init__(self, game, x=7, y=7, image_coords=(0, 0), width=(120, 114)):
        image_file = game.prince_spritesheet
        super().__init__(game, image_file, x, y, image_coords, width)
        self.game = game
        self.idle_frame = 0
        self.shadow_frame = 0
        self.max_health = 350
        self.health = self.max_health
        self.can_hit = True
        self.width = width[0]
        self.height = width[1]
        self.cooldown = 800
        self.last_arrow = pygame.time.get_ticks() + random.randint(0,2090)
        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        self.sword_image = self.game.enemy_spritesheet.get_sprite(486,96,30,48)
        self.can_hurt = True
        self.speed = 2.5
        self.visible = True

        self.attack_count = 0
        self.opening_cooldown = 20000
        self.last_opening = pygame.time.get_ticks()
    def throw_arrow(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0): #If able to shoot arrow, shoot a shot of three
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 3
            self.can_hit = True
            self.image.set_alpha(255)
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = random.randrange(1000,1500)
            SFX.orb_throw.play()
            if random.randint(0,1):
                GuardSword(self.game,self.x+random.randint(-48,48),self.y+random.randint(-48,48),(self.game.player.x,self.game.player.y),self.sword_image)
            else:
                GuardSword(self.game,random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT),(random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)),self.sword_image)
                GuardSword(self.game,random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT),(random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)),self.sword_image)
            self.attack_count += 1
            if self.attack_count >= 18:
                self.last_opening = pygame.time.get_ticks()
    def chase(self):
        self.roam()
    def roam(self):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
        if self.visible:
            if abs(dirvect.x) < 150.0 or abs(dirvect.y) < 150.0:
                if random.randint(0,3) and self.attack_count < 18:
                    self.throw_arrow()
                else:
                    if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
                        self.visible = False
                        self.can_hit = False
                        self.can_hurt = False
                        self.cooldown = 500
                        self.last_arrow = pygame.time.get_ticks()
                        SFX.disappear.play()
            if self.attack_count >= 18:
                self.opening_cooldown = 10000
                if (pygame.time.get_ticks() - self.last_opening > self.opening_cooldown):
                    self.cooldown = 500
                    self.last_arrow = pygame.time.get_ticks()
                    self.attack_count = 0
        else:
            if random.randint(0,1) and self.attack_count < 18:
                if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
                    SFX.orb_throw.play()
                    self.attack_count += 1
                    if self.attack_count >= 18:
                        self.last_opening = pygame.time.get_ticks()
                    self.cooldown = 750
                    self.last_arrow = pygame.time.get_ticks()
                    SFX.disappear.play()
                    for i in range(random.randint(1,2)):
                        GuardSword(self.game,random.randint(0,WIN_HEIGHT),random.randint(0,WIN_HEIGHT),(self.game.player.x,self.game.player.y),pygame.transform.scale2x(self.sword_image),5)
            else:
                if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0):
                        self.x,self.y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
                        self.rect.x,self.rect.y = self.x,self.y
                        self.visible = True
                        self.can_hit = True
                        self.can_hurt = True
                        self.last_arrow = pygame.time.get_ticks()
                        if self.attack_count < 12:
                            self.cooldown = 1500
                        else:
                            self.cooldown = 5000
                        SFX.disappear.play()
        if pygame.time.get_ticks() - self.last_arrow > self.cooldown:
            self.player_x,self.player_y = self.game.player.x, self.game.player.y
            self.speed = 3
        if dirvect.x != 0 and dirvect.y != 0:
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
        else:
            dirvect = pygame.math.Vector2(0,0)
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            SFX.orb_throw.play()
            GuardSword(self.game,random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT),(self.game.player.x,self.game.player.y),self.sword_image)
            self.speed = 0
        # Move along this normalized vector towards the player at current speed.
        
        self.x_change, self.y_change = dirvect.x, dirvect.y    
    def animate(self):
        self.idle_frame += 0.02
        self.image = self.game.prince_spritesheet.get_sprite(120*floor(self.idle_frame),0,self.width,self.height)
        if self.idle_frame >= 1.98:
            self.idle_frame = 0 
        if self.visible:
            if self.alpha < 255:
                self.alpha += 5
        else:
            if self.alpha > 0:
                self.alpha -= 5

class Empress(Boss):
    def __init__(self, game, x=7, y=7, image_coords=(0, 0), width=(180, 120)):
        image_file = game.empress_spritesheet
        super().__init__(game, image_file, x, y, image_coords, width)
        self.game = game
        self.idle_frame = 0
        self.shadow_frame = 0
        self.max_health = 450
        self.health = self.max_health
        self.can_hit = True
        self.width = width[0]
        self.height = width[1]
        self.cooldown = 800
        self.last_arrow = pygame.time.get_ticks() + random.randint(0,2090)
        self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
        self.arrow_image = self.game.sorcerer_spritesheet.get_sprite(48,120,30,36)
        self.blue_image = self.game.enemy_spritesheet.get_sprite(486,96,30,48)
        self.yellow_image = self.game.guardian_spritesheet.get_sprite(48,198,28,48)
        self.pink_image = self.game.sorcerer_spritesheet.get_sprite(48,120,30,36)
        self.can_hurt = True
        self.speed = 4
        self.is_transforming = False
        self.form_values = {"basic":0,"blue":2,"pink":4,"yellow":6,"soul":8,"twisted":10}
        self.form = "basic"

    def phase_change(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0): #If able to shoot arrow, shoot a shot of three
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 4
            self.can_hit = True
            self.image.set_alpha(255)
            self.form = random.choice(["basic","blue","pink","yellow","soul","twisted"])
            self.last_arrow = pygame.time.get_ticks()
            self.cooldown = 2000
            SFX.orb_special.play()
    def phase_attack(self):
        if (pygame.time.get_ticks() - self.last_arrow > self.cooldown or self.last_arrow == 0): #If able to shoot arrow, shoot a shot of three
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 3
            self.can_hit = True
            for i in range(random.randint(1,5)):
                if self.form == "basic":
                    pass
                if self.form == "twisted":
                    GroundAttack(self.game,self.player_x,self.player_y,self.game.dark_attack,6,48,78,0.05)
                elif self.form == "pink":
                    SFX.fire_attack.play()
                    Projectile(self.game,self.x,self.y,(self.player_x,self.player_y),self.pink_image,3)
                elif self.form == "yellow":
                    SFX.laser.play()
                    Projectile(self.game,self.x,self.y,(self.player_x,self.player_y),self.yellow_image,4)
                elif self.form == "blue":
                    SFX.orb_throw.play()
                    GuardSword(self.game,self.x,self.y,(self.player_x,self.player_y),self.blue_image)
                self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            if self.form == "blue":
                SFX.dash.play()
                self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
                self.speed = 6
                self.cooldown = 300
                self.can_hit = False
                self.image.set_alpha(200)
                
            else:
                self.cooldown = 200
            self.last_arrow = pygame.time.get_ticks()  
    def chase(self):
        self.roam()
    def roam(self):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(self.player_x - self.x, self.player_y - self.rect.y)
        if abs(dirvect.x) < 150.0 or abs(dirvect.y) < 150.0:
            if not self.form in ["blue","pink","yellow"]:
                if random.randint(0,10):
                    self.phase_attack()
                else:
                    self.phase_change()
            else:
                if random.randint(0,4):
                    self.phase_attack()
                else:
                    self.phase_change()
        if pygame.time.get_ticks() - self.last_arrow > self.cooldown:
            self.player_x,self.player_y = self.game.player.x, self.game.player.y
            self.speed = 4
        if dirvect.x != 0 and dirvect.y != 0:
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
        else:
            dirvect = pygame.math.Vector2(0,0)
            self.player_x,self.player_y = random.randint(0,WIN_HEIGHT), random.randint(0,WIN_HEIGHT)
            self.speed = 0
        # Move along this normalized vector towards the player at current speed.
        
        self.x_change, self.y_change = dirvect.x, dirvect.y    
    def animate(self):
        self.idle_frame += 0.05
        self.image = self.game.empress_spritesheet.get_sprite(180*floor(self.idle_frame),120*self.form_values[self.form],self.width,self.height)
        if self.idle_frame >= 2.95:
            self.idle_frame = 0 

##############################################################

class Text: #Unused for now, but will be used when there are more text requirements for things
    def __init__(self, x, y, width, height, fg, bg, content, fontsize) -> None:
        self.font = pygame.font.Font('Assets/Font/royal-intonation.ttf', fontsize)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.content = content
        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self. y
        self.text = self.font.render(self.content, True, self.fg, self.bg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)
class Button: 
    def __init__(self, x, y, width, height, fg, bg, content, fontsize) -> None:
        self.font = pygame.font.Font('Assets/Font/royal-intonation.ttf', fontsize)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.content = content
        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self. y
        self.text = self.font.render(self.content, True, self.fg, self.bg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    def is_hovered(self,pos,pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return False
            return True
        return False
    