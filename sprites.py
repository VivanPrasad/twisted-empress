from config import *
import pygame, random
from math import *

class Spritesheet:
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
class Profile(pygame.sprite.Sprite): #Profile Handler for Player
    def __init__(self, player):
        self.player = player
        self._layer = 4
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
        
        self.image = self.player.game.profile_spritesheet.get_sprite(336*self.player.power,192*6,56*6,32*6) #gets the correct player to display in the profile UI
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self): #updates all the parts of the profile
        self.max_health_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.max_health / 2 - 2),0,336,192) #updates the max health based on the max health
        self.health_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.health),192,336,192)
        self.max_mana_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.max_mana - 3),192*2,336,192)
        self.mana_bar.image = self.player.game.profile_spritesheet.get_sprite(336*floor(self.player.mana),192*3,336,192)
        self.max_experience_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.max_experience / 2 - 4),192*4,336,192)
        self.experience_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.experience),192*5,336,192)

class Image(pygame.sprite.Sprite): #Images without any functions or movement (just for display and updated framing, mainly UI)
    def __init__(self,game, x, y, image,layer = 4):
        self.game = game
        self._layer = layer
        self.groups = self.game.profile
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, power = 0):
        self.game = game
        self.power = power

        self.profile = Profile(self)
        
        self.stat_tree = {
            0:[], #Lionheart Stat Tree
            1:[], #Odyssey Stat Tree
            2:[]  #Acuity Stat Tree
        }
        self.level = 1
        self.max_health = 22
        self.health = self.max_health
        
        self.max_mana = 5
        self.mana = self.max_mana
        self.experience = 0
        self.max_experience = self.level * 2 + 6

        print(f'''
        level:{self.level}
        health:{self.health}/{self.max_health}
        mana:{self.mana}/{self.max_mana}
        xp:{self.experience}/{self.max_experience}
        ''')

        self._layer = PLAYER_LAYER #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.all_sprites
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

        self.dash_cooldown = 2000
        self.basic_cooldown = 700 - 100*self.power
        self.special_cooldown = 1000
        self.last_dashed = 0
        self.last_basic = 0
        self.dashing = 1
        self.last_special = 0

        self.hit_cooldown = 500
        self.last_hit = 0
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
        #self.image.set_alpha(random.randint(0,255))
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

        if pygame.time.get_ticks() - self.last_dashed > self.dash_cooldown / 8:
            self.dashing = 1

        if keys[pygame.K_SPACE]:
            self.dash()
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
            if pygame.time.get_ticks() - self.last_hit > self.hit_cooldown:
                self.last_hit = pygame.time.get_ticks()
                self.health -= 1
                print(self.health)
        if hits or pygame.time.get_ticks() - self.last_hit <= self.hit_cooldown:
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
            self.last_dashed = pygame.time.get_ticks()
    def basic_attack(self):
        if (pygame.time.get_ticks() - self.last_basic > self.basic_cooldown or self.last_basic == 0):
            self.last_basic = pygame.time.get_ticks()
            if int(self.mana + 0.25) < self.max_mana:
                self.mana += 0.25
            else:
                self.mana = self.max_mana
            self.basic = BasicAttack(self.game, self.x+32,self.y, (self.game.mouse_pos[0],self.game.mouse_pos[1]))
    def special_attack(self):
        if (pygame.time.get_ticks() - self.last_special > self.special_cooldown or self.last_special == 0) and self.mana >= 1:
            self.last_special = pygame.time.get_ticks()
            self.mana -= 1
            self.special = SpecialAttack(self.game, self.x+32,self.y, (self.game.mouse_pos[0],self.game.mouse_pos[1]))

class BasicAttack(pygame.sprite.Sprite):
    def __init__(self,game,x,y,mouse_pos) -> None:
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
            self.image = self.game.attack_spritesheet.get_sprite(0,96,self.width*2,self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.current_level = self.game.level
        self.angle = (180 / pi) * -atan2(self.mouse_y-self.y, self.mouse_x-self.x)-90
        self.arrow_copy = pygame.transform.rotate(self.image,self.angle)
        self.image = self.arrow_copy
        self.alpha = 255
        self.animation_frame = 0
    def update(self):
        self.collide()
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
        if self.game.player.power == 0:
            if not self.animation_frame > 2:
                self.x = self.game.player.x - self.x_vel * self.speed * 2 - 20
                self.y = self.game.player.y - self.y_vel * self.speed * 2 - 20
            else:
                self.x_vel = 0
                self.y_vel = 0
            self.alpha -= 3
            if self.animation_frame < 5:
                self.animation_frame += 0.08
            else:
                self.kill()
            self.image = self.image = self.game.attack_spritesheet.get_sprite(0,96+(48*floor(self.animation_frame)),self.width*2,self.height)
            self.attack_copy = pygame.transform.rotate(self.image,self.angle)
            self.image = self.attack_copy
            self.image.set_alpha(int(self.alpha))
            #if self.alpha < 1: self.kill()
        pygame.time.delay(0)
    def collide(self):
        hits = pygame.sprite.spritecollide(self,self.game.enemies, False)
        if hits:
            if self.game.player.power != 0:
                self.kill()
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
        self.speed = 10
        self.angle = atan2(y-mouse_y,x-mouse_x)
        self.x_vel = cos(self.angle) * self.speed
        self.y_vel = sin(self.angle) * self.speed
        
        self.image = self.game.attack_spritesheet.get_sprite(48*self.game.player.power,48,self.width,self.height)
        
        if self.game.player.power == 0:
            self.image = self.game.attack_spritesheet.get_sprite(self.width*2,96,self.width*2,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

        angle = (180 / pi) * -atan2(mouse_y-self.y, mouse_x-self.x)-90
        self.arrow_copy = pygame.transform.rotate(self.image,angle)
        self.image = self.arrow_copy
        self.alpha = 255
    def update(self):
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
            self.alpha -= 2
            self.image.set_alpha(self.alpha)
            if self.alpha < 1:
                self.kill()
        pygame.time.delay(0)
       
class Spell(pygame.sprite.Sprite):
    pass

class Enemy(pygame.sprite.Sprite):
    pass
    #spawn_pos
    #health
    #available attacks
    #chase mechanic by getting (self.game.player.x,self.game.player.y)
    def __init__(self, game, x=7, y=7, image_coords = (0,0)):
        self.game = game
        self.health = 15
        self.speed = 1.5

        self._layer = PLAYER_LAYER #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.enemy_spritesheet.get_sprite(image_coords[0]*48,image_coords[1]*48,self.width,self.height)
        self.weapon = self.game.enemy_spritesheet.get_sprite(image_coords[0]*48,image_coords[1]*48+48,self.width,self.height)
        self.weapon_angle = 90
        self.weapon_copy = Image(self.game,self.x+20,self.y,pygame.transform.rotate(self.weapon,self.weapon_angle),PLAYER_LAYER+1)
        self.original_image = self.image
        
        self.hit_image = self.image.copy()
        var = pygame.PixelArray(self.hit_image)
        var.replace(pygame.Color(255,255,255), pygame.Color(255,0,0))
        del var

        self.x_change = 0 #x_vel
        self.y_change = 0 #y_vel

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.last_hit = 0
        self.hit_cooldown = 300
        self.alpha = 255
    def update(self):
        self.movement()
        self.handle_weapon()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x = self.rect.x
        self.y = self.rect.y
        self.collide()
        self.x_change = 0
        self.y_change = 0
        if self.health < 1:
            self.alpha -= 10
            self.image.set_alpha(self.alpha)
        if self.alpha < 1:
            if self.alive():
                self.game.enemies_remaining -= 1
            self.weapon_copy.kill()
            self.kill()
            
    def movement(self):
        self.chase()
    def collide(self):
        if self.y > (WIN_HEIGHT - TILESIZE):
            self.rect.y = (WIN_HEIGHT - TILESIZE)
        elif self.y < 0:
            self.rect.y = 0
        if self.x > (WIN_WIDTH - TILESIZE):
            self.rect.x = (WIN_WIDTH-TILESIZE)
        elif self.x < 1:
            self.rect.x = 0 
        hits = pygame.sprite.spritecollide(self,self.game.attacks, False)
        if hits:
            if pygame.time.get_ticks() - self.last_hit > self.hit_cooldown:
                self.last_hit = pygame.time.get_ticks()
                self.health -= 1
                print(self.health)
        if hits or pygame.time.get_ticks() - self.last_hit <= self.hit_cooldown:
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

class Projectile(pygame.sprite.Sprite):
    def __init__(self,game,x,y,target_pos,image) -> None:
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.game = game

        self._layer = PLAYER_LAYER+1 #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.target_x, self.target_y = target_pos
        self.speed = 4
        self.angle = atan2(y-self.target_y,x-self.target_x)
        self.x_vel = cos(self.angle) * self.speed
        self.y_vel = sin(self.angle) * self.speed
        
        self.image = image
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.current_level = self.game.level
        self.angle = (180 / pi) * -atan2(self.target_y-self.y, self.target_x-self.x)-90
        self.arrow_copy = pygame.transform.rotate(self.image,self.angle)
        self.image = self.arrow_copy
        self.animation_frame = 0
    def update(self):
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
        pygame.time.delay(0)

class Boss(pygame.sprite.Sprite):
    pass

# Area 1 Enemies
class Thief(Enemy):
    def __init__(self, game, x=7, y=7):
        super().__init__(game, x, y)
        self.shuriken_cooldown = 4500
        self.last_shuriken = pygame.time.get_ticks() + random.randint(0,4500)
    def throw_shuriken(self):
        if (pygame.time.get_ticks() - self.last_shuriken > self.shuriken_cooldown or self.last_shuriken == 0):

            self.last_shuriken = pygame.time.get_ticks()
            Projectile(self.game,self.x,self.y,(self.game.player.x-20,self.game.player.y-20),self.game.enemy_spritesheet.get_sprite(0,48,48,48))
            Projectile(self.game,self.x,self.y,(self.game.player.x+20,self.game.player.y+20),self.game.enemy_spritesheet.get_sprite(0,48,48,48))
    def chase(self):
        player_x,player_y = self.game.player.x,self.game.player.y
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(player_x - self.x, player_y - self.rect.y)
        
        print(dirvect)
        if abs(dirvect.x) > 400.0 or abs(dirvect.y) > 400.0:
            self.throw_shuriken()
            self.speed = 1.5
        elif abs(dirvect.x) < 10.0 or abs(dirvect.y) < 10.0:
            self.speed = -1
        if pygame.time.get_ticks() - self.last_shuriken > self.shuriken_cooldown:
            #dirvect = pygame.math.Vector2(player_x - self.x, player_y - self.rect.y)
            self.speed = -2.5
        dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
        dirvect.scale_to_length(self.speed)
        self.x_change, self.y_change = dirvect.x, dirvect.y
        

class Archer(Enemy):
    def __init__(self, game, x,y):
        super().__init__(game, x, y,(1,0))
        self.shuriken_cooldown = 4500
        self.last_shuriken = pygame.time.get_ticks() + random.randint(0,4500)
    def throw_shuriken(self):
        if (pygame.time.get_ticks() - self.last_shuriken > self.shuriken_cooldown or self.last_shuriken == 0):

            self.last_shuriken = pygame.time.get_ticks()
            Projectile(self.game,self.x,self.y,(self.game.player.x,self.game.player.y),self.game.enemy_spritesheet.get_sprite(48,96,48,48))
            Projectile(self.game,self.x,self.y,(self.game.player.x-96,self.game.player.y-96),self.game.enemy_spritesheet.get_sprite(48,96,48,48))
            Projectile(self.game,self.x,self.y,(self.game.player.x+96,self.game.player.y+96),self.game.enemy_spritesheet.get_sprite(48,96,48,48))
    def chase(self):
        player_x,player_y = self.game.player.x,self.game.player.y
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(player_x - self.x, player_y - self.rect.y)
        
        print(dirvect)
        if abs(dirvect.x) > 400.0 or abs(dirvect.y) > 400.0:
            self.throw_shuriken()
            self.speed = 1.5
        elif abs(dirvect.x) < 10.0 or abs(dirvect.y) < 10.0:
            self.speed = -1
        if pygame.time.get_ticks() - self.last_shuriken > self.shuriken_cooldown:
            #dirvect = pygame.math.Vector2(player_x - self.x, player_y - self.rect.y)
            self.speed = -2.5
        dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
        dirvect.scale_to_length(self.speed)
        self.x_change, self.y_change = dirvect.x, dirvect.y

# Area 2 Enemies
class Defender(Enemy):
    pass

class Sentry(Enemy):
    pass

class Detector(Enemy):
    pass

# Area 3 Enemies

class Apprentice(Enemy):
    pass

class Warrior(Enemy):
    pass

# Area 4 Enemies

class Angel(Enemy):
    pass

class Guard(Enemy):
    pass

#BOSSES

class Ninja(Boss):
    pass

class Guardian(Boss):
    pass

class Wizard(Boss):
    pass

class Prince(Boss):
    pass

##############################################################

class Text:
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
    