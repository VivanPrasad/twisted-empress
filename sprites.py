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
        self._layer = 6
        self.groups = self.player.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = 9 * TILESIZE
        self.y = 12 * TILESIZE
        self.max_health_bar = Image(self.player.game, self.x, self.y, self.player.game.profile_spritesheet.get_sprite(0,0,336,192))
        self.health_bar = Image(self.player.game, self.x, self.y, self.player.game.profile_spritesheet.get_sprite(336*4,192,336,192), 5)
        self.max_mana_bar = Image(self.player.game,self.x,self.y,self.player.game.profile_spritesheet.get_sprite(336*4,192*2,336,192))
        self.mana_bar = Image(self.player.game,self.x,self.y,self.player.game.profile_spritesheet.get_sprite(336*3,192*3,336,192), 5)
        self.max_experience_bar = Image(self.player.game,self.x,self.y,self.player.game.profile_spritesheet.get_sprite(336*2,192*4,336,192))
        self.experience_bar = Image(self.player.game,self.x,self.y,self.player.game.profile_spritesheet.get_sprite(336*5,192*5,336,192))
        
        self.image = self.player.game.profile_spritesheet.get_sprite(336*self.player.power,192*6,56*6,32*6)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self): #updates all the parts of the profile
        self.max_health_bar = self.player.game.profile_spritesheet.get_sprite(336*(self.player.max_health / 2 - 2),0,336,192) #updates the max health based on the max health
        self.health_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.health),192,336,192)
        self.max_mana_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.max_mana - 3),192*2,336,192)
        self.mana_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.mana),192*3,336,192)
        self.max_experience_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.max_experience / 2 - 4),192*4,336,192)
        self.experience_bar.image = self.player.game.profile_spritesheet.get_sprite(336*(self.player.experience),192*5,336,192)



class Image(pygame.sprite.Sprite): #Images without any functions or movement (just for display and updated framing, mainly UI)
    def __init__(self,game, x, y, image,layer = 4):
        self.game = game
        self._layer = layer
        self.groups = self.game.all_sprites
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
        self.health = 4
        self.max_health = 4
        self.mana = 3
        self.max_mana = 3
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
        self.last_dashed = 0
        self.dashing = 1
    def update(self):
        self.animate()
        self.movement()
        
        self.x_change = 1 if self.x < 1 else self.x_change
        self.x_change = -1 if self.x > WIN_WIDTH - TILESIZE - 1 else self.x_change
        self.y_change = 1 if self.y < 1 else self.y_change
        self.y_change = -1 if self.y > WIN_HEIGHT - TILESIZE - 1 else self.y_change
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x = self.rect.x
        self.y = self.rect.y
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
            self.game.screen.blit(self.image,(self.x-6,self.y-6))

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
        if (pygame.time.get_ticks() - self.last_dashed > self.dash_cooldown or self.last_dashed == 0) and self.mana > 0 and (self.x_change != 0 or self.y_change != 0):
            self.dashing = 4
            self.mana -= 1
            self.last_dashed = pygame.time.get_ticks()
class BasicAttack(pygame.sprite.Sprite):
    def __init__(self,game,x,y,mouse_pos) -> None:
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.game = game

        self._layer = PLAYER_LAYER #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.speed = 7
        self.angle = atan2(y-mouse_y,x-mouse_x)
        self.x_vel = cos(self.angle) * self.speed
        self.y_vel = sin(self.angle) * self.speed
        
        self.image = self.game.attack_spritesheet.get_sprite(48*self.game.player.power,0,self.width,self.height)
        
        if self.game.player.power == 0:
            self.image = self.game.attack_spritesheet.get_sprite(0,96,self.width*2,self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.current_level = self.game.level
        angle = (180 / pi) * -atan2(mouse_y-self.y, mouse_x-self.x)-90
        self.arrow_copy = pygame.transform.rotate(self.image,angle)
        self.image = self.arrow_copy
        self.alpha = 255
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
        if self.game.player.power == 0:
            self.x_vel *= 0.93
            self.y_vel *= 0.93
            self.alpha -= 2
            self.image.set_alpha(self.alpha)
            if self.alpha < 1:
                self.kill()

        pygame.time.delay(0)
class SpecialAttack(pygame.sprite.Sprite):
    def __init__(self,game,x,y,mouse_pos) -> None:
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.game = game
        self._layer = PLAYER_LAYER #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        mouse_x, mouse_y = pygame.mouse.get_pos()
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
    def __init__(self, game, x=7, y=7):
        self.game = game
        self.health = 4
        self.speed = 1.25

        self._layer = PLAYER_LAYER+1 #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.enemy_spritesheet.get_sprite(0,0,self.width,self.height)
        self.weapon = self.game.weapon_spritesheet.get_sprite(self.game.player.power*48,0,self.width,self.height)
        

        self.x_change = 0 #x_vel
        self.y_change = 0 #y_vel

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x += self.x_change
        self.y += self.y_change
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        self.chase()
    def chase(self):
        player_x,player_y = self.game.player.x,self.game.player.y
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(player_x - self.x, player_y - self.rect.y)
        dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
        dirvect.scale_to_length(self.speed)
        self.x_change, self.y_change = dirvect.x, dirvect.y
    def handle_weapon(self):
        pass

class Projectile(pygame.sprite.Sprite):
    pass

class Boss(pygame.sprite.Sprite):
    pass

# Area 1 Enemies
class Thief(Enemy):
    pass

class Archer(Enemy):
    pass

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
    